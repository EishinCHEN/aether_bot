from api_fetcher import get_pm25_data, get_site_information
from data_handler import get_latest_pm25_data, extract_exceed_pm25_data, merge_site_and_pm25
from chart_generator import genarate_pm25_map, generate_charts,generate_pm25_trend_by_site, generate_pm25_trend_by_county, generate_average_bar_chart_by_county
from line_notifier import send_pm25_flex_message

def main():
    # 取得 openAPI PM2.5觀測紀錄
    pm25_data = get_pm25_data()
    # 取得 openAPI 觀測站資訊
    site_information = get_site_information()
    # 生成地圖
    latest_pm25_data = get_latest_pm25_data(pm25_data)
    genarate_pm25_map(latest_pm25_data, site_information)
    # 生成各區圖表
    concated_data = merge_site_and_pm25(pm25_data, site_information)
    generate_charts(concated_data)
    # 傳送超標通知
    exceed_pm25_data = extract_exceed_pm25_data(latest_pm25_data)
    send_pm25_flex_message(exceed_pm25_data)
    
if __name__ == "__main__":
    main()