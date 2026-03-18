# 🏏 IPL Dream11 ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-orange?logo=mysql&logoColor=white)
![AWS RDS](https://img.shields.io/badge/AWS-RDS-FF9900?logo=amazonaws&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=sqlalchemy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> End-to-end **ETL pipeline** that extracts raw IPL cricket data from a local MySQL database,
> transforms it into **Dream11 fantasy cricket scores** using custom Python logic,
> and loads the final dataset to a live **AWS RDS (MySQL)** cloud database.

---

## 📌 Table of Contents
- [Pipeline Architecture](#-pipeline-architecture)
- [Tech Stack](#-tech-stack)
- [Dream11 Scoring Logic](#-dream11-scoring-logic)
- [Project Structure](#-project-structure)
- [Results](#-results)
- [Setup & Run](#-setup--run)
- [Output Sample](#-output-sample)
- [What I Learned](#-what-i-learned)

---

## 🏗 Pipeline Architecture

```
┌─────────────────────┐      ┌──────────────────────────┐      ┌─────────────────────┐
│   EXTRACT           │      │   TRANSFORM              │      │   LOAD              │
│                     │      │                          │      │                     │
│  MySQL Workbench    │ ───▶ │  Python + Pandas         │ ───▶ │  AWS RDS            │
│  (localhost)        │      │                          │      │  (MySQL 8.4)        │
│                     │      │  • Batting aggregation   │      │                     │
│  3 Tables:          │      │  • Dream11 scoring       │      │  ap-south-1 region  │
│  • deliveries       │      │  • Strike rate calc      │      │  dream11 database   │
│  • player           │      │  • Captain 2x bonus      │      │  batter_points      │
│  • player_match     │      │  • Milestone bonuses     │      │  table              │
│                     │      │                          │      │                     │
│  46,180 rows        │      │  2,944 player scores     │      │  2,944 rows live    │
└─────────────────────┘      └──────────────────────────┘      └─────────────────────┘
```

---

## 🛠 Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.11 |
| Data Processing | Pandas, NumPy |
| Database (Local) | MySQL 8.0, MySQL Workbench |
| Database (Cloud) | AWS RDS MySQL 8.4 |
| ORM / Connector | SQLAlchemy, pymysql, mysql-connector-python |
| Security | python-dotenv (environment variables) |
| IDE | PyCharm, Jupyter Notebook |
| Version Control | Git, GitHub |
| Cloud Region | AWS ap-south-1 (Mumbai) |

---

## 🧮 Dream11 Scoring Logic

### Batting Points
| Action | Points |
|---|---|
| Every run scored | +1 |
| Boundary bonus (4) | +1 |
| Six bonus (6) | +2 |
| 30+ runs milestone | +4 |
| 50+ runs milestone | +8 |
| 100+ runs milestone | +16 |
| Duck (0 runs, dismissed) | -2 |

### Strike Rate Bonus / Penalty (min 10 balls faced)
| Strike Rate | Points |
|---|---|
| SR > 170 | +6 |
| SR 151–170 | +4 |
| SR 131–150 | +2 |
| SR 61–70 | -2 |
| SR 51–60 | -4 |
| SR ≤ 50 | -6 |

### Captain Multiplier
| Role | Multiplier |
|---|---|
| Captain | 2× total score |
| Others | 1× total score |

---

## 📁 Project Structure

```
ipl_etl/
│
├── etl_pipeline.py       # Main ETL script — Extract, Transform, Load
├── .env.example          # Credential template (safe to share)
├── .env                  # Real credentials (local only, never on GitHub)
├── .gitignore            # Blocks .env from being pushed
└── requirements.txt      # All Python dependencies
```

---

## 📊 Results

| Stage | Metric | Value |
|---|---|---|
| Extract | Raw delivery records | 46,180 rows |
| Extract | Tables pulled | 3 (deliveries, player, player_match) |
| Transform | Player match scores computed | 2,944 rows |
| Transform | Scoring features engineered | 8 columns |
| Load | Rows loaded to AWS RDS | 2,944 rows |
| Load | Cloud database | dream11 (AWS ap-south-1) |

### 🏆 Top 10 Dream11 Scores (Live from AWS RDS)

| Rank | Player | Match ID | Score |
|---|---|---|---|
| 1 | BB McCullum | 335982 | 216.0 |
| 2 | SC Ganguly | 419158 | 200.0 |
| 3 | M Vijay | 419137 | 179.0 |
| 4 | G Gambhir | 392211 | 172.0 |
| 5 | ST Jayasuriya | 336018 | 167.0 |
| 6 | PC Valthaty | 501206 | 165.0 |
| 7 | A Symonds | 335990 | 164.0 |
| 8 | MEK Hussey | 335983 | 164.0 |
| 9 | AC Gilchrist | 335994 | 160.0 |
| 10 | SE Marsh | 336019 | 160.0 |

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/ShravanShukla-ai/ipl-dream11-etl-pipeline.git
cd ipl-dream11-etl-pipeline
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your credentials:
```
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=dream11
DB_PORT=3306
```

### 5. Run the pipeline
```bash
python etl_pipeline.py
```

### Expected Output
```
Credentials loaded from .env ✔
Extract done — 46,180 rows ✔
Transform done — 2,944 rows scored ✔
Database ready on AWS ✔
Load done — 2,944 rows on AWS RDS ✔
=== ETL Pipeline Complete ===
```

---

## 📋 Requirements

```
pandas
sqlalchemy
pymysql
mysql-connector-python
python-dotenv
cryptography
numpy
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 💡 What I Learned

- Built a **real-world ETL pipeline** from scratch using Python
- Connected to **AWS RDS** — configured Security Groups, VPC, Public Access
- Used **SQLAlchemy engine** for professional database connections
- Secured credentials using **python-dotenv** — industry standard practice
- Applied **Dream11 fantasy scoring logic** using Pandas `apply()` function
- Handled **AWS connectivity issues** — IP whitelisting, port 3306 configuration
- Used **Git & GitHub** for version control with proper `.gitignore` setup

---

## 🔐 Security

- All credentials stored in `.env` file (never committed to GitHub)
- `.gitignore` blocks `.env` from being pushed
- `.env.example` provides safe credential template for collaborators
- AWS Security Group restricts database access to authorised IPs only

---

## 👤 Author

**Shravan Shukla**
- GitHub: [@ShravanShukla-ai](https://github.com/ShravanShukla-ai)
- Location: Surat, Gujarat, India

---

## 📄 Dataset

IPL Complete Dataset (2008–2020) — sourced from Kaggle
- 46,180+ ball-by-ball delivery records
- Player profiles and match participation data

---

*Built as a Data Engineering capstone project — March 2026*
