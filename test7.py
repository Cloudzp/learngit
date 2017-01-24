#计算1-100的整数之和，从1写道100优点困难，幸好Python提供了一个range()函数，可以##声称一个序列，再通过list()函数转换为list.比如range(5)生成的序列是从0开始的小于5#的整数：
sum = 0
for x in range(101):
    sum = sum + x
print(sum)
#运行结果：5050
