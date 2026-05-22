from src.main import ulozit_ukol, odstranit_ukol_logika
from tests.db_funkce import pripojeni_db

# Pozitivní test na funkci odstranit úkol
def test_delete_task_positive():
    """Pozitivní test na přidání úkolů a jeho následné odstranění."""
    gen = pripojeni_db()
    conn = next(gen)
    try:
        ulozit_ukol(conn, "cvicit", "behat")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("cvicit",))
        ukol = cursor.fetchone()
        id_ukolu = ukol[0]

        result = odstranit_ukol_logika(conn, id_ukolu, "ano")
        assert result == True, f"Pokud ne tak, protoze {result}"

        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        deleted = cursor.fetchone()

        assert deleted == None, f"Úkol měl být smazaný, ale pořád existuje: {deleted}"

        cursor.close()

    finally:    
        next(gen, None)


# Negativní test na funkci odstranit úkol
def test_delete_task_negative():
    """Negativní test na přidání úkolů a jeho následné odstranění."""
    gen = pripojeni_db()
    conn = next(gen)
    try:
        id_ukolu = 999

        result = odstranit_ukol_logika(conn, id_ukolu, "ano")
        assert result == False, f"Funkce měla vrátit false, ale vrátila {result}"

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        deleted = cursor.fetchone()

        assert deleted == None, f"Neexistující úkol by neměl být v databázi: {deleted}"

        cursor.close()

    finally:    
        next(gen, None)