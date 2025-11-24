def f(x):
    from itertools import product
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    ops = ['+', '-', '']
    resultados = []
    for combinacao in product(ops, repeat=8):
        expressao = nums[0]
        for i in range(8):
            expressao += combinacao[i] + nums[i+1]
        if eval(expressao) == x:
            resultados.append(expressao + f'=={x}')
    return resultados
# print(f(100))
