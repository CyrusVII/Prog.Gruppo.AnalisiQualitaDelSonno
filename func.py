import numpy as np
import mysql.connector as sq

def connect(db):
    df = sq.connect(
        host="localhost",
        user="root",
        password="",
        database=db,
    )
    return df
    
def data(db, feature): # recupero le professioni
    conn = connect(db)
    cursor = conn.cursor()
    try:
        query = f"SELECT DISTINCT {feature} FROM sleepdata"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        data = [r[0] for r in rows] # recupero le professioni
        arr = np.array(data, dtype="<U50").reshape(-1, 1) # crea array di tipo stringa
        return arr
    
    except Exception as e:
        print(f"Error: {e}")
        print("Error: Unable to fetch data")
    except sq.Error as e:
        print(f"Error: {e}")
        print("Error: Unable to connect to the database")
    finally:
        cursor.close()
        conn.close()
        
# group_feat è la feature da raggruppare, agg_feature è la feature da aggregare, func è la funzione di aggregazione
def data_stats(db, group_feat, agg_feature, func): # recupero le professioni e la media della qualità del sonno
    conn = connect(db)
    cursor = conn.cursor()
    try:
        query = f"SELECT {group_feat}, {func}({agg_feature}) FROM sleepdata GROUP BY {group_feat}"
        cursor.execute(query)
        data = cursor.fetchall()
        labels, values = zip(*data) # spacchetto i dati in due liste
        lbl_arr = np.array(labels, dtype="<U50").reshape(-1, 1)
        val_arr = np.array(values, dtype="float").reshape(-1, 1)
        return np.hstack((lbl_arr, val_arr)) # unisco le due liste in un array 2D

    except Exception as e:
        print(f"Error: {e}")
        print("Error: Unable to fetch data")
    except sq.Error as e:
        print(f"Error: {e}")
        print("Error: Unable to connect to the database")
    finally:
        cursor.close()
        conn.close()

def data_mean(db, group_feat, agg_feature="QualitySleep"): # recupero le professioni e la media della qualità del sonno
    return data_stats(db, group_feat, agg_feature, "AVG")

def data_std(db, group_feat, agg_feat="QualitySleep"):
    return data_stats(db, group_feat, agg_feat, "STD")

def data_var(db, group_feat, agg_feat="QualitySleep"):
    return data_stats(db, group_feat, agg_feat, "VAR")

def data_var(db, group_feat, agg_feat="QualitySleep"): # recupero le professioni e la varianza della qualità del sonno
    return data_stats(db, group_feat, agg_feat, "VARIANCE")

def data_median(db, group_feat, agg_feat="QualitySleep"):
    conn = connect(db)
    cursor = conn.cursor()
    try:
        query = f"SELECT {group_feat}, {agg_feat} FROM sleepdata"
        cursor.execute(query)
        rows = cursor.fetchall()
        groups = {}
        for grp, value in rows:
            groups.setdefault(grp, []).append(value) # raggruppo i dati in un dizionario
        items = [(grp, float(np.median(values))) for grp, values in groups.items()] # calcolo la mediana
        labels, values = zip(*items) # spacchetto i dati in due liste
        lbl_arr = np.array(labels, dtype="<U50").reshape(-1, 1)
        val_arr = np.array(values, dtype="float").reshape(-1, 1)
        return np.hstack((lbl_arr, val_arr)) # unisco le due liste in un array 2D
    except Exception as e:
        print(f"Error: {e}")
        print("Error: Unable to fetch data")
    except sq.Error as e:  
        print(f"Error: {e}")
        print("Error: Unable to connect to the database")
    finally:
        cursor.close()
        conn.close()

#print(data_median("csv_db 10", "Occupation", "QualitySleep"))

def main_menu():
    import sys
    
    db = "sleepdata"
    group_feat = input("Inserisci il nome della feature da raggruppare (es: Occupation): ")
    agg_feat = "QualitySleep"  

    while True:
        print("\n--- Menu ---")
        print("1. Mostra valori distinti della feature")
        print("2. Calcola media")
        print("3. Calcola deviazione standard")
        print("4. Calcola varianza")
        print("5. Calcola mediana")
        print("0. Esci")

        choice = input("Scegli un'opzione: ")

        match choice:
            case "1":
                arr = data(db, group_feat)
                print("\nValori distinti:")
                print(arr)

            case "2":
                arr = data_mean(db, group_feat, agg_feat)
                print("\nMedia della feature aggregata:")
                print(arr)

            case "3":
                arr = data_std(db, group_feat, agg_feat)
                print("\nDeviazione standard della feature aggregata:")
                print(arr)

            case "4":
                arr = data_var(db, group_feat, agg_feat)
                print("\nVarianza della feature aggregata:")
                print(arr)

            case "5":
                arr = data_median(db, group_feat, agg_feat)
                print("\nMediana della feature aggregata:")
                print(arr)

            case "0":
                print("Uscita dal programma.")
                sys.exit()

            case _:
                print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main_menu()