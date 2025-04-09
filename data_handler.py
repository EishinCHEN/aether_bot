import pandas as pd
from datetime import datetime
import folium
from branca.element import Template, MacroElement

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

    # 移除空值
    df_data = df_data.dropna(subset=["pm25", "datacreationdate"]).copy()
    
    # 計算最近時間（不論正負值）
    now = datetime.now()
    df_data["time_diff"] = (df_data["datacreationdate"] - now).abs() 
    min_time_diff = df_data["time_diff"].min()
    lastest_data = df_data.loc[df_data["time_diff"] == min_time_diff]
    
    return lastest_data

# 擷取pm2.5濃度高於35的資料
def extract_exceed_pm25_data(pm25_dataframe):
    return pm25_dataframe[pm25_dataframe["pm25"] > 35]

def show_pm25_map(pm25_dataframe, lng_lat_dataframe):
    # 合併＆整理資料
    pm25_dataframe = pm25_dataframe.rename(columns={"site": "sitename"})
    pm25_dataframe = pm25_dataframe.dropna(subset=["pm25"])
    df = pd.merge(pm25_dataframe, lng_lat_dataframe, on = "sitename")
    df = df.drop(columns=["county_y"])
    df = df.rename(columns={"county_x":"county"})
    print(df)

    # 建立地圖物件
    map = folium.Map(location=[23.7, 121], zoom_start=7)

    for _, row in df.iterrows():
        color = get_pm25_map_color(row["pm25"])
        popup_html = popup_html = f"""
<div style="
    font-family: 'Arial', sans-serif;
    font-size: 14px;
    line-height: 1.6;
    padding: 10px 12px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
    color: #222;
    width: 200px;
">
    📍 <strong>{row['sitename']}</strong><br>
    PM2.5：{row['pm25']} μg/m³<br>
    縣市：{row['county']}<br>
    {row['datacreationdate']} 更新
</div>
"""
        folium.CircleMarker(
            location=[row["twd97lat"], row["twd97lon"]],
            radius=9,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(map)

    # 加入圖例
    legend = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    bottom: 40px;
    left: 40px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    padding: 16px 20px;
    font-size: 14px;
    font-family: 'Arial', sans-serif;
    line-height: 1.8;
    z-index:9999;
    color: #333;
    width: 210px;
">
    <div style="font-weight: bold; margin-bottom: 8px;">PM2.5 空氣品質指標</div>
    <div><span style="display:inline-block;width:14px;height:14px;background:#00e400;border-radius:3px;margin-right:8px;"></span>0-15 良好</div>
    <div><span style="display:inline-block;width:14px;height:14px;background:#ffff00;border-radius:3px;margin-right:8px;"></span>16-35 普通</div>
    <div><span style="display:inline-block;width:14px;height:14px;background:#ff7e00;border-radius:3px;margin-right:8px;"></span>36-54 敏感族群不健康</div>
    <div><span style="display:inline-block;width:14px;height:14px;background:#ff0000;border-radius:3px;margin-right:8px;"></span>55-150 不健康</div>
    <div><span style="display:inline-block;width:14px;height:14px;background:#8f3f97;border-radius:3px;margin-right:8px;"></span>151+ 非常不健康</div>
    <div><span style="display:inline-block;width:14px;height:14px;background:#aaaaaa;border-radius:3px;margin-right:8px;"></span>無資料</div>
</div>
{% endmacro %}
"""

    macro = MacroElement()
    macro._template = Template(legend)
    map.get_root().add_child(macro)

    # 儲存為 HTML
    map.save("pm25_map.html")
    print("✅ 地圖已儲存為 pm25_map.html")

# 標示pm2.5濃度顏色
def get_pm25_map_color(pm25_value):
    try:
        value = float(pm25_value)
        if value <= 15: return "#00e400"  # 綠色：良好
        elif value <= 35: return "#ffff00"  # 黃色：普通
        elif value <= 54: return "#ff7e00"  # 橘色：對敏感族群不健康
        elif value <= 150: return "#ff0000"  # 紅色：不健康
        else: return "#8f3f97"  # 紫色：非常不健康
    except:
        return "#aaaaaa"  # 無資料：灰色