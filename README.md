# Artificial Non Intelligence

<img src=/images/Cover_photo_Artifical_NonIntelligence.png>

A deep learning generated web game to raise awareness about AI and trolls.
This repository contains the API and the data analysis dashboard.

For the frontend, check the [dedicated frontend repo](https://github.com/bolinocroustibat/artificial-non-intelligence-frontend).


## Requirements

- [Docker](https://www.docker.com/) and Docker Compose (for running the application)
- [uv](https://github.com/astral/uv) package manager (optional, only for development)


## Internal Dependencies

These dependencies are automatically handled by Docker:
- [Python 3.13](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) with [Uvicorn](https://www.uvicorn.org/)/[Gunicorn](https://gunicorn.org/) workers
- [Streamlit](https://streamlit.io/) for the data analysis dashboard
- [PostgreSQL 18](https://www.postgresql.org/)
- [uv](https://github.com/astral/uv) package manager


## Running with Docker (recommended)

1. Create a `.env` file in the root directory with the following variables:
```bash
ENVIRONMENT=local
APP_PORT=8000
DATA_PORT=8501
POSTGRES_PORT=5432
POSTGRES_DB=artificial-non-intelligence
SENTRY_DSN=https://abc123@abc123.ingest.sentry.io/abc123
ORIGINS=http://localhost:8888,https://artificial-non-intelligence.netlify.app
```

`POSTGRES_PORT` is the port published on your machine. Inside Compose, both apps talk to Postgres on port 5432.

2. Build and start the containers:
```bash
docker compose up --build
```

The API will be available at `http://localhost:8000` (or whichever port you specified in `APP_PORT`).

The data analysis dashboard will be available at `http://localhost:8501` (or whichever port you specified in `DATA_PORT`).

### Container Registry

Images are built and pushed to GitHub Container Registry on each tag release.

API:
```
ghcr.io/bolinocroustibat/artificial-non-intelligence-backend/api
```

Data analysis:
```
ghcr.io/bolinocroustibat/artificial-non-intelligence-backend/data-analysis
```

Available tags:
- `latest`: Latest stable release
- `x.y.z`: Specific version releases


## API

### Run locally (without Docker)

1. Create a `.env` file as described above

2. Create a virtual environment and install dependencies:
```bash
cd api
uv sync
```

3. Start the development server:
```bash
uv run uvicorn main:app --reload
```

### Endpoints

- `/docs`: Documentation of the API in Swagger format
- `/redoc`: Documentation of the API in Redoc format
- `/sessions`: POST a new session id (see `/docs` for full documentation of this endpoint)
- `/questions`: GET a random question (see `/docs` for full documentation of this endpoint)
- `/answers`: POST - post the user's answer (see `/docs` for full documentation of this endpoint)


## Data analysis

The Streamlit dashboard reads the same Postgres database as the API and shows live game stats.

### Run locally (without Docker)

```bash
cd data-analysis
uv sync
uv run streamlit run app.py
```

### Notebooks

These notebooks contain the data analysis and processing work for this project, including exploratory data analysis of tweets, text generation, fake tweets, and a comparison of models that try to detect fake tweets.

- [Exploratory Data Analysis & Text Generation for Fake Tweets](https://colab.research.google.com/drive/1ZcTjCIe_RXHtVwk9v_z5SlwRmfdnEBfM?usp=sharing)
- [Model Comparison & Selection to represent AI Player](https://colab.research.google.com/drive/1INR2W0NlG5qYsan94eS-hUvSOmzBO38O?usp=sharing)

Preliminary R&D notebooks:

- [R&D-A](https://colab.research.google.com/drive/1pjQPQVu6jJOYleQ1VoCv_kRtPeVgc3NR)
- [R&D-GPT2 Primer Text Approach](https://colab.research.google.com/drive/1NHUtwSCIZSj4I8q8KmLBY3SKtP6mTEDB)
- [R&D-RNN Text Generation](https://colab.research.google.com/drive/1Wm9Go9oA6_wQz5gGinOfYJxkUWulvXjL)
- [R&D-Template](https://colab.research.google.com/drive/1FevBBLTL4EByWy49a-EUx5fHmr_z6I2M)
- [R&D-GPT2 Resources](https://colab.research.google.com/drive/1PTbX8Ncl-OiZgqut6X06a4yKZ2roGItF?usp=sharing)

### Data files

JSON and CSV files from Kaggle and from those notebooks are in `data-analysis/data`.

### Import script

`data-analysis/scripts/import_json.py` can load those JSON files into the database. It still writes to an old `comments` table, and Compose does not run it.

### Comment crawlers

Crawlers live in `data-analysis/scraper`. They collect comments from websites into a SQLite database, use Peewee, and still need to be adapted to the current database.

From the `data-analysis` directory:

```bash
uv run ./scraper/crawl.py figaro
```


## Exporting dependencies

From `api` or from `data-analysis`:

```bash
uv export --no-dev --format requirements-txt > requirements.txt
```
