def f(nums):
    visto = set()
    for num in nums:
        if num in visto:
            duplicado = num
            break
        visto.add(num)
    n = len(nums)
    faltante = n * (n + 1) // 2 - sum(nums) + duplicado
    return (duplicado, faltante)
# print(f([1, 2, 2, 4]))
