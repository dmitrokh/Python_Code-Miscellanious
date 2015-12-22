import time
def userInput():
    userStr = input("Enter numbers for list divided by ',' :")
    userList = userStr.split(',')
    return userList

def intersection(_list1, _list2, _interList):
    for j in range(len(_list2)):
        if _list1[0] == _list2[j]:
            _interList.append(_list1[0])
        for i in range(len(_list1)):
            for j in range(len(_list2)):
                flag = 0
                if _list1[i] == _list2[j]:
                    for k in range(len(_interList)):
                        if _interList[k] == _list1[i]:
                            flag = 1
                    if flag == 0:
                        _interList.append(_list1[i])
        break
    return _interList

interList = []
print("The program will find the intersection of two lists of numbers")
list1 = userInput()
list2 = userInput()

if len(list1) == 0 or len(list2) == 0:
    print("the intersection set is empty")
else:
    interList = intersection(list1, list2, interList)
print(interList)




