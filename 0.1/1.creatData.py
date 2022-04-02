'''
Author: Innis
Description: Rete:A Fast Algorithm for the Many Pattern
Date: 2022-03-28 22:13:01
LastEditTime: 2022-03-28 22:39:27
FilePath: \0328P-rete\creatData.py
'''
import csv
import random
import time

def getRandomData():
    grade = random.randint(1,13)

    sexNum  = random.randint(0,1)
    sex = ""
    if sexNum == 0:
        sex = "male"
    elif sexNum == 1:
        sex = "female"

    age = random.randint(5,17)

    figureNum = random.randint(1,3)
    figure = ""
    if figureNum == 1:
        figure = "thin"
    elif figureNum == 2:
        figure = "normal"
    elif figureNum == 3:
        figure = "strong"

    heigth = random.randint(150,190)
    return [grade,sex,age,figure,heigth]

data = []
start = time.time()
for i in range(500000):
    ramdomData = getRandomData()
    id = str(i+1).zfill(6)
    ramdomData.insert(0,id)
    data.append(ramdomData)

with open("data.csv","w",newline="") as handle:
    writer = csv.writer(handle)
    writer.writerows(data)
end = time.time()
print(f"{end-start}s,done")