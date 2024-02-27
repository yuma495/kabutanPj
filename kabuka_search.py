import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from calculation import automatic_calculation

def get_stock_data(stock_code):
    # 株価情報のページからデータを取得
    stock_url = f"https://kabutan.jp/stock/?code={stock_code}"
    stock_soup = BeautifulSoup(requests.get(stock_url).text, 'html.parser')
    # 財務情報のページからデータを取得
    finance_url = f"https://kabutan.jp/stock/finance?code={stock_code}"
    finance_soup = BeautifulSoup(requests.get(finance_url).text, 'html.parser')
    # Yahooファイナンスからデータを取得
    yahoo_finance_url = f"https://finance.yahoo.co.jp/quote/{stock_code}.T"
    yahoo_soup = BeautifulSoup(requests.get(yahoo_finance_url).text, 'html.parser')


    # 株価を含む要素を探す
    stock_price = get_data(stock_soup, 'span', class_name='kabuka')
    # PERを含む要素を探す
    per_elem = stock_soup.find('div', id='stockinfo_i3').find('td')
    per = per_elem.get_text(strip=True) if per_elem else "情報なし"

    #テーブルを取得
    finance_info_table = stock_soup.find('div', id='kobetsu_right').find_all('table')[2]  # 3番目のテーブルを選択
    #テーブルがない場合は「情報なし」
    if finance_info_table.find('div', class_= "gyouseki_block"):
        # 今季1株益を取得
        now_oneP_elem = finance_info_table.find_all('tr')[2].find_all('td')[3]  # 2行目の4列目を選択
        now_oneP = now_oneP_elem.get_text(strip=True) if now_oneP_elem else "情報なし"
        # 来季1株益を取得
        next_oneP_elem = finance_info_table.find_all('tr')[3].find_all('td')[3]  # 3行目の4列目を選択
        next_oneP = next_oneP_elem.get_text(strip=True) if next_oneP_elem else "情報なし"
    else:
        now_oneP = "情報なし"
        next_oneP = "情報なし"

    ##財務情報を自動取得
    sales_list, operating_list = finance_get(finance_soup)
    #リストから個々の営業益を取り出す
    operating_incomeB, operating_incomeN, operating_incomeA = sales_list
    # リストから個々の売上予想を取り出す
    sales_forecastB, sales_forecastN, sales_forecastA = operating_list

    # 時価総額を取得
                                                    #株によって違うやつがある1XwIwJ
    market_cap_elem = yahoo_soup.find('span', class_="1XwIwJ").find_all('li')[0].find('dl').find('dd').find('span').find('span').find('span')
    market_cap = market_cap_elem.get_text(strip=True) if market_cap_elem else "情報なし"

    # get_stock_data() 関数内で automatic_calculation() を呼び出す部分
    calc_params = {
    "stock_price": clean_numeric(stock_price),  # '3456.0円' のような文字列を処理
    "per": clean_numeric(per),
    "nowP": clean_numeric(now_oneP),
    "nextP": clean_numeric(next_oneP),
    "oiB": clean_numeric(operating_incomeB),
    "oiN": clean_numeric(operating_incomeN),
    "oiA": clean_numeric(operating_incomeA),
    "sales_forecastB": clean_numeric(sales_forecastB),
    "sales_forecastN": clean_numeric(sales_forecastN),
    "sales_forecastA": clean_numeric(sales_forecastA),
    "market_cap": clean_numeric(market_cap),
    }
    result = automatic_calculation(calc_params)

    return {
        "証券コード": stock_code,
        "株価": stock_price,
        "PER": per,
        "今季1株益": now_oneP,
        "来季1株益": next_oneP,
        "前期営業益": operating_incomeB,
        "今季営業益": operating_incomeN,
        "来季営業益": operating_incomeA,
        "前期売上予想": sales_forecastB,
        "今期売上予想": sales_forecastN,
        "来期売上予想": sales_forecastA,
        "時価総額": market_cap,
        **result
    }



#財務情報を取得
def finance_get(finance_soup_data):
    # 財務情報のセクションを取得
    finance_section = finance_soup_data.find('div', class_='fin_year_t0_d fin_year_result_d')
    # 売上予想のデータを格納するためのリスト
    sales_list = []
    operating_list = []

    # 対象の行インデックス：前期売上、今期売上予想、来季期売上
    rows_indexes = [4, 5, 6]

    # 各行インデックスに対してループ
    if finance_section:
        for index in rows_indexes:
            # 指定された行と列から売上予想の要素を取得
            operating_income_elem = finance_section.find_all('tr')[index].find_all('td')[1]
            sales_forecast_elem = finance_section.find_all('tr')[index].find_all('td')[0]

            operating_list.append(operating_income_elem.get_text(strip=True) if operating_income_elem else "情報なし")
            sales_list.append(sales_forecast_elem.get_text(strip=True) if sales_forecast_elem else "情報なし")
    else:
        for index in rows_indexes:
            operating_list.append("情報なし")
            sales_list.append("情報なし")

    return sales_list, operating_list


#余計な文字を除去する処理
def clean_numeric(value):
    if value == "情報なし":
        return 0
    # 非数値文字を除去（カンマ、円記号など）
    cleaned_value = ''.join(filter(str.isdigit, value.replace('.', ''))) or '0'
    return float(cleaned_value)

# ユーザー入力
stock_codes = input("証券コードをカンマ区切りで入力してください（例: 7203,6758,9984）: ").split(',')

# 各証券コードに対して情報を取得し、リストに保存
data = []
for code in stock_codes:
    stock_data = get_stock_data(code.strip())
    data.append(stock_data)

# pandasのDataFrameを作成し、Excelファイルに保存
df = pd.DataFrame(data)
excel_file_path = 'stock_data.xlsx'

try:
    df.to_excel(excel_file_path, index=False)
except PermissionError:
    print(f"エラー: '{excel_file_path}' が開かれているため、ファイルを保存できません。")

specific_data = pd.DataFrame({
    "証券コード": [d["証券コード"] for d in data],
    "上昇率①": [d["上昇率①"] for d in data],
    "目標株価①": [d["目標株価①"] for d in data],
    "上昇率②": [d["上昇率②"] for d in data],
    "目標株価②": [d["目標株価②"] for d in data],
    "PSR": [d["PSR"] for d in data],
    "40%ルール": [d["40%ルール"] for d in data]
})

# "目標株価②"の値に基づいてデータフレームを降順にソート
specific_data_sorted = specific_data.sort_values(by="目標株価②", ascending=False)

# Excelファイルにデータフレームを書き込むためのExcelWriterを使用
with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a') as writer:
    # ソートされたデータフレームを新しいシートに書き込む
    specific_data_sorted.to_excel(writer, sheet_name='特定のデータ', index=False)

print("データをExcelファイルに出力しました。")

# Excelファイルを開く
os.startfile(excel_file_path)
