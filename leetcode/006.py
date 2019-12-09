"""
输入: s = "LEETCODEISHIRING", numRows = 3
输出: "LCIRETOESIIGEDHN"
解释:
    L   C   I   R
    E T O E S I I G
    E   D   H   N
输入: s = "LEETCODEISHIRING", numRows = 4
输出: "LDREOEIIECIHNTSG"
解释:
    L     D     R
    E   O E   I I
    E C   I H   N
    T     S     G
class Solution:
    def convert(self, s: str, numRows: int) -> str:
"""

def convert(s, numRows):
    if numRows == 1:
        return s
    nums = [[] for i in range(numRows)]
    count = 0
    row = 0
    total = len(s)
    while total > count:
        for i in range(numRows):
            if not row:
                print(s[count], count)
                nums[i].append(s[count])
                count +=1
                if count == total:
                    break
            else:
                if row == numRows - i -1:
                    nums[i].append(s[count])
                    count +=1
                    if count == total:
                        break
                else:
                    nums[i].append('')
        row += 1
        if row == numRows-1:
            row = 0
    result = [i for num in nums for i in num if i]
    result =  ''.join(result)
    return result

if __name__ == '__main__':
    s = 'PAYPALISHIRING'
    numRows = 3
    convert(s, numRows)
