'''
Author: Innis
Description: creat fake data and store to txt
Date: 2022-04-01 21:55:36
LastEditTime: 2022-04-01 22:11:37
FilePath: \0328P-rete\0.1\1.1.createData.py
'''

"if d1 e1 d2 e2 then action5"

times = 1


def createData():
    global times
    numList = [str(times).zfill(6)[index] for index in range(6)]

    pattern = ["a" + numList[-1], "b" + numList[-2],
               "c" + numList[-3], "d" + numList[-4], "e" + numList[-5], "f" + numList[-6]]
    rule = "if " + " ".join(pattern) + " then " + f"action{times}"

    times += 1

    return rule + "\n"


for i in range(500000):
    rule = createData()
    with open("data.txt", "a+") as handle:
        handle.write(rule)

print("done")
