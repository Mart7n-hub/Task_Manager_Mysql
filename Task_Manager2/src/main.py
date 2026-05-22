import mysql.connector

# Funkce, která slouží pro kontrolu zapojení do databáze
def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1111",
            database="Task_manager"
        )
        print("Connected")
        return conn

    except mysql.connector.Error as err:
        print(f"Chyba připojení: {err}")
        return None
    
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

# Funkce, která zobrazí seznam s úkoly
def zobrazit_ukoly(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM ukoly WHERE stav = 'Nezahájeno' OR stav = 'Probíhá' ")
        result = cursor.fetchall()
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


def pridat_ukol(conn):
    nazev_ukolu = input("Zadej název úkolu: ")
    popis_ukolu = input("Zadej popis úkolu: ")

    vysledek = ulozit_ukol(conn, nazev_ukolu, popis_ukolu)

    print(vysledek)

def aktualizovat_ukol_logika(conn, id_ukolu, volba_stavu):
    if volba_stavu == "1":
        novy_stav = "Probíhá"
    elif volba_stavu == "2":
        novy_stav = "Hotovo"
    else:
        return "Neplatná volba"

    if not existuje_ukol(conn, id_ukolu):
        return "Úkol neexistuje"

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

    potvrzeni = input("Opravdu chceš smazat? (ano/ne): ").lower()

    vysledek = odstranit_ukol_logika(conn, id_ukolu, potvrzeni)
    print(vysledek)

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

if __name__ == "__main__":
    conn = pripojeni_db()

    if conn:
        vytvoreni_tabulky(conn)
        hlavni_menu(conn)
        conn.close()
    else:
        print("Program nelze spustit - DB nefunguje")