import os
import sys
import requests

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from packages.utils import get_advanced_stats, advanced_stats_headers, convert_string_to_ints
from tests.test_main import test_dataframe_operations


current_dir = os.path.dirname(os.path.abspath('/Users/maukanmir/Documents/Machine-Learning/Web-Scraping-Code/Ball-Dont-Lie-API/main.py'))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, project_root)

dotenv_path = ("/Users/maukanmir/Documents/Machine-Learning/Web-Scraping-Code/Ball-Dont-Lie-API/main.py")
load_dotenv(dotenv_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
TABLE_NAME = "Advanced_Stats"

DB_USER = os.getenv("DB_USER")

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')


years = [str(year) for year in range(1980, 2025)]

all_data= pd.DataFrame()
for year in years:
  base_url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
  response = requests.get(base_url)
  soup = BeautifulSoup(response.text, "html.parser")
  try:
    year = int(year)
    rows = get_advanced_stats(soup)
    adjusted_headers = advanced_stats_headers()
    df = pd.DataFrame(rows, columns=adjusted_headers)
    df = convert_string_to_ints(df, year)
    all_data = pd.concat([all_data, df])
  except Exception as error:
    print(f" The error is {error}")
    
    

try:
    all_data.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
    print("Data successfully written to the database.")
except Exception as e:
    print(f"Database operation failed. Error: {e}")
    

all_data.to_csv("advanced_stats.csv", index=False)

# Run Tests for dataframe operations
test_dataframe_operations(all_data)
