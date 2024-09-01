# Author: Nelson Chung
# Email: chihchun.chung@gmail.com
# Description: This script retrieves and processes the 7-day weather forecast for various regions in Taiwan
#              from the Taiwan Open Data API. The data is parsed and organized into a structured format
#              using pandas, and the final dataset is saved as a CSV file for further analysis or reporting.


import requests
import pandas as pd

# 設置 URL 並發送請求
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=rdec-key-123-45678-011121314"
response = requests.get(url)

# 縣市名單
target_cities = ["桃園市", "花蓮市", "連江縣", "台東縣", "嘉義市", "嘉義縣", "屏東縣", 
                 "台中市", "新竹市", "新竹縣", "金門縣", "苗栗縣", "新北市", 
                 "宜蘭縣", "雲林縣", "台南市", "高雄市", "彰化縣", "臺北市", 
                 "南投縣", "澎湖縣", "基隆市"]

# 檢查請求是否成功
if response.status_code == 200:
    # 將 JSON 數據轉換為 Python 字典
    data = response.json()

    # 解析縣市的資料
    locations = data['records']['locations'][0]['location']
    
    # 創建一個空的列表來存儲天氣數據
    weather_data = []

    # 遍歷每個地點
    for location in locations:
        location_name = location['locationName']
        if location_name in target_cities:
            print(f"Processing data for {location_name}...")
            weather_elements = location['weatherElement']

            # 解析每個天氣元素
            for element in weather_elements:
                element_name = element['elementName']
                description = element['description']

                # 遍歷每個時間段
                for time in element['time']:
                    start_time = time['startTime']
                    end_time = time['endTime']
                    element_value = time['elementValue'][0]['value']

                    # 添加記錄到列表中
                    record = {
                        'location': location_name,
                        'start_time': start_time,
                        'end_time': end_time,
                        'element_name': element_name,
                        'description': description,
                        'value': element_value
                    }
                    weather_data.append(record)

    # 將數據轉換為 DataFrame
    df = pd.DataFrame(weather_data)
    
    # 設置顯示選項來顯示完整的 DataFrame
    pd.set_option('display.max_rows', None)  # 顯示所有行
    pd.set_option('display.max_columns', None)  # 顯示所有列
    pd.set_option('display.width', 1000)  # 設置顯示寬度
    pd.set_option('display.colheader_justify', 'left')  # 左對齊列標題

    # 打印 DataFrame 確認結果
    print("\nFinal DataFrame:")
    print(df)

    # 可選：將 DataFrame 保存為 CSV 文件
    df.to_csv('taiwan_weather.csv', index=False)
    print("Data saved to taiwan_weather.csv")

else:
    print("Failed to retrieve data. HTTP Status code:", response.status_code)
