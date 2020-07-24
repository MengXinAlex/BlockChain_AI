nums = [2,3,4]
target = 6

for i,j in enumerate (nums):
    nums.pop(i)
    print(i)
    for m,k in enumerate (nums):
        label = m
        number =k
        nums.insert(i,j)
        if i+number ==target:
            for a in range(len(nums)):
                if nums[a]==number:
                    print([i,a])