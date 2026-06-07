from dotenv import load_dotenv
import os

load_dotenv()
from decode import decode_synop
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# SEARCH DATE AND SHOW AVAILABLE TIMES
@app.route("/search", methods=["POST"])
def search():

    selected_date = request.form["date"]

    # Date validation
    if selected_date < "2000-01-01" or selected_date > "2025-12-31":
        return "Date out of range. Please select a date between 2000 and 2025."

    year, month, day = selected_date.split("-")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="synopticdb"
    )

    cursor = conn.cursor()

    sql = """
    SELECT hour, minute
    FROM synopticdt
    WHERE year=%s
    AND month=%s
    AND day=%s
    ORDER BY hour
    """

    cursor.execute(sql, (year, month, day))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "times.html",
        rows=rows,
        date=selected_date
    )


# SHOW DECODED WEATHER REPORT
@app.route("/observation")
def observation():

    date = request.args.get("date")
    hour = request.args.get("hour")

    year, month, day = date.split("-")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="synopticdb"
    )

    cursor = conn.cursor()

    sql = """
    SELECT *
    FROM synopticdt
    WHERE year=%s
    AND month=%s
    AND day=%s
    AND hour=%s
    """

    cursor.execute(sql, (year, month, day, hour))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return "No observation found."

    decoded = decode_synop(
        row[1],  # station_id
        row[2],  # year
        row[3],  # month
        row[4],  # day
        row[5],  # hour
        row[6],  # minute
        row[7]   # synoptic_message
    )

    return render_template(
        "weather.html",
        data=decoded
    )


if __name__ == "__main__":
    app.run(debug=True)