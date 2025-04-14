import folium
from branca.element import Template, MacroElement
import matplotlib.pylab as plt
import seaborn as sns
import platform
from data_handler import merge_site_and_pm25

# 產生PM2.5地圖
def genarate_pm25_map(pm25_dataframe, lng_lat_dataframe):
    # 合併＆整理資料
    pm25_dataframe = pm25_dataframe.dropna(subset=["pm25"])
    pm25_dataframe["datacreationdate"] = pm25_dataframe["datacreationdate"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df = merge_site_and_pm25(pm25_dataframe, lng_lat_dataframe)

    # 建立地圖物件
    map = folium.Map(location=[23.7, 121], zoom_start=7)

    # 加入觀測站圓點標示
    for _, row in df.iterrows():
        color = get_pm25_map_color(row["pm25"])
        popup_html = f"""
<div style="
    font-family: 'Arial', sans-serif;
    font-size: 14px;
    line-height: 1.6;
    padding: 10px 12px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
    color: #222;
    width: 220px;
">
    📍 <strong>{row['sitename']}</strong><br>
    PM2.5：{row['pm25']} μg/m³<br>
    縣市：{row['county']}<br>
    {row['datacreationdate']} 更新

    <div style="margin-top: 12px;">
        <button onclick="window.parent.postMessage({{ county: '{row['county']}', site: '{row['siteengname']}' }}, '*')" style="
            padding: 6px 12px;
            background-color: #444;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-family: 'Arial', sans-serif;
        ">
            查看 {row['county']} 圖表
        </button>
    </div>
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
<div id="legendToggleWrapper" style="position: fixed; bottom: 20px; left: 20px; z-index:9999;">
  <!-- 按鈕 -->
  <button onclick="toggleLegend()" id="legendButton" style="
      padding: 6px 12px;
      background-color: #444;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin-bottom: 8px;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 6px;
  ">
      <span id="legendButtonText">顯示圖例</span>
      <span id="legendArrow">▼</span>
  </button>

  <!-- 圖例本體 -->
  <div id="legendBox" style="
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.5s ease, padding 0.5s ease;
      background-color: white;
      border-radius: 12px;
      box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
      padding: 0 20px;
      font-size: 14px;
      font-family: 'Arial', sans-serif;
      line-height: 1.8;
      color: #333;
      width: 200px;
  ">
      <div id="legendContent" style="padding: 16px 0;">
          <div style="font-weight: bold; margin-bottom: 8px;">PM2.5 濃度指標</div>
          <div><span style="display:inline-block;width:14px;height:14px;background:#00e400;border-radius:3px;margin-right:8px;"></span>0-15 良好</div>
          <div><span style="display:inline-block;width:14px;height:14px;background:#ffff00;border-radius:3px;margin-right:8px;"></span>16-35 普通</div>
          <div><span style="display:inline-block;width:14px;height:14px;background:#ff7e00;border-radius:3px;margin-right:8px;"></span>36-54 敏感族群不健康</div>
          <div><span style="display:inline-block;width:14px;height:14px;background:#ff0000;border-radius:3px;margin-right:8px;"></span>55-150 不健康</div>
          <div><span style="display:inline-block;width:14px;height:14px;background:#8f3f97;border-radius:3px;margin-right:8px;"></span>151+ 非常不健康</div>
          <div><span style="display:inline-block;width:14px;height:14px;background:#aaaaaa;border-radius:3px;margin-right:8px;"></span>無資料</div>
      </div>
  </div>
</div>

<script>
  let isLegendVisible = false;

  function toggleLegend() {
    const legendBox = document.getElementById('legendBox');
    const buttonText = document.getElementById('legendButtonText');
    const arrow = document.getElementById('legendArrow');

    if (!isLegendVisible) {
      legendBox.style.maxHeight = "500px";
      legendBox.style.paddingTop = "16px";
      legendBox.style.paddingBottom = "16px";
      buttonText.innerText = "隱藏圖例";
      arrow.innerText = "▲";
    } else {
      legendBox.style.maxHeight = "0";
      legendBox.style.paddingTop = "0";
      legendBox.style.paddingBottom = "0";
      buttonText.innerText = "顯示圖例";
      arrow.innerText = "▼";
    }

    isLegendVisible = !isLegendVisible;
  }
</script>
{% endmacro %}
"""

    macro = MacroElement()
    macro._template = Template(legend)
    map.get_root().add_child(macro)

    # 儲存為 HTML
    map.save("templates/map.html")

# 標示pm2.5濃度顏色
def get_pm25_map_color(pm25_value):
    try:
        value = float(pm25_value)
        if value <= 15: return "#00e400"     # 綠色：良好
        elif value <= 35: return "#ffff00"   # 黃色：普通
        elif value <= 54: return "#ff7e00"   # 橘色：對敏感族群不健康
        elif value <= 150: return "#ff0000"  # 紅色：不健康
        else: return "#8f3f97"               # 紫色：非常不健康
    except:
        return "#aaaaaa"                     # 無資料：灰色

# 產生各地區圖表
def generate_charts(concated_df):
    site_eng_names = concated_df["siteengname"].dropna().unique()
    county_names = concated_df["county"].dropna().unique()

    for site in site_eng_names:
        generate_pm25_trend_by_site(concated_df, site)
    for county in county_names:
        generate_pm25_trend_by_county(concated_df, county)
        generate_average_bar_chart_by_county(concated_df, county)

# 製作指定觀測站PM2.5濃度折線圖
def generate_pm25_trend_by_site(df_data, site_eng_name):
    # 指定篩選觀測站
    df_site = df_data[df_data["siteengname"] == site_eng_name].copy()
    site_ch_name = df_site["sitename"].iloc[0]

    # 排序
    df_site.sort_values("datacreationdate", inplace=True)
    
    # 產生折線圖
    set_chinese_font()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_site, x='datacreationdate', y='pm25', marker='o')
    plt.title(f"{site_ch_name}觀測站 12小時 PM2.5 濃度紀錄")
    plt.xlabel("月-日 時")
    plt.ylabel("PM2.5 (μg/m³)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"./charts/site_line_charts/{site_eng_name}_site_trend.png")

# 製作指定行政區PM2.5濃度折線圖
def generate_pm25_trend_by_county(df_data, county_name):
    df_county = df_data[df_data["county"] == county_name].copy()
    df_county.sort_values(["sitename", "datacreationdate"], inplace=True)
    
    # 產生折線圖
    set_chinese_font() 
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=df_county, x='datacreationdate', y='pm25', hue='sitename', marker='o')
    plt.title(f"{county_name} 12小時內 PM2.5 濃度紀錄")
    plt.xlabel("月-日 時")
    plt.ylabel("PM2.5 (μg/m³)")
    plt.legend(title='site', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"./charts/county_line_charts/{county_name}_trend.png")

# 製作指定行政區PM2.5平均指數長條圖
def generate_average_bar_chart_by_county(df_data, county_name):
    county_df = df_data[df_data["county"] == county_name].copy()
    average_by_county = county_df.groupby("sitename")["pm25"].mean().sort_values(ascending=True).reset_index()

    # 產生長條圖
    set_chinese_font()
    plt.figure(figsize=(10,6))
    ax = sns.barplot(data=average_by_county, x= "sitename", y="pm25", palette='Reds')
    
    # 生成每個柱的數值標籤
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f', label_type='edge', padding=2)
    
    plt.title(f"{county_name}平均 PM2.5 排行")
    plt.ylabel("PM2.5 平均值")
    plt.xlabel("觀測站")
    plt.tight_layout()
    plt.savefig(f"./charts/county_bar_charts/{county_name}_average_bar_chart.png")

# 顯示中文字體
def set_chinese_font():
    # 根據系統設定中文字型
    if platform.system() == 'Darwin':  # macOS
        plt.rcParams['font.family'] = 'Heiti TC'
    elif platform.system() == 'Windows':  # Windows
        plt.rcParams['font.family'] = 'Microsoft JhengHei'
    else:  # Linux 或 Colab
        plt.rcParams['font.family'] = 'Taipei Sans TC Beta'