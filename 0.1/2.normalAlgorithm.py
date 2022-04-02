'''
Author: Innis
Description: use normal algorithm to peocess data
Date: 2022-03-28 22:34:52
LastEditTime: 2022-03-29 00:04:10
FilePath: \0328P-rete\2.normalAlgorithm.py
'''

import csv
import time


with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

start = time.time()
result = []
for ele in data:
    if int(ele[1]) ==6  and ele[2] =="male" and int(ele[3]) ==13 and ele[4] == "normal" and int(ele[5]) ==170:
        result.append(ele[0])
end = time.time()
print(f"{end-start}s,done")
print(f"amout is {len(result)}")
