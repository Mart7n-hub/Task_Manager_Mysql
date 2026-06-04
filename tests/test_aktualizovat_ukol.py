from tests.db_funkce import pripojeni_db
from src.db import ulozit_ukol 
from src.ui import aktualizovat_ukol_logika

# Pozitivní test na funkci aktualizovat úkol
def test_update_task_positive():
    """Testuje pozitivní aktualizaci úkolu na nový stav."""
    gen = pripojeni_db()
    conn = next(gen)
    try:
        ulozit_ukol(conn, "cvicit", "behat")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("cvicit",))
        ukol = cursor.fetchone()

        result = aktualizovat_ukol_logika(conn, ukol[0], "2")
        assert result == "Stav úkolu byl aktualizován", f"Očekávalo se 'Stav úkolu byl aktualizován', ale vrátila: {result}"

        cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol[0],))
        updated = cursor.fetchone()
        assert updated[0] == "Hotovo", f"Stav není Hotovo: {updated}"

        cursor.close()

    finally:    
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ukoly WHERE nazev = %s", ("cvicit",))
        conn.commit()
        cursor.close()
        next(gen, None)

# Negativní test na funkci aktualizovat úkol
def test_update_task_negative():
    """Testuje negativní aktualizaci s neplatným stavem."""
    gen = pripojeni_db()
    conn = next(gen)
    try:
        ulozit_ukol(conn, "cvicit_test_1234", "behat")

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("cvicit_test_1234",))
        ukol = cursor.fetchone()

        result = aktualizovat_ukol_logika(conn, ukol[0], "")

        assert result == "Neplatná volba", f"Očekávalo se 'Neplatná volba', ale vrátila: {result}"

        cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol[0],))
        updated = cursor.fetchone()

        assert updated[0] == "Nezahájeno", f"Stav se neměl změnit: {updated}"

        cursor.close()

    finally:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ukoly WHERE nazev = %s", ("cvicit_test_1234",))
        conn.commit()
        cursor.close()
        next(gen, None)



