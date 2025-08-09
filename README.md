Elections Scraper (PS 2017)

Skript stahuje výsledky voleb do Poslanecké sněmovny Parlamentu ČR 2017 pro zadaný výběr (seznam obcí) a ukládá je do CSV souboru.

---

Požadavky
- Python: 3.8+
- Knihovny:
  - requests
  - beautifulsoup4

---

Struktura repozitáře
| Soubor | Popis |
|--------|-------|
| main.py | Hlavní skript pro stažení a zpracování dat |
| requirements.txt | Seznam potřebných knihoven |
| README.md | Dokumentace projektu |
| output.csv | Výstupní CSV soubor (generuje se po spuštění skriptu) |

---

Instalace
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

---

Použití
python3 main.py "<URL_se_seznamem_obcí>" "<nazev_vystupniho_souboru>.csv"

---

Příklady URL
- https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xobec=0
- https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=5&xnumnuts=4102

---

Příklad spuštění
python3 main.py "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xobec=0" "KV_output.csv"

---
Formát výstupního CSV
- Oddělovač: ;
- Sloupce:
  1. Municipality Code
  2. Municipality Name
  3. Voters
  4. Envelopes
  5. Valid Votes
  6. Každá další položka = počet hlasů pro konkrétní stranu

---

Poznámky
- Skript ověřuje vstupy a bezpečně parsuje hodnoty i při drobných změnách v HTML.
- Pro jiné kraje/okresy stačí upravit URL dle uvedeného vzoru.
