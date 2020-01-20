

if __name__ == '__main__':
    nums = [1,2,3,5]
    ll = len(nums)
    results = [nums[i+1] for i in range(0,ll,2) for j in range(nums[i])]
    print(results)
