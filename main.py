from api_fetcher import get_pm25_data 
from data_handler import get_exceed_pm25_data

def main():
    pm25_data = get_pm25_data()
    get_exceed_pm25_data(pm25_data)
    
if __name__ == "__main__":
    main()