from src.db import vytvorit_databazi, pripojeni_db, vytvoreni_tabulky
from src.ui import hlavni_menu


if __name__ == "__main__":
    if vytvorit_databazi():
        conn = pripojeni_db()

        if conn:
            vytvoreni_tabulky(conn)
            hlavni_menu(conn)
            conn.close()
        else:
            print("Program nelze spustit - DB nefunguje")
    else:
        print("Program nelze spustit - databazi se nepodařilo vytvořit")