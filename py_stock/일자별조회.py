import win32com.client


def ReqeustData(obj):
    # 데이터 요청
    obj.BlockRequest()

    # 통신 결과 확인
    rqStatus = obj.GetDibStatus()
    rqRet = obj.GetDibMsg1()
    #print("통신상태", rqStatus, rqRet)
    if rqStatus != 0:
        return False

    # 일자별 정보 데이터 처리
    count = obj.GetHeaderValue(1)  # 데이터 개수
    for i in range(count):
        date = obj.GetDataValue(0, i)  # 일자
        open = obj.GetDataValue(1, i)  # 시가
        high = obj.GetDataValue(2, i)  # 고가
        low = obj.GetDataValue(3, i)  # 저가
        close = obj.GetDataValue(4, i)  # 종가
        diff = obj.GetDataValue(5, i)  # 종가
        vol = obj.GetDataValue(6, i)  # 종가
        print(date, '\t', open, '\t', high, '\t', low, '\t', close, '\t', diff, '\t', vol)

    return True


# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# 일자별 object 구하기
objStockWeek = win32com.client.Dispatch("DsCbo1.StockWeek")
objStockWeek.SetInputValue(0, 'A229200')  # 종목 코드 - KODEX 코스다 150

# 최초 데이터 요청
ret = ReqeustData(objStockWeek)
if ret == False:
    exit()

# 연속 데이터 요청
# 예제는 5번만 연속 통신 하도록 함.
#NextCount = 1
while objStockWeek.Continue:  # 연속 조회처리
    #NextCount += 1;
    #if (NextCount > 5):
    #    break
    ret = ReqeustData(objStockWeek)
    if ret == False:
        exit()

#통신상태 0 B035 조회가 계속 됩니다.(stock.week1)
#20200214 60900 61900 60200 61800 1100 13276067
#20200213 61200 61600 60500 60700 200 18449775
#20200212 60300 60700 59700 60500 600 12904207
#20200211 59800 60700 59700 59900 200 11071231
#20200210 59200 59800 59100 59700 700 13107121

#통신상태 0 B035 조회가 계속 됩니다.(stock.week1)
#20200214 60900 61900 60200 61800 1100 13276067
#20200213 61200 61600 60500 60700 200 18449775
#20200212 60300 60700 59700 60500 600 12904207
#20200211 59800 60700 59700 59900 200 11071231
#20200210 59200 59800 59100 59700 700 13107121
