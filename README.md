# MovieLens ETL Pipeline

An end-to-end ETL pipeline that downloads the public MovieLens dataset,
cleans and transforms the data using Python and pandas, and loads
analytics-ready tables into a local SQLite database — orchestrated
with Apache Airflow.

## What it does
- **Extract**: downloads MovieLens Small (100k ratings) from GroupLens
- **Validate**: checks file integrity before transformation
- **Transform**: cleans nulls/duplicates, explodes multi-genre fields,
  computes avg rating per genre and top-10 movies (min 50 ratings)
- **Load**: writes staging and mart tables to SQLite

## Tech stack
Python · pandas · Apache Airflow · SQLite · SQL · Git

## Project structure
```
movielens-etl/
├── dags/
│   └── movielens_dag.py      # Airflow DAG
├── utils/
│   ├── extract.py            # Download & unzip dataset
│   └── transform.py          # Clean, transform, load to DB
├── data/
│   └── raw/                  # Downloaded CSVs (git-ignored)
├── requirements.txt
├── .gitignore
└── README.md
```

## How to run locally
```bash
pip install apache-airflow pandas requests
python utils/extract.py      # download dataset
python utils/transform.py    # clean + load to DB
```

## Key concepts demonstrated
- ETL pipeline architecture (extract → validate → transform → load)
- Data cleaning with pandas (null handling, deduplication, type casting)
- Multi-value field normalization (genre explosion)
- Aggregation and mart layer creation
- Airflow DAG with task dependencies and retry logic
- Layered data model: raw → staging → mart

## Dataset
MovieLens Small — 100,836 ratings across 9,742 movies
Source: https://grouplens.org/datasets/movielens/
