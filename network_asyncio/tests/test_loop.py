count = 1
# 正常退出执行else可以理解为条件不满足，选择else。break非正常退出不执行else
while count < 50:
    count += 1
else:
    print('while 循环结束')

count = 1

for i in range(10):
    pass
else:
    print('for 循环结束')
