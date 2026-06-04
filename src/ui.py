from src.db import ulozit_ukol, ziskat_ukoly, existuje_ukol, zmenit_stav_ukolu, smazat_ukol_db
import mysql.connector
from mysql.connector import Error

# Funkce, která zobrazí seznam s úkoly
def zobrazit_ukoly(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM ukoly WHERE stav = 'Nezahájeno' OR stav = 'Probíhá' ")
        result = cursor.fetchall()

        if not result:
            print("Žádné aktivní úkoly.")
            return

        for ukol in result:
            print(f"""
            ID: {ukol[0]}
            Název: {ukol[1]}
            Popis: {ukol[2]}
            Stav: {ukol[3]}
            """)
    except mysql.connector.Error as err:
        print(f"Chyba databáze: {err}")

    finally:
        cursor.close()


def pridat_ukol(conn):
    while True:
        nazev_ukolu = input("Zadej název úkolu: ").strip()
        
        if not nazev_ukolu:
            print("Název úkolu nesmí být prázdný. Zkus to znovu.")
            continue
        
        break
    
    while True:
        popis_ukolu = input("Zadej popis úkolu: ").strip()
        
        if not popis_ukolu:
            print("Popis úkolu nesmí být prázdný. Zkus to znovu.")
            continue
        
        break

    vysledek = ulozit_ukol(conn, nazev_ukolu, popis_ukolu)
    print(vysledek)


def aktualizovat_ukol_logika(conn, id_ukolu, volba_stavu):
    if not existuje_ukol(conn, id_ukolu):
        return "Úkol neexistuje"
    
    if volba_stavu == "1":
        novy_stav = "Probíhá"
    elif volba_stavu == "2":
        novy_stav = "Hotovo"
    else:
        return "Neplatná volba"

    zmenit_stav_ukolu(conn, id_ukolu, novy_stav)
    return "Stav úkolu byl aktualizován"

def aktualizovat_ukol(conn):
    ukoly = ziskat_ukoly(conn)

    if not ukoly:
        print("Žádné úkoly v databázi.")
        return

    for ukol in ukoly:
        print(f"ID: {ukol[0]} | Název: {ukol[1]} | Stav: {ukol[2]}")

    while True:
        try:
            id_ukolu = int(input("\nZadej ID úkolu: "))
            break
        except ValueError:
            print("ID musí být číslo.")

    print("\n1 - Probíhá")
    print("2 - Hotovo")
    volba = input("Vyber nový stav: ")

    vysledek = aktualizovat_ukol_logika(conn, id_ukolu, volba)
    print(vysledek)


def odstranit_ukol_logika(conn, id_ukolu, potvrzeni):
    if not existuje_ukol(conn, id_ukolu):
        return "Úkol neexistuje"

    if potvrzeni != "ano":
        return "Mazání zrušeno"

    smazat_ukol_db(conn, id_ukolu)
    return "Úkol byl odstraněn"

def odstranit_ukol(conn):
    ukoly = ziskat_ukoly(conn)

    if not ukoly:
        print("Žádné úkoly v databázi.")
        return

    for ukol in ukoly:
        print(f"ID: {ukol[0]} | Název: {ukol[1]} | Stav: {ukol[2]}")

    while True:
        try:
            id_ukolu = int(input("\nZadej ID úkolu ke smazání: "))
            break
        except ValueError:
            print("ID musí být číslo.")
    
    if not existuje_ukol(conn, id_ukolu):
        print("Úkol neexistuje")
        return

    potvrzeni = input("Opravdu chceš smazat? (ano/ne): ").lower()

    vysledek = odstranit_ukol_logika(conn, id_ukolu, potvrzeni)
    print(vysledek)

def hlavni_menu(conn):
    while True:
        print("\nTASK MANAGER")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        volba = input("\nVyber možnost: ")

        if volba == "1":
            pridat_ukol(conn)
        elif volba == "2":
            zobrazit_ukoly(conn)
        elif volba == "3":
            aktualizovat_ukol(conn)
        elif volba == "4":
            odstranit_ukol(conn)
        elif volba == "5":
            print("Program byl ukončen.")
            break
        else:
            print("Neplatná volba. Zkus to znovu.")