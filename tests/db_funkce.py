import mysql.connector
from mysql.connector import Error
import os
from src.db import vytvoreni_tabulky
from dotenv import load_dotenv

load_dotenv()

# Funkce pro připojení do databáze a uzavření připojení
def pripojeni_db():
    connection = None
    try:
        db_conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        db_name = os.getenv("DB_NAME_TEST")

        cursor = db_conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
        db_conn.close()

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME_TEST")  
        )

        print("Připojeno k testovací databázi")

        vytvoreni_tabulky(connection)

        yield connection
        
    except Error as err:
        print(f" Chyba připojení: {err}")
        yield None
        
    finally:
        if connection and connection.is_connected():
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM ukoly")  
                connection.commit()
                cursor.close()
                print(" Testovací data vymazána")
            except Error as err:
                print(f" Chyba při čištění: {err}")
            finally:
                connection.close()
                print(" Odpojeno od databáze")
    

    