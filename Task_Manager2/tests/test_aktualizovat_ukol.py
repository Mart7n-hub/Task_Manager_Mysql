from src.main import aktualizovat_ukol_logika, ulozit_ukol
from tests.db_funkce import pripojeni_db

# Pozitivní test na funkci aktualizovat úkol
def test_update_task_positive():
    """Testuje pozitivní přidání úkolů a jeho následnou aktualizaci na nový úkol."""
    gen = pripojeni_db()
    conn = next(gen)
    try:
        ulozit_ukol(conn, "cvicit", "behat")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("cvicit",))
        ukol = cursor.fetchone()

        result = aktualizovat_ukol_logika(conn, ukol[0], "Hotovo")
        assert result == True, f"Chyba ve vysledku> {result}"

        cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol[0],))
        updated = cursor.fetchone()
        assert updated[0] == "Hotovo", f"Stav v databázi není Hotovo, ale: {updated}"

        cursor.close()

    finally:    
        next(gen, None)

# Negativní test na funkci aktualizovat úkol
def test_update_task_negative():
    """Testuje pozitivni přidání úkolů a negativni aktualizaci na nový úkol."""
    gen = pripojeni_db()
    conn = next(gen)
    try:
        ulozit_ukol(conn, "cvicit", "behat")

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("cvicit",))
        ukol = cursor.fetchone()

        result = aktualizovat_ukol_logika(conn, ukol[0], "")

        assert result is False, f"Chyba ve vysledku: {result}"

        cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol[0],))
        updated = cursor.fetchone()

        assert updated[0] == "behat", f"Stav v databázi se neměl změnit, ale je: {updated}"

        cursor.close()

    finally:    
        next(gen, None)



