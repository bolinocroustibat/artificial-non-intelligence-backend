import os

import matplotlib.pyplot as plt
import pandas as pd
import psycopg
import seaborn as sns
import sentry_sdk
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "unknown")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB")
SENTRY_DSN = os.getenv("SENTRY_DSN")

if ENVIRONMENT != "local":
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        # release=f"{APP_NAME}@{VERSION}",
        traces_sample_rate=1.0,
        # Experimental profiling
        _experiments={
            "profiles_sample_rate": 1.0,
        },
    )

st.set_page_config(
    page_title="Artificial Non Intelligence - Live Data Analysis",
    page_icon="https://artificial-non-intelligence.herokuapp.com/style/favicon.ico",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Artificial Non Intelligence - Live Data Analysis")

connection = psycopg.connect(
    host=POSTGRES_HOST if POSTGRES_HOST else None,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER if POSTGRES_USER else None,
    password=POSTGRES_PASSWORD if POSTGRES_PASSWORD else None,
)

with connection:
    cursor = connection.cursor()

    # Get the number of scores and the max
    query: str = "SELECT MAX(score), count(*) AS s FROM sessions;"
    cursor.execute(query)
    sessions_count = cursor.fetchone()

    # Get the number of questions
    query: str = "SELECT real, count(*) AS a FROM questions GROUP by real;"
    cursor.execute(query)
    comments_count = cursor.fetchall()

    # Total answers in the table (may include orphaned rows if questions were removed)
    query: str = "SELECT count(*) FROM answers;"
    cursor.execute(query)
    total_answers_count: int = cursor.fetchone()[0]

    # Answers joined with questions — used for accuracy (excludes orphans)
    query: str = """
    SELECT
        questions.id,
        questions.content,
        questions.real,
        answers.answer,
        count(*) AS count
    FROM
        questions
        INNER JOIN answers ON questions.id = answers.question_id
    GROUP BY
        questions.id,
        questions.content,
        questions.real,
        answers.answer;
    """
    cursor.execute(query)
    answers = cursor.fetchall()
    cursor.close()

st.markdown("<h2>Number of games played (sessions)</h2>", unsafe_allow_html=True)
st.write(sessions_count[1])

st.markdown("<h2>Number of answers</h2>", unsafe_allow_html=True)
st.write(total_answers_count)

df = pd.DataFrame(answers, columns=["id", "content", "real", "answer", "count"])
analyzed_answers_count: int = int(df["count"].sum()) if not df.empty else 0

if analyzed_answers_count != total_answers_count:
    st.warning(
        f"{total_answers_count - analyzed_answers_count} answer(s) could not be "
        "matched to an existing question and were excluded from accuracy."
    )

# Count total number of human right guesses
right_guesses: int = 0
wrong_guesses: int = 0
for i in df.index:
    if df["real"][i] == df["answer"][i]:
        right_guesses += df["count"][i]
    else:
        wrong_guesses += df["count"][i]

accuracy: float = (
    round(right_guesses / analyzed_answers_count, 4) if analyzed_answers_count else 0.0
)

st.markdown("<h2>Current players accuracy</h2>", unsafe_allow_html=True)
st.write(accuracy)

fig, ax = plt.subplots()
sns.barplot(x=["Right guesses", "Wrong guesses"], y=[right_guesses, wrong_guesses], ax=ax)
st.pyplot(fig)

# st.markdown("<h2>Easiest question</h2>", unsafe_allow_html=True)
# st.write(
#     f'{best_comment[0]}: "{best_comment[1]}" ({best_comment[2]} right answers, real={best_comment[3]})'
# )

# st.markdown("<h2>Most difficult question</h2>", unsafe_allow_html=True)
# st.write(
#     f'{worst_comment[0]}: "{worst_comment[1]}" ({worst_comment[2]} wrong answers, real={worst_comment[3]})'
# )

st.markdown("<h2>Best score</h2>", unsafe_allow_html=True)
st.write(sessions_count[0])

st.markdown("<h2>Current dataset</h2>", unsafe_allow_html=True)
total_comments_count: int = sum(row[1] for row in comments_count)
st.write(f"Number of questions in the database: {total_comments_count}")
fig2, ax2 = plt.subplots()
sns.barplot(x=["AI", "Real"], y=[comments_count[0][1], comments_count[1][1]], ax=ax2)
st.pyplot(fig2)
