def f(x, y):
    n = len(x)
    soma_x = sum(x)
    soma_y = sum(y)
    soma_xy = sum(x[i] * y[i] for i in range(n))
    soma_x2 = sum(xi * xi for xi in x)
    inclinacao = (n * soma_xy - soma_x * soma_y) / (n * soma_x2 - soma_x * soma_x)
    intercepto = (soma_y - inclinacao * soma_x) / n
    return [intercepto, inclinacao]
# print(f([-2, -2, -1, -1, 0, 0, 1, 1, 2, 2], [0, 0, 2, 3, 4, 4, 5, 6, 8, 8]))
