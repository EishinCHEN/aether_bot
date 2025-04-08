import pandas as pd
from datetime import date, datetime, timedelta

# 取得最近時間內pm2.5濃度高於35的資料
def get_exceed_pm25_data(df_data):
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

    # 移除空值
    df_data = df_data.dropna(subset=["pm25", "datacreationdate"]).copy()
    
    # 計算最近時間（不論正負值）
    now = datetime.now()
    df_data["time_diff"] = (df_data["datacreationdate"] - now).abs() 
    min_time_diff = df_data["time_diff"].min()
    lastest_data = df_data.loc[df_data["time_diff"] == min_time_diff]
    
    return lastest_data[lastest_data["pm25"] > 35]