import sys

def isValidForEncode():
    resultList = []
    testCasesEncode = ['a', 'ab', 'aab', 'aabbaa', '1', '1aaa', 'aa4bb', 'aa.bb', '.aa', '*', '']
    for k in range(len(testCasesEncode)):
        result = rleEncode(testCasesEncode[k])
        resultList.append(result)
        if rleEncode(testCasesEncode[k]) == -1:
            print("Ok - Test failed for Encode function if input equals: ", testCasesEncode[k])
    

def isValidForDecode():
    testCasesDecode = [['2a','3b','4c'],['12a','13b'],['2a','12b'],['12a','2b'],[],[''],['',''],['2a',''],['','2b'],['a','2b'],['2a','b'],[',','2b'],['1!','2b'],['2a','!b']]
    for n in range(len(testCasesDecode)):
        if rleDecode(testCasesDecode[n]) == -1:
            print("Ok - Test failed for Decode function if input equals: ",testCasesDecode[n])
    

def rleEncode(aStr):
    count = 1
    listRLEcode = []
    if len(aStr) == 0:
        return -1
    else:
        for i in range(len(aStr)):
            if aStr[0].isalpha():
                if i == len(aStr) - 1:
                    listRLEcode.append(str(count) + aStr[i])
                    break
                if aStr[i].isalpha() and aStr[i+1].isalpha():
                    if aStr[i] == aStr[i+1]:
                        count += 1
                    else:
                        listRLEcode.append(str(count) + aStr[i])
                        count = 1
                else:
                    return -1
            else:
                return -1
    return listRLEcode

def rleDecode(rleEnc):
    i = 0
    j = 0
    multi = ''
    strOut = ''
    rleEnc.reverse()
    if len(rleEnc) == 0:
        return -1
    else:
        for i in range(len(rleEnc)):
            if len(rleEnc[i]) == 0:
                return -1
            else:
                strT = rleEnc[i]
                j = 0
                multi = ''
                while j < len(strT):
                    if strT[j].isdigit() and strT[j + 1].isalpha():
                        multi += strT[j]
                        strOut += strT[j + 1] * int(multi)
                        multi = ''
                        break
                    elif strT[j].isdigit() and strT[j + 1].isdigit():
                        multi += strT[j]
                        j = j + 1
                    else:
                        return -1
        return strOut

working = True
isValidForEncode()
isValidForDecode()
print("The program will convert the sequence of letters to RLE code and back")

while working == True:
    strIn = input("Enter valid string (only letters):  ")
    rleEncoded = rleEncode(strIn)
    if rleEncoded != -1:
        for l in range(len(rleEncoded)):
            print(rleEncoded[l], end='')
        rleDecoded = rleDecode(rleEncoded)
        print('\n'+rleDecoded)
        working = False
    else:
        print("Invalid input")
        
    






