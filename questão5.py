def f(x, y):
    resultado = []
    for i in range(max(len(x), len(y))):
        if i < len(x): resultado.append(x[i])
        if i < len(y): resultado.append(y[i])
    return resultado
# print(f(["a", "b", "c"], [1, 2, 3]))
