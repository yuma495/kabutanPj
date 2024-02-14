import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_stock_data(stock_code):
    # 株価情報のURL
    stock_url = f"https://kabutan.jp/stock/?code={stock_code}"
    # 財務情報のURL
    finance_url = f"https://kabutan.jp/stock/finance?code={stock_code}"
    #Yahooファイナンス
    yahoo_finance_url = f"https://finance.yahoo.co.jp/quote/{stock_code}.T"

    # 株価情報のページからデータを取得
    response = requests.get(stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 株価を含む要素を探す
    stock_price = get_data(soup, 'span', class_name='kabuka')

    # PERを含む要素を探す
    per_elem = soup.find('div', id='stockinfo_i3').find('td')
    per = per_elem.get_text(strip=True) if per_elem else "情報なし"

    #テーブルを取得
    finance_info_table = soup.find('div', id='kobetsu_right').find_all('table')[2]  # 3番目のテーブルを選択

    # 今季1株益を取得
    now_oneP_elem = finance_info_table.find_all('tr')[2].find_all('td')[3]  # 2行目の4列目を選択
    now_oneP = now_oneP_elem.get_text(strip=True) if now_oneP_elem else "情報なし"
    # 来季1株益を取得
    next_oneP_elem = finance_info_table.find_all('tr')[3].find_all('td')[3]  # 3行目の4列目を選択
    next_oneP = next_oneP_elem.get_text(strip=True) if next_oneP_elem else "情報なし"

    # 財務情報のページからデータを取得
    response = requests.get(finance_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 前期営業益を取得
    operating_income_elem = soup.find('div', class_='fin_year_t0_d fin_year_result_d').find_all('tr')[4].find_all('td')[1]
    operating_incomeB = operating_income_elem.get_text(strip=True) if operating_income_elem else "情報なし"

    # 今季営業益を取得
    operating_income_elem = soup.find('div', class_='fin_year_t0_d fin_year_result_d').find_all('tr')[5].find_all('td')[1]
    operating_incomeN = operating_income_elem.get_text(strip=True) if operating_income_elem else "情報なし"

    # 来季営業益を取得
    operating_income_elem = soup.find('div', class_='fin_year_t0_d fin_year_result_d').find_all('tr')[6].find_all('td')[1]
    operating_incomeA = operating_income_elem.get_text(strip=True) if operating_income_elem else "情報なし"
    
    # #テーブルを取得
    # sales_forecast_table = soup.find('div', id='finance_box').find_all('div')[4].find('table')  # 5番目のdiv内のテーブルを選択

    #前期売上
    sales_forecast_elem = soup.find('div', class_='fin_year_t0_d fin_year_result_d').find_all('tr')[4].find_all('td')[0]
    sales_forecastB = sales_forecast_elem.get_text(strip=True) if sales_forecast_elem else "情報なし"
    
    # 今期売上予想を取得
    sales_forecast_elem = soup.find('div', class_='fin_year_t0_d fin_year_result_d').find_all('tr')[5].find_all('td')[0]
    sales_forecastN = sales_forecast_elem.get_text(strip=True) if sales_forecast_elem else "情報なし"

    #来季期売上
    sales_forecast_elem = soup.find('div', class_='fin_year_t0_d fin_year_result_d').find_all('tr')[6].find_all('td')[0] 
    sales_forecastA = sales_forecast_elem.get_text(strip=True) if sales_forecast_elem else "情報なし"

    #Yahooファイナンスからデータを取得
    response = requests.get(yahoo_finance_url)
    soupY = BeautifulSoup(response.text, 'html.parser')

    # 時価総額を取得
    market_cap_elem = soupY.find('ul', class_="_3U1XwIwJ").find_all('li')[0].find('dl').find('dd').find('span').find('span').find('span')
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

    # result = automatic_calculation(stock_price,per,now_oneP,next_oneP,operating_incomeB,operating_incomeN,operating_incomeA,sales_forecastB,sales_forecastN,sales_forecastA)
    
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

def automatic_calculation(params):
    stock_price = params.get("stock_price")
    per = params.get("per")
    nowP = params.get("nowP")
    nextP = params.get("nextP")
    oiB = params.get("oiB")
    oiN = params.get("oiN")
    oiA = params.get("oiA")
    sales_forecastB = params.get("sales_forecastB")
    sales_forecastN = params.get("sales_forecastN")
    sales_forecastA = params.get("sales_forecastA")
    market_cap = params.get("market_cap")


    middleP = (nowP + nextP) / 2  #中間
    targetP1 = middleP * per        #目標株価①
    rate1 = (targetP1 -stock_price) / stock_price #上昇率①

    increase_rate =(((oiN - oiB)/oiB) + ((oiA - oiN)/oiA))/2 #増益率3期平均
    next_increase_rat = (oiA - oiN)/oiN                     #来季増益率
    
    #目標PER算出
    # targetPER=hoge(next_increase_rat)

    # targetP2=targetPER*targetP1                    #目標株価②
    # rate2=(targetP2 - stock_price)/stock_price  #上昇率②
    yosouPER = stock_price/middleP        #予想PER

    psr = market_cap/sales_forecastN    #psr

    #増収率
    revenue_price=(((sales_forecastN-sales_forecastB)/sales_forecastB)+((sales_forecastA-sales_forecastN)/sales_forecastN))/2 

    #利益率
    profit_Rate=oiN/sales_forecastN
    #40％ルール
    answer = profit_Rate + revenue_price

    return {
        "目標株価①" :targetP1,
        "上昇率①" :rate1,
        # "目標PER" :targetPER,
        # "目標株価②" :targetP2,
        # "上昇率②" :rate2,
        "40%ルール" : answer
    }

#余計な文字を除去する処理
def clean_numeric(value):
    if value == "情報なし":
        return 0
    # 非数値文字を除去（カンマ、円記号など）
    cleaned_value = ''.join(filter(str.isdigit, value.replace('.', ''))) or '0'
    return float(cleaned_value)

def get_data(soup, tag, class_name=None, id=None):
    try:
        if class_name:
            elem = soup.find(tag, class_=class_name)
        elif id:
            elem = soup.find(tag, id=id)
        else:
            elem = soup.find(tag)
        return elem.get_text(strip=True) if elem else "情報なし"
    except Exception as e:
        return "情報なし"

#TODO:目標PERの算出方法を考える
#目標PERを出す
def hoge(next_increase_rat):
    return

# ユーザー入力
stock_codes = input("証券コードをカンマ区切りで入力してください（例: 7203,6758,9984）: ").split(',')

# 各証券コードに対して情報を取得し、リストに保存
data = []
for code in stock_codes:
    stock_data = get_stock_data(code.strip())
    data.append(stock_data)

# pandasのDataFrameを作成し、Excelファイルに保存
df = pd.DataFrame(data)
df.to_excel('stock_data.xlsx', index=False)

print("データをExcelファイルに出力しました。")
