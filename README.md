# Task Manager (Python + MySQL)

Konzolová aplikace pro správu úkolů s MySQL databází a základní sadou integračních testů.

---

## Aplikace umožňuje:

- přidání úkolu
- zobrazení aktivních úkolů
- změnu stavu úkolu
- odstranění úkolu
- automatické uložení dat do databáze
---

## Stavy úkolů:
- Nezahájeno
- Probíhá
- Hotovo
---

## Struktura projektu
```
src/
    db.py
    ui.py
tests/
    test_*.py
    db_funkce.py
main.py
.gitignore
requirements.txt

```

## Technologie:
- Python 3
- MySQL
- PyTest (testy)
---

## Testy
Testy jsou integrační a pracují s reálnou MySQL databází.

Spuštění testů: 
pytest
---

## Požadavky

- Python 3.10+
- MySQL Server

## Konfigurace

Před spuštěním aplikace vytvořte v adresáři src/ soubor .env s následujícím obsahem:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=Task_manager
DB_NAME_TEST=Task_manager_test
```
## Spuštění projektu:

```
pip install -r requirements.txt
python main.py
```
