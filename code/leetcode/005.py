# 回文
# 给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。

import random

def is_hw(array):
    count = len(array)
    num = count//2
    for i in range(num):
        if array[i] != array[count-i-1]:
            return False
    return True
"""
def is_hw(array):
    count = len(array)
    num = count//2
    for i in range(num):
        if array[i] != array[count-i-1]:
            return False
    return True

class Solution:
    def longestPalindrome(self, s: str) -> str:
        lenth = len(s)
        max = s[0] if s else ''
        for i in range(lenth):
            max_l = len(max)
            if max_l >= lenth-i+1:
                break
            for j in range(lenth-1, i, -1):
                if s[i] == s[j]:
                    if max_l >= j+1-i:
                        break
                    if is_hw(s[i:j+1]):
                        max = s[i:j+1]
                        break
        return max
"""
"""
def is_hw(array):
    count = len(array)
    num = count//2
    for i in range(num):
        if array[i] != array[count-i-1]:
            return False
    return True

class Solution:
    def longestPalindrome(self, s: str) -> str:
        lenth = len(s)
        max = s[0] if s else ''
        for i in range(lenth):
            for j in range(lenth-1, i, -1):
                if len(max) > j+1-i:
                    break
                if s[i] == s[j]:
                    if is_hw(s[i:j+1]):
                        if len(max) < j+1-i:
                            max = s[i:j+1]
                        break
        return max
"""
if __name__ == '__main__':
    s = random.sample('abcdefalksdjlizuxbeonvxw', 20)
    s = ''.join(s)
    lenth = len(s)
    print(s)
    max = s[0]
    for i in range(lenth):
        for j in range(lenth-1, i, -1):
            if len(max) > j+1-i:
                break
            if s[i] == s[j]:
                if is_hw(s[i:j+1]):
                    if len(max) < j+1-i:
                        max = s[i:j+1]
                    break
    print(max)
