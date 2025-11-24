def f(nums, alvo):
    visto = {}
    for i, num in enumerate(nums):
        complemento = alvo - num
        if complemento in visto:
            return (visto[complemento], i)
        visto[num] = i
# print(f([2, 7, 11, 15], 9))
