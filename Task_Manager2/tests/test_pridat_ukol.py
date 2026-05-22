from src.main import ulozit_ukol
from tests.db_funkce import pripojeni_db

# Pozitivní test na funkci přidat úkol
def test_add_task_positive():
    """Testuje pozitivní přidání úkolů."""
    gen = pripojeni_db()
    conn = next(gen)
    try:
        result = ulozit_ukol(conn, "cvicit", "behat")
        assert result == "Záznam byl uložen do databáze.", f"Pokud neni true result je:{result}"
    finally:    
        next(gen, None)


# Negativní test na funkci přidat úkol
def test_add_task_negative():
    """Testuje negativní přidání úkolů."""
    gen = pripojeni_db()
    conn = next(gen)
    try:
        result = ulozit_ukol(conn, "", "")
        assert result == "Název i popis musí být vyplněný", f"Pokud neni false result je:{result}"
    finally:
        next(gen, None)
