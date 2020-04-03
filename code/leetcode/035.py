


if __name__ == '__main__':
    nums = [1,3,5,6]
    target = 7
    ll = len(nums)
    for i in range(ll):
        if nums[i] >= target:
            print(i)
            # return i
    print(ll)
    # return ll
