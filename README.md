# 🏏 IPL Dream11 ETL Pipeline

End-to-end ETL pipeline that extracts IPL cricket data from MySQL,
computes Dream11 fantasy points, and loads results to AWS RDS.

## Pipeline Architecture
```
MySQL Workbench → Python/Pandas → AWS RDS (MySQL)
EXTRACT           TRANSFORM        LOAD
```

## Tech Stack
- Python, Pandas, NumPy
- MySQL, SQLAlchemy, pymysql
- AWS RDS (MySQL 8.4, ap-south-1)
- python-dotenv (secure credentials)
- PyCharm, Jupyter Notebook, Git

## Dream11 Scoring Logic
| Action | Points |
|---|---|
| Every run | +1 |
| Boundary (4) | +1 |
| Six (6) | +2 |
| 30+ runs bonus | +4 |
| 50+ runs bonus | +8 |
| 100+ runs bonus | +16 |
| Strike rate > 170 | +6 |
| Duck (0 runs) | -2 |
| Captain multiplier | 2x |

## Results
- Extracted: 46,180 delivery records
- Transformed: 2,944 player match scores
- Loaded: AWS RDS live database

## Project Structure
```
ipl_etl/
├── etl_pipeline.py   # main ETL script
├── .env.example      # credential template
├── .gitignore        # blocks .env from GitHub
└── requirements.txt  # dependencies
```

## Setup
```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/ipl-dream11-etl-pipeline

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in your credentials in .env

# Run pipeline
python etl_pipeline.py
```

## Environment Variables
Create a `.env` file with:
```
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=dream11
DB_PORT=3306
```

## Output Sample
| match_id | batter | runs | fours | sixes | sr | score |
|---|---|---|---|---|---|---|
| 335982 | BB McCullum | 158 | 10 | 13 | 205.19 | 216 |
| 419158 | SC Ganguly | 100+ | ... | ... | ... | 200 |
```

---

**Step 3 — Create `.env.example` file**
```
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=dream11
DB_PORT=3306
