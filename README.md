Elections Scraper (PS 2017)

Skript stahuje výsledky voleb do Poslanecké sněmovny ČR 2017 pro zadaný výběr a ukládá je do CSV souboru.

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

Příkad vystupu tabulky KV_volby.csv

| Municipality Code | Municipality Name   | Voters | Envelopes | Valid Votes | Občanská demokratická strana | Řád národa - Vlastenecká unie | Česká str.sociálně demokrat. | STAROSTOVÉ A NEZÁVISLÍ | Komunistická str.Čech a Moravy | Strana zelených | ROZUMNÍ-stop migraci,diktát.EU | Strana svobodných občanů | Blok proti islam.-Obran.domova | Občanská demokratická aliance | Česká pirátská strana | Referendum o Evropské unii | TOP 09 | ANO 2011 | SPR-Republ.str.Čsl. M.Sládka | Křesť.demokr.unie-Čs.str.lid. | REALISTÉ | SPORTOVCI | Dělnic.str.sociální spravedl. | Svob.a př.dem.-T.Okamura (SPD) | Strana Práv Občanů |
|------------------:|:--------------------|-------:|----------:|------------:|-----------------------------:|------------------------------:|-----------------------------:|-----------------------:|-------------------------------:|----------------:|-------------------------------:|-------------------------:|-------------------------------:|------------------------------:|----------------------:|---------------------------:|-------:|---------:|-----------------------------:|------------------------------:|---------:|----------:|-----------------------------:|-------------------------------:|-------------------:|
| 554979            | Abertamy            |    795 |       366 |         366 |                           39 |                             2 |                           32 |                     29 |                             24 |               6 |                             12 |                        7 |                              0 |                             1 |                    36 |                          1 |     19 |       96 |                            0 |                            11 |        0 |         0 |                             5 |                             44 |                  2 |
| 538001            | Andělská Hora       |    269 |       188 |         188 |                           17 |                             0 |                            8 |                      6 |                             13 |               2 |                              1 |                        0 |                              1 |                             0 |                    18 |                          0 |     16 |       70 |                            0 |                             2 |        0 |         0 |                             1 |                             30 |                  3 |
| 554995            | Bečov nad Teplou    |    779 |       440 |         437 |                           32 |                             9 |                           21 |                     25 |                             35 |               0 |                              4 |                        6 |                              1 |                             0 |                    35 |                          0 |     12 |      154 |                            0 |                            53 |        4 |         1 |                             2 |                             42 |                  1 |
| 555029            | Bochov              |   1598 |       826 |         819 |                           70 |                            11 |                           83 |                     31 |                             94 |               7 |                              9 |                        6 |                              0 |                             2 |                    57 |                          2 |     33 |      257 |                            1 |                            30 |        2 |         3 |                             2 |                            116 |                  3 |
| 506486            | Boží Dar            |    232 |       172 |         169 |                           29 |                             1 |                            6 |                     20 |                              2 |               3 |                              3 |                        2 |                              0 |                             1 |                    22 |                          1 |     21 |       40 |                            0 |                             4 |        2 |         2 |                             0 |                              8 |                  2 |

