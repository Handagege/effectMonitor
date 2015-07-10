#!/usr/bin/python

def parserKeyToMap(dataList,index):
	keyMap = {}
	for i in dataList:
		pos = i.rfind(index)
		key = i[:pos]
		if key in keyMap.keys():
			keyMap[key].append(i)
		else:
			keyMap[key] = []
			keyMap[key].append(i)
	return keyMap


strList = ["userprofile.st1.sp2","userprofile.st1.sp1","userprofile","userprofile-cand1","userprofile-cand2","userprofile:st1","userprofile.st2.sp1","feed.st1.sp1","feed"]

indexList = [".",":","-"]

key1List = []
key2List = []
key3List = []
key4List = []

stdIndex = ":"
for key in strList:
	if key.rfind(indexList[0]) != -1:
		key = key.replace(indexList[0],stdIndex)
		key1List.append(key)
	elif key.rfind(indexList[1]) != -1:
		key = key.replace(indexList[1],stdIndex)
		key2List.append(key)
	elif key.rfind(indexList[2]) != -1:
		key = key.replace(indexList[2],stdIndex)
		key3List.append(key)
	else:
		key4List.append(key)

print key1List
print key2List
print key3List
print key4List


key1Map = parserKeyToMap(key1List,stdIndex)
key2Map = parserKeyToMap(key2List,stdIndex)
key3Map = parserKeyToMap(key3List,stdIndex)

print key1Map
print key2Map
print key3Map
print key4List
