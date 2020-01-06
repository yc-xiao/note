# 快排 O(n)
import random
array = random.sample([i for i in range(100000)], 10000)
array = [random.randint(0, 3) for i in range(10)]

# [l, r]闭区间
def so_sort(array, left, right):
    if right <= left:
        return
    temp = array[left]
    lindex = left
    rindex = right
    while lindex < rindex:
        while lindex < rindex and array[lindex] <= temp:
            lindex+=1
        while lindex < rindex and array[rindex] >= temp:
            rindex-=1
        if lindex < rindex:
            array[lindex], array[rindex] = array[rindex], array[lindex]
            lindex+=1
            rindex-=1
    if array[lindex] > temp:
        lindex-=1
    array[lindex], array[left] = array[left], array[lindex]

    so_sort(array, left, lindex-1)
    so_sort(array, lindex+1, right)


# 栈处理了递归问题
def zz_so_sort(array, left, right):
    if right <= left:
        return
    zz = []
    zz.append((left, right))
    while zz:
        left, right = zz.pop()
        temp = array[left]
        lindex = left
        rindex = right
        while lindex < rindex:
            while lindex < rindex and array[lindex] <= temp:
                lindex+=1
            while lindex < rindex and array[rindex] >= temp:
                rindex-=1
            if lindex < rindex:
                array[lindex], array[rindex] = array[rindex], array[lindex]
                lindex+=1
                rindex-=1
        if array[lindex] > temp:
            lindex-=1
        array[lindex], array[left] = array[left], array[lindex]

        if left < lindex-1:
            zz.append((left, lindex-1))
        if lindex+1 < right:
            zz.append((lindex+1, right))
        # so_sort(array, left, lindex-1)
        # so_sort(array, lindex+1, right)

def main():
    print(array)
    zz_so_sort(array, 0, len(array)-1)
    print(array)

if __name__ == "__main__":
    main()
