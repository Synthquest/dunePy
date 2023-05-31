import requests
import pandas as pd

url = 'https://api.synthetix.io/staking-ratio'
headers = {
    'accept': 'application/json'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    # Normalize 'stakedSnx' object into separate columns since it comes in as a nested object
    stakedSnx_df = pd.json_normalize(data['stakedSnx'])
    del data['stakedSnx']  # Remove the original 'stakedSnx' object

    # Create DataFrame from the remaining data
    df = pd.DataFrame(data, index=[0])

    # Merge the DataFrames
    df = pd.concat([df, stakedSnx_df], axis=1)

    # Convert Unix timestamp to UTC
    df['timestamp_utc'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC')

    # Convert DataFrame to CSV and export as staking_ratio.csv
    df.to_csv('staking_ratio.csv', index=False)
else:
    print('Request failed with status code:', response.status_code)

