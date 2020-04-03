def isMatch(s, p):
    if not len(s):
        return True
    # s = "aab"
    # p = "c*a*b"
    pi = 0
    plenth = len(p)
    while pi < plenth-1:

        temp = p[pi]
        if p[pi] == '*':
            temp = p[pi-1]

        if temp == s[0] or temp == '.':
            tpi = pi
            for s1 in s:
                tempp = p[tpi]
                if p[pi] == '*':
                    tempp = p[tpi-1]
                    tpi = tpi -1
                print(tempp, s1, tpi)
                if tempp == s1 or tempp == '.':
                    print(tempp, s1, tpi)
                    tpi = tpi +1
                    continue
                break
            else:
                return True

        if p[pi] != '*':
            pi += 1

    return False






if __name__ == '__main__':
    s = '22'
    p = '.*'
    print(isMatch(s, p))
