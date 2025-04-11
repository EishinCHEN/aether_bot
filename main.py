from api_fetcher import get_pm25_data, get_site_information
from data_handler import get_latest_pm25_data, extract_exceed_pm25_data, show_pm25_map
from line_notifier import send_pm25_flex_message

def main():
    pm25_data = get_pm25_data()
    latest_pm25_data = get_latest_pm25_data(pm25_data)
    site_information = get_site_information()
    show_pm25_map(latest_pm25_data, site_information)
    exceed_pm25_data = extract_exceed_pm25_data(latest_pm25_data)
    send_pm25_flex_message(exceed_pm25_data)

if __name__ == "__main__":
    main()