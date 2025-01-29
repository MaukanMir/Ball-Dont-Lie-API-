# Description: This file contains utility functions that are used to scrape data from basketball-reference.com
import pandas as pd

# Universal Functions

def change_to_numeric(df):
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def set_season(df, year):
    df["season"] = year
    return df


def advanced_stats_headers():
    ## Advanced Stats Exraction
    headers = [
        "Rk", "Team", "Age", "W", "L", "PW", "PL", "MOV", "SOS", "SRS",
        "ORtg", "DRtg", "NRtg", "Pace", "FTr", "3PAr", "TS%", "",
        "eFG%", "TOV%", "ORB%", "FT/FGA", "", "eFG%", "TOV%", "DRB%", "FT/FGA",
        "Arena", "Attend.", "Attend./G"
    ]

    # Higher-level headers
    offensive_four_factors = ["eFG%", "TOV%", "ORB%", "FT/FGA"]
    defensive_four_factors = ["eFG%", "TOV%", "DRB%", "FT/FGA"]

    # Modify headers by prefixing higher-level headers
    adjusted_headers = []
    offense_added, defense_added = False, False

    for header in headers:
        if header in offensive_four_factors and not offense_added:
            adjusted_headers.append(f"Offensive {header}")
            offensive_four_factors.remove(header)
        elif header in defensive_four_factors and not defense_added:
            adjusted_headers.append(f"Defensive {header}")
            if header == "FT/FGA":
                defense_added = True
        elif header == "":
            continue
        else:
            adjusted_headers.append(header)
    return adjusted_headers


def get_advanced_stats(soup, year):
    table = soup.find("table", {"id": "advanced-team"})
    rows = []
    
    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all(["th", "td"])
        formatted_cell = [cell.get_text(strip=True) for cell in cells]
        for clean_cell in formatted_cell:
            if len(clean_cell) == 0:
                formatted_cell.remove(clean_cell)
        rows.append(formatted_cell)
    adjusted_headers = advanced_stats_headers()
    df = pd.DataFrame(rows, columns=adjusted_headers)
    df = change_to_numeric(df)
    df = set_season(df, year)
    return df


def get_total_stats(soup, year):
    table = soup.find("table", {"id": "totals-team"})
    headers = [header.text for header in table.find("thead").find_all("th")]

    rows = []
    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all(["th", "td"])
        rows.append([cell.text.strip() for cell in cells])

    df = pd.DataFrame(rows, columns=headers)
    df["Team"] = df["Team"].str.replace("*", "")

    df = change_to_numeric(df)
    df = set_season(df, year)

    return df

def per_game_stats(soup, year):
    table = soup.find("table", {"id": "per_game-team"})
    headers = [th.text.strip() for th in table.find("thead").find_all("th")]

    rows = table.find("tbody").find_all("tr")

    data = []
    for row in rows:
        cells = row.find_all("td")
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers[1:])
    df = change_to_numeric(df)
    df = set_season(df, year)
    return df