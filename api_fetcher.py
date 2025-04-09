import requests 
import pandas as pd

def get_pm25_data():
    result = requests.get("https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=4416ea29-5385-4903-b3cd-b0e97b909751").json()
    return pd.DataFrame(result["records"])

def get_site_information():
    result = requests.get("https://data.moenv.gov.tw/api/v2/aqx_p_07?api_key=4416ea29-5385-4903-b3cd-b0e97b909751").json()
    return pd.DataFrame(result["records"])