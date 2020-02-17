import win32com.client

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# 종목코드 리스트 구하기
objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = objCpCodeMgr.GetStockListByMarket(1)  # 거래소
codeList2 = objCpCodeMgr.GetStockListByMarket(2)  # 코스닥

#outFp = open("d:/종목.txt ", "w")
#outStr = ""

print("거래소 종목코드", len(codeList))
for i, code in enumerate(codeList):
    secondCode = objCpCodeMgr.GetStockSectionKind(code)
    name = objCpCodeMgr.CodeToName(code)
    stdPrice = objCpCodeMgr.GetStockStdPrice(code)
    print(i, '\t', code, '\t', secondCode, '\t', stdPrice, '\t', name)
#    outStr = outStr + chr(i)
#    outStr = outStr + chr(code)
#    outStr = outStr + chr(secondCode)
#    outStr = outStr + chr(strPrice)
#    outStr = outStr + name
#    outFp.writelines( outStr )

#outFp.close()

print("코스닥 종목코드", len(codeList2))
for i, code in enumerate(codeList2):
    secondCode = objCpCodeMgr.GetStockSectionKind(code)
    name = objCpCodeMgr.CodeToName(code)
    stdPrice = objCpCodeMgr.GetStockStdPrice(code)
    print(i, '\t', code, '\t', secondCode, '\t', stdPrice, '\t', name)

print("거래소 + 코스닥 종목코드 " ,len(codeList) + len(codeList2))


# 거래소 종목코드 1565
# 0 A000020 1 7580 동화약품
# 1 A000040 1 250 KR모터스
