import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

# Funkce, která slouží pro kontrolu zapojení do databáze
def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("Connected")
        return conn

    except mysql.connector.Error as err:
        print(f"Chyba připojení: {err}")
        return None
    
# Funkce, která vytvoří databázi, pokud neexistuje
def vytvorit_databazi():
    db_name = os.getenv("DB_NAME", "Task_manager")

    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "")
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Databáze '{db_name}' připravena.")
        cursor.close()
        conn.close()
        
    except Error as err:
        print(f"Chyba při vytváření databáze: {err}")
        return False
    
    return True

# Funkce pro vytvoření tabulky
def vytvoreni_tabulky(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(100),
                popis VARCHAR(200),
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
                datum_vytvoreni DATE DEFAULT (CURRENT_DATE)
            )
        """)
        conn.commit()
        print("Tabulka 'ukoly' připravena.")

    except mysql.connector.Error as err:
        print(f"Chyba při vytváření tabulky: {err}")
    
    finally:
        cursor.close()

# Funkce, která slouží pro přidání úkolů
def ulozit_ukol(conn, nazev_ukolu, popis_ukolu):
    cursor = conn.cursor()

    try:
        if not nazev_ukolu.strip() or not popis_ukolu.strip():
            return "Název i popis musí být vyplněný"

        sql = """
        INSERT INTO ukoly (nazev, popis)
        VALUES (%s, %s)
        """

        hodnoty = (nazev_ukolu, popis_ukolu)

        cursor.execute(sql, hodnoty)
        conn.commit()

        return "Záznam byl uložen do databáze."

    except mysql.connector.Error as err:
        return f"Chyba při vkládání dat: {err}"

    finally:
        cursor.close()

def ziskat_ukoly(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nazev, stav FROM ukoly")
        return cursor.fetchall()
    finally:
        cursor.close()

def existuje_ukol(conn, id_ukolu):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM ukoly WHERE id = %s", (id_ukolu,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()


def zmenit_stav_ukolu(conn, id_ukolu, stav):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE ukoly SET stav = %s WHERE id = %s",
            (stav, id_ukolu)
        )
        conn.commit()
    finally:
        cursor.close()

def smazat_ukol_db(conn, id_ukolu):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
        conn.commit()
    finally:
        cursor.close()
