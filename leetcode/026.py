

def func(nums):
    if not nums:
        return 0
    v = nums[0]
    j = 0
    for i in range(len(nums)):
        if v == nums[i]:
            nums[j] = v
        else:
            v = nums[i]
            j+=1
            nums[j] = v
    return j+1

if __name__ == '__main__':
    nums = [0,0,1,1,1,2,2,3,3,4]
    n = func(nums)
    result = [nums[i] for i in range(n)]
    print(result)
