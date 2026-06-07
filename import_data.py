import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Karthika141120@",
    database="synopticdb"
)

cursor = conn.cursor()

# Open TXT file
with open(
    "Synops_43150_2000010100_202512312100.txt",
    "r",
    encoding="utf-8"
) as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        parts = line.split(",")

        station_id = parts[0]
        year = int(parts[1])
        month = int(parts[2])
        day = int(parts[3])
        hour = int(parts[4])
        minute = int(parts[5])

        synoptic_message = ",".join(parts[6:])

        sql = """
        INSERT INTO synopticdt
        (
            station_id,
            year,
            month,
            day,
            hour,
            minute,
            synoptic_message
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            station_id,
            year,
            month,
            day,
            hour,
            minute,
            synoptic_message
        )

        cursor.execute(sql, values)

conn.commit()

print("Data Imported Successfully!")

cursor.close()
conn.close()