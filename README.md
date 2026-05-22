# Task Manager (Python + MySQL)
Konzolová aplikace pro správu úkolů s MySQL databází a základní sadou integračních testů.

## Aplikace umožňuje:
- přidání úkolu
- zobrazení aktivních úkolů
- změnu stavu úkolu
- odstranění úkolu
- automatické uložení dat do databáze

## Stavy úkolů:
- Nezahájeno
- Probíhá
- Hotovo

## Struktura projektu
src/
    main.py

tests/
    test_*.py
    db_funkce.py

## Technologie:
- Python 3
- MySQL
- PyTest (testy)

## Testy
Testy jsou integrační a pracují s reálnou MySQL databází.

Spuštění testů: pytest

## Spuštění projektu:
pip install -r requirements.txt

python src/main.py
