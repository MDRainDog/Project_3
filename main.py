"""
projekt_3.py: třetí projekt pro  Engeto Online Python Akademie
               Elections Scraper
author: Rostyslav Luzan
email: roluzan@email.cz

"""



import csv
import re
import sys
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE = "https://www.volby.cz/pls/ps2017nss/"
NBSP = "\xa0"


# Input validation

def validate_input() -> None:
    """Validate CLI arguments"""
    if len(sys.argv) != 3:
        sys.exit(
            "Incorrect input.\n"
            f"Usage: {sys.argv[0]} <URL> <output.csv>\n"
            "  1) URL with election results (municipality list)\n"
            "  2) Output CSV filename"
        )

    url = sys.argv[1]
    out = sys.argv[2]

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        sys.exit("Invalid URL scheme. Use http(s)://")
    if not parsed.netloc.endswith("volby.cz"):
        sys.exit("Invalid host. Expected volby.cz / www.volby.cz")
    if not parsed.path.startswith("/pls/ps2017nss/"):
        sys.exit("Invalid path. Expected '/pls/ps2017nss/'")

    if not out.lower().endswith(".csv"):
        sys.exit(f"File: {out} is not a CSV file!")

    print(f"DOWNLOADING DATA FROM URL: {url}")


# HTTP & parsing

def get_server_response(url: str) -> requests.Response:
    """Perform with basic headers, timeout, and error handling."""
    try:
        headers = {"User-Agent": "elections-scraper/0.1"}
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp
    except requests.exceptions.RequestException as exc:
        sys.exit(f"Error downloading page: {exc}")


def parse_response(response: requests.Response) -> BeautifulSoup:
    """Create BeautifulSoup from HTTP response."""
    return BeautifulSoup(response.text, "html.parser")



# Helpers (conversions/selectors)

def _to_int(text: str) -> int:
    """Convert number-like text (with NBSP and spaces) to int, empty -> 0."""
    cleaned = (text or "").replace(NBSP, "").replace(" ", "").strip()
    return int(cleaned or 0)


def _td_num_by_headers(soup: BeautifulSoup, header_id: str) -> Optional[int]:
    """Return integer from <td headers='...'> cell, or None if missing."""
    td = soup.select_one(f"td[headers='{header_id}']")
    return _to_int(td.get_text(strip=True)) if td else None


def _cell_after_label_in_same_row(
    soup: BeautifulSoup, label_regex: str
) -> Optional[int]:
    """  Fallback for pages without 'headers' attributes """
    label = soup.find(
        lambda tag: tag.name in ("th", "td")
        and re.search(label_regex, tag.get_text(strip=True), re.IGNORECASE)
    )
    if not label:
        return None

    tr = label.find_parent("tr")
    if not tr:
        return None

    seen = False
    for cell in tr.find_all(["th", "td"]):
        if cell is label:
            seen = True
            continue
        if seen and cell.name == "td":
            return _to_int(cell.get_text(strip=True))
    return None


# Resolve page type and get municipality list page (ps32)

def resolve_municipality_list(url: str) -> Tuple[str, BeautifulSoup]:
    """   Return  for the municipality LIST   """
    if "ps32" in url:
        return url, parse_response(get_server_response(url))

    soup = parse_response(get_server_response(url))
    anchor = soup.find("a", href=lambda h: h and "ps32" in h)
    if anchor and anchor.has_attr("href"):
        next_url = urljoin(BASE, anchor["href"])
        return next_url, parse_response(get_server_response(next_url))

    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    params = {
        "xjazyk": qs.get("xjazyk", ["CZ"])[0],
        "xkraj": qs.get("xkraj", [""])[0],
        "xnumnuts": qs.get("xnumnuts", [""])[0],
    }
    if not params["xkraj"] or not params["xnumnuts"]:
        sys.exit("Missing xkraj/xnumnuts to construct ps32 URL.")
    ps32_url = f"{BASE}ps32?{urlencode(params)}"
    return ps32_url, parse_response(get_server_response(ps32_url))


# Parse municipality list (ps32… page)

def get_basic_data(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract municipality stubs"""
    municipalities: List[Dict[str, Any]] = []
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        code_text = cells[0].get_text(strip=True)
        name = cells[1].get_text(strip=True)
        link_tag = cells[0].find("a")

        if not (link_tag and code_text.isdigit() and name):
            continue

        link = urljoin(BASE, link_tag["href"])
        municipalities.append({"code": code_text, "name": name, "link": link})
    return municipalities

# Parse municipality detail (robust)

def get_detailed_data(url: str) -> Dict[str, Any]:
    """    Extract per-municipality numbers """
    soup = parse_response(get_server_response(url))

    # Prefer explicit header-based cells
    voters = _td_num_by_headers(soup, "sa2")
    envelopes = _td_num_by_headers(soup, "sa3")
    valid_votes = _td_num_by_headers(soup, "sa6")

    # Fallbacks by label text (same table row)
    if voters is None:
        voters = _cell_after_label_in_same_row(soup, r"Voliči v seznamu")
    if envelopes is None:
        envelopes = _cell_after_label_in_same_row(soup, r"Vydané obálky")
    if valid_votes is None:
        valid_votes = _cell_after_label_in_same_row(soup, r"Platné hlasy")

    voters = voters or 0
    envelopes = envelopes or 0
    valid_votes = valid_votes or 0

    # Collect party rows: (name, votes)
    parties: List[Tuple[str, int]] = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 3:
            continue

        name = tds[1].get_text(strip=True)
        votes_raw = tds[2].get_text(strip=True)

        if name and re.search(r"\d", votes_raw):
            try:
                votes = _to_int(votes_raw)
            except ValueError:
                continue
            if len(name) > 1:
                parties.append((name, votes))

    return {
        "voters": voters,
        "envelopes": envelopes,
        "valid_votes": valid_votes,
        "parties": parties,
    }


# CSV writing
def create_csv(municipalities: List[Dict[str, Any]], filename: str) -> None:
    """    Write results to CSV  """
    if not municipalities:
        print("No data to save!")
        return

    header = [
        "Municipality Code",
        "Municipality Name",
        "Voters",
        "Envelopes",
        "Valid Votes",
    ]
    if municipalities and municipalities[0]["results"]["parties"]:
        header += [party for party, _ in municipalities[0]["results"]["parties"]]

    rows: List[List[Any]] = []
    for m in municipalities:
        row = [
            m["code"],
            m["name"],
            m["results"]["voters"],
            m["results"]["envelopes"],
            m["results"]["valid_votes"],
        ]
        row += [votes for _, votes in m["results"]["parties"]]
        rows.append(row)

    with open(filename, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, delimiter=";")
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Data successfully saved to {filename}")


# Entrypoint
def main() -> None:
    """CLI entrypoint."""
    validate_input()
    url = sys.argv[1]
    csv_file = sys.argv[2]

    _, soup = resolve_municipality_list(url)
    municipalities = get_basic_data(soup)

    for municipality in municipalities:
        if municipality["link"]:
            municipality["results"] = get_detailed_data(municipality["link"])
        else:
            municipality["results"] = {
                "voters": 0,
                "envelopes": 0,
                "valid_votes": 0,
                "parties": [],
            }

    create_csv(municipalities, csv_file)
    print("Done!")


if __name__ == "__main__":
    main()
