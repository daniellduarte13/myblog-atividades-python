def f(nums):
    if not nums or len(nums) < 2:
        return False
    return len(nums) != len(set(nums))
# print(f([1, 2, 3, 3]))
