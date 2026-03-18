import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import mysql.connector

# ── Load environment variables ──
load_dotenv()

DB_HOST     = os.getenv('DB_HOST')
DB_USER     = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME     = os.getenv('DB_NAME')
DB_PORT     = os.getenv('DB_PORT')

print('Credentials loaded from .env ✔')

# ═══════════════════════════════
#  EXTRACT — Local MySQL
# ═══════════════════════════════
LOCAL_ENGINE = create_engine(
    'mysql+pymysql://root:Shravan%40123@localhost:3306/ipl',
    pool_pre_ping=True
)

with LOCAL_ENGINE.connect() as conn:
    delivery       = pd.read_sql('SELECT * FROM deliveries',   conn)
    player         = pd.read_sql('SELECT * FROM player',       conn)
    player_captain = pd.read_sql('SELECT * FROM player_match', conn)

print(f'Extract done — {len(delivery)} rows ✔')

# ═══════════════════════════════
#  TRANSFORM — Dream11 Scoring
# ═══════════════════════════════
temp_df = (
    player
    .merge(player_captain, on='Player_Id')
    [['Player_Name', 'Match_Id', 'Is_Captain']]
)

runs  = delivery.groupby(['match_id','batter'])['batsman_runs'].sum().reset_index()
balls = delivery.groupby(['match_id','batter'])['batsman_runs'].count().reset_index()
fours = (delivery.query('batsman_runs == 4')
         .groupby(['match_id','batter'])['batsman_runs'].count().reset_index())
sixes = (delivery.query('batsman_runs == 6')
         .groupby(['match_id','batter'])['batsman_runs'].count().reset_index())

final_df = (
    runs
    .merge(balls,  on=['match_id','batter'], suffixes=('_runs','_balls'))
    .merge(fours,  on=['match_id','batter'], how='left')
    .merge(sixes,  on=['match_id','batter'], how='left')
    .fillna(0)
)
final_df.rename(columns={
    'batsman_runs_runs' : 'runs',
    'batsman_runs_balls': 'balls',
    'batsman_runs_x'    : 'fours',
    'batsman_runs_y'    : 'sixes'
}, inplace=True)

final_df['sr'] = round((final_df['runs'] / final_df['balls'].replace(0, 1)) * 100, 2)

final_df = (
    final_df
    .merge(temp_df,
           left_on=['match_id','batter'],
           right_on=['Match_Id','Player_Name'],
           how='left')
    .drop(columns=['Player_Name','Match_Id'])
    .fillna(0)
)

def dream11(row):
    score = 0
    score += row['runs'] + row['fours'] + 2 * row['sixes']
    if row['runs'] >= 100:   score += 16
    elif row['runs'] >= 50:  score += 8
    elif row['runs'] >= 30:  score += 4
    elif row['runs'] == 0 and row['balls'] > 0: score -= 2
    if row['balls'] >= 10:
        if row['sr'] > 170:        score += 6
        elif row['sr'] > 150:      score += 4
        elif row['sr'] > 130:      score += 2
        elif 60 < row['sr'] <= 70: score -= 2
        elif 50 < row['sr'] <= 60: score -= 4
        elif row['sr'] <= 50:      score -= 6
    if row['Is_Captain'] == 1:
        score *= 2
    return score

final_df['score'] = final_df.apply(dream11, axis=1)

export_df = (
    final_df
    .sort_values('score', ascending=False)
    [['match_id','batter','runs','balls','fours','sixes','sr','Is_Captain','score']]
    .reset_index(drop=True)
)

print(f'Transform done — {len(export_df)} rows scored ✔')

# ═══════════════════════════════
#  LOAD — AWS RDS
# ═══════════════════════════════
# Step 1 — Create database
root_conn = mysql.connector.connect(
    host     = DB_HOST,
    user     = DB_USER,
    password = DB_PASSWORD
)
cursor = root_conn.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS dream11')
root_conn.commit()
root_conn.close()
print('Database ready on AWS ✔')

# Step 2 — Load using SQLAlchemy
RDS_ENGINE = create_engine(
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    pool_pre_ping=True
)

export_df.to_sql(
    name      = 'batter_points',
    con       = RDS_ENGINE,
    if_exists = 'replace',
    index     = False,
    chunksize = 500,
    method    = 'multi'
)

print(f'Load done — {len(export_df)} rows on AWS RDS ✔')
print('\n=== ETL Pipeline Complete ===')


