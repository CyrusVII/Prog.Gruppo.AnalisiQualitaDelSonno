import mysql.connector
import numpy as np

def db_connection(db_name):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
        conn.close()

        myDB = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=db_name
        )
        return myDB
    except mysql.connector.Error as err:
        print("Errore:", err)
        return None

def calcola_medie_per_eta(conn):
    cursor = conn.cursor(dictionary=True)

    # Query: prendi solo i campi rilevanti
    cursor.execute("""
        SELECT Age, SleepDuration, QualitySleep FROM sleepData
    """)
    rows = cursor.fetchall()

    # Contenitori per ogni fascia
    under_34 = {"durations": [], "qualities": []}
    range_35_49 = {"durations": [], "qualities": []}
    range_50_60 = {"durations": [], "qualities": []}

    # Suddividi i dati
    for row in rows:
        age = row["Age"]
        duration = row["SleepDuration"]
        quality = row["QualitySleep"]

        if age <= 34:
            under_34["durations"].append(duration)
            under_34["qualities"].append(quality)
        elif 35 <= age <= 49:
            range_35_49["durations"].append(duration)
            range_35_49["qualities"].append(quality)
        elif 50 <= age <= 60:
            range_50_60["durations"].append(duration)
            range_50_60["qualities"].append(quality)

    # Calcolo medie
    def calc_avg(group):
        if group["durations"] and group["qualities"]:
            return {
                "avg_sleep": round(np.mean(group["durations"]), 2),
                "avg_quality": round(np.mean(group["qualities"]), 2)
            }
        else:
            return {"avg_sleep": None, "avg_quality": None}

    print("➡️ Medie Sleep Duration e Quality per fascia d'età:\n")
    print("Under 34:", calc_avg(under_34))
    print("35-49:", calc_avg(range_35_49))
    print("50-60:", calc_avg(range_50_60))

    cursor.close()

# Esecuzione
conn = db_connection("sleepdata")  
if conn:
    calcola_medie_per_eta(conn)
    conn.close()
else:
    print("Connessione al database fallita.")

