
def func(haystack, needle):
    ll = len(haystack)
    nl = len(needle)

    if haystack == needle or not nl:
        return 0

    for i in range(ll):
        if haystack[i] == needle[0]:
            F=True
            if ll-i < nl:
                return -1

            for j in range(nl):
                if j+i >= ll or needle[j] != haystack[j+i]:
                    F=False
                    break
            if F:
                return i
    return -1


if __name__ == '__main__':
    haystack = "hello"
    needle = "ll"
    result = func(haystack, needle)
    print(result)
