def f(prices):
    if not prices or len(prices) < 2:
        return 0
    lucro_max = 0
    preco_min = prices[0]
    for preco in prices[1:]:
        if preco < preco_min:
            preco_min = preco
        lucro_atual = preco - preco_min
        if lucro_atual > lucro_max:
            lucro_max = lucro_atual
    return lucro_max
# print(f([10, 1, 5, 6, 7, 1]))
