#自動計算処理
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
    rate1 = (targetP1 - stock_price) / stock_price #上昇率①

    #oiNが0でわたってくる可能性があるため
    if oiN != 0:
        increase_rate =(((oiN - oiB)/oiB) + ((oiA - oiN)/oiA))/2 #増益率3期平均
        next_increase_rat = (oiA - oiN)/oiN                      #来季増益率
    else:
        next_increase_rat = 0

    #目標PER算出
    targetPER=per_calculation(next_increase_rat)

    targetP2= targetPER * middleP                      #目標株価②
    rate2=(targetP2 - stock_price) / stock_price       #上昇率②
    yosouPER = stock_price / middleP                     #予想PER
    psr = market_cap/sales_forecastN                   #psr
    revenue_price=(((sales_forecastN-sales_forecastB)/sales_forecastB)+((sales_forecastA-sales_forecastN)/sales_forecastN))/2 #増収率
    profit_Rate=oiN/sales_forecastN         #利益率
    answer = profit_Rate + revenue_price    #40％ルール

    #パーセンテージで表示する
    return {
        "目標株価①" :targetP1,
        "上昇率①" :str(round(rate1 * 100, 1)) + "%",
        "目標PER" :targetPER,
        "目標株価②" :targetP2,
        "上昇率②" :str(round(rate2 * 100, 1)) + "%",
        "予想PER" :yosouPER,
        "来季増益率" :str(round(next_increase_rat * 100, 1)) + "%" ,
        "PSR" :psr,
        "利益率" :str(round(profit_Rate * 100, 1)) + "%",
        "40%ルール" :str(round(answer * 100, 2)) + "%"
    }



#TODO:マイナスの場合の考慮ができていない
#目標PERを出す
def per_calculation(next_increase_rat):
    basePER = 0
    targetPER = 0
    if next_increase_rat <= 0:
        basePER = None
    elif 1 <= next_increase_rat <= 7:
        basePER = 5
    elif 8 <= next_increase_rat <= 12:
        basePER = 10
    elif 13 <= next_increase_rat <= 17:
        basePER = 15
    elif 18 <= next_increase_rat <= 22:
        basePER = 20
    elif 23 <= next_increase_rat <= 27:
        basePER = 25
    elif 28 <= next_increase_rat <= 32:
        basePER = 30
    elif 33 <= next_increase_rat <= 37:
        basePER = 35
    elif 38 <= next_increase_rat <= 45:
        basePER = 40
    elif 46 <= next_increase_rat <= 54:
        basePER = 50
    elif 55 <= next_increase_rat <= 64:
        basePER = 60
    else :
        basePER = 70
    
    #2年で考える
    if basePER == 5:
        targetPER = 16.5
    elif basePER == 10:
        targetPER = 18.2
    elif basePER == 15:
        targetPER = 19.8
    elif basePER == 20:
        targetPER = 21.6
    elif basePER == 25:
        targetPER = 23.4
    elif basePER == 30:
        targetPER = 25.4
    elif basePER == 35:
        targetPER = 27.3
    elif basePER == 40:
        targetPER = 29.4
    elif basePER == 40:
        targetPER = 29.4
    elif basePER == 50:
        targetPER = 33.8
    elif basePER == 60:
        targetPER = 38.4
    else:
        targetPER = 43.4

    return targetPER

