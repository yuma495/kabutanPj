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