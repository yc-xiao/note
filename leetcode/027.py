

def func(nums, val):
    ll = len(nums)
    j = 0
    for i in range(ll):
        if nums[i] != val:
            nums[j] = nums[i]
            j+=1
    return j

if __name__ == '__main__':
    nums = [3,2,2,3,3,4,1]
    val = 3
    n = func(nums, val)
    for i in range(n):
        print(nums[i])
