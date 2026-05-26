import requests
import pandas as pd

resp = requests.get("https://data.cityofnewyork.us/resource/5hjv-bjbv.json?$limit=5")
df = pd.DataFrame(resp.json())
print(df.columns.tolist())
print(df.head())
