"""
给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转
输入: 123
输出: 321

输入: -123
输出: -321

输入: 120
输出: 21
"""
"""
class Solution:
    def reverse(self, x: int) -> int:
"""

def reverse(x):
    nums = []
    flag = False
    if x < 0:
        x = -1 * x
        flag = True
    while x:
        num = x%10
        x = x//10
        nums.append(num)
    num = 0
    for each in nums:
        num = num * 10 + each
    if flag:
        num = num * -1
    if -2**31 > num or num > 2**31-1:
        return 0
    print(num)

if __name__ == '__main__':
    reverse(1563847412)
