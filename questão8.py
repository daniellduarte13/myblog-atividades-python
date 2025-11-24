def f(nums):
    produto_total = 1
    zeros = nums.count(0)
    if zeros > 1:
        return [0] * len(nums)
    for num in nums:
        if num != 0:
            produto_total *= num
    resultado = []
    for num in nums:
        if zeros == 1:
            resultado.append(0 if num != 0 else produto_total)
        else:
            resultado.append(int(produto_total / num) if num != 0 else 0)
    return resultado
# print(f([1, 2, 4, 6]))
