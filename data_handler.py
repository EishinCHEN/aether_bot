import pandas as pd
from datetime import datetime, timezone

# 取得最近時間的pm2.5資料
def get_latest_pm25_data(df_data):
    # 檢查空值
    if df_data.empty:
        print("傳入資料為空")
        return df_data
    # 檢查欄位
    if "pm25" not in df_data.columns:
        print("資料未包含pm2.5欄位")
        return df_data
    
    # 型別轉換
    df_data["pm25"] = pd.to_numeric(df_data["pm25"], errors="coerce")
    df_data["datacreationdate"] = pd.to_datetime(df_data["datacreationdate"], errors="coerce")
    # 加入時區
    df_data["datacreationdate"] = df_data["datacreationdate"].dt.tz_localize("Asia/Taipei", ambiguous='NaT', nonexistent='shift_forward')
    
    # 移除空值
    df_data = df_data.dropna(subset=["pm25", "datacreationdate"]).copy()
    
    # 計算相同時區內最近時間（不論正負值）
    now = datetime.now(timezone.utc)
    df_data["time_diff"] = (df_data["datacreationdate"].dt.tz_convert("UTC") - now).abs() 
    min_time_diff = df_data["time_diff"].min()
    lastest_data = df_data.loc[df_data["time_diff"] == min_time_diff]

    return lastest_data

# 擷取pm2.5濃度高於35的資料
def extract_exceed_pm25_data(pm25_df):
    return pm25_df[pm25_df["pm25"] > 35]

# 合併觀測站與PM2.5資料
def merge_site_and_pm25(pm25_dataframe, lng_lat_dataframe):
    pm25_dataframe = pm25_dataframe.rename(columns={"site":"sitename"})
    result = pd.merge(pm25_dataframe, lng_lat_dataframe, on = "sitename")
    result = result.drop(columns=["county_y"])
    result = result.rename(columns={"county_x":"county"})
    return result