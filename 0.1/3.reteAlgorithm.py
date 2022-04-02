'''
Author: Innis
Description: built rete graph
Date: 2022-03-28 22:53:27
LastEditTime: 2022-03-29 00:10:42
FilePath: \0328P-rete\3.reteAlgorithm.py
'''
import csv
import time


# built graph
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

start = time.time()
nodeAlphaGrade = []
nodeAlphaSex = []
nodeAlphaAge = []
nodeAlphafigure = []
nodeAlphaHeight = []

nodeBeta_Grade_Sex = []
nodeBeta_Grade_Sex_Age = []
nodeBeta_Grade_Sex_Age_Figure = []
nodeBeta_Grade_Sex_Age_Figure_Height = []

for ele in data:
    if int(ele[1]) > 10:
        nodeAlphaGrade.append(ele[0])
    else:
        continue

    if ele[2] =="male":
        nodeAlphaSex.append(ele[0])
        nodeBeta_Grade_Sex.append(ele[0])
    else:
        continue

    if int(ele[3]) >15:
        nodeAlphaAge.append(ele[0])
        nodeBeta_Grade_Sex_Age.append(ele[0])
    else:
        continue

    if ele[4] == "strong":
        nodeAlphafigure.append(ele[0])
        nodeBeta_Grade_Sex_Age_Figure.append(ele[0])
    else:
        continue

    if int(ele[5]) > 180:
        nodeAlphaHeight.append(ele[0])
        nodeBeta_Grade_Sex_Age_Figure_Height.append(ele[0])
    else:
        continue

end = time.time()
print(f"Built graph cost {end-start}s")

start1 = time.time()
goal = ['500000', '6', 'male', '13', 'normal', '170']
if goal[0] == '500000' and goal[1] == '6' and goal[2] == 'male' and  goal[3] =='13' and goal[4] =='normal' and goal[5] =='170':
    pass
end1 = time.time()
#print(f"Amout is {len(nodeBeta_Grade_Sex_Age_Figure_Height)}")
print(f"Match cost {end1-start1}s")
