import requests
from bs4 import BeautifulSoup

# 中油油價公告頁（實際網址可能需要你更新）
url = "https://www.cpc.com.tw/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'  # 有時會是 big5 或 utf-8 看網頁源碼

soup = BeautifulSoup(response.text, "html.parser")

message = "📢 今天油價：\n"

# 根據實際的網頁內容做選擇
# 假設油價公告在某個特定區塊，例如 class 為 "price-box" 或 "oil-price"
# 以下為假設寫法，實際要根據 HTML 結構調整
oil_section = soup.find("ul", class_="today_price_ct")  # 你需要打開開發者工具看正確 class
if oil_section:
    items = oil_section.select(".today_price_info")
    response = requests.get("https://www.cpc.com.tw/GetOilPriceJson.aspx?type=TodayOilPriceString")
    data = response.json()
    for item in items:
        label = item.select_one(".name").get_text(strip=True)
        price = item.select_one(".price")
        priceId = price.get("id")
        message += f"{label}:{data[priceId[2:]]}\n"
else:
    print("找不到油價資料")
    
channel_access_token = "xPf+q95sdpLv68wbU48tI3FHqP83sQeAvx5sUXi3cSOjIgVVKDPTG1NtIKchv64riyw4HnvkjT+BdRL3UhPknhg6+Rt+u1xbeV8Qlv3JF7Hg3lFaCdLtuX5kZmuC/jKBP0Xj4RrmcAgTXwYj6kohCAdB04t89/1O/w1cDnyilFU="
line_headers = {
    "Authorization": f"Bearer {channel_access_token}",
    "Content-Type": "application/json"
}

line_data = {
    "messages": [
        {
            "type": "text",
            "text": message
        }
    ]
}

res = requests.post("https://api.line.me/v2/bot/message/broadcast", headers=line_headers, json=line_data)
print(res)