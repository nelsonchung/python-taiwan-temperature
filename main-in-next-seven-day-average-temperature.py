import requests
import pandas as pd
import json

# 使用您的網址
# 英文版
#url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-006?Authorization=rdec-key-123-45678-011121314&format=JSON"
# 中文版
url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-005?Authorization=rdec-key-123-45678-011121314&format=JSON"
response = requests.get(url)

# 檢查請求是否成功
if response.status_code == 200:
    # 將 JSON 數據轉換為 Python 字典
    data = response.json()
    
    # 打印出 JSON 數據結構來檢查
    print(json.dumps(data, indent=4))

    # 確認資料結構並解析
    if 'cwaopendata' in data:
        locations = data['cwaopendata']['dataset']['location']

        # 創建一個空的列表來存儲天氣數據
        weather_data = []

        # 遍歷每個地點的天氣預報數據
        for location in locations:
            location_name = location['locationName']
            weather_elements = location['weatherElement']

            # 取出所需的天氣元素，如氣溫、降雨機率等
            for i in range(len(weather_elements[0]['time'])):
                record = {
                    'location': location_name,
                    'start_time': weather_elements[0]['time'][i]['startTime'],
                    'end_time': weather_elements[0]['time'][i]['endTime'],
                    'weather': weather_elements[0]['time'][i]['parameter']['parameterName'],
                    'max_temperature': float(weather_elements[1]['time'][i]['parameter']['parameterName']),
                    'min_temperature': float(weather_elements[2]['time'][i]['parameter']['parameterName'])
                }
                weather_data.append(record)

        # 將數據轉換為 DataFrame
        df = pd.DataFrame(weather_data)

        # 進行一週天氣分析（例如，計算平均最高和最低溫度）
        weekly_summary = df.groupby('location').agg({
            'max_temperature': ['mean', 'min', 'max'],
            'min_temperature': ['mean', 'min', 'max'],
            'weather': lambda x: x.mode()[0]  # 找出最常見的天氣狀況
        }).reset_index()

        # 輸出結果
        print("Weekly Weather Summary:")
        print(weekly_summary)

    else:
        print("Unexpected JSON structure")
else:
    print("Failed to retrieve data. HTTP Status code:", response.status_code)
