import numpy as np

# Matriz de coeficientes do sistema linear
A = np.array([[10,  7,  8,  7],
              [ 7,  5,  6,  5],
              [ 8,  6, 10,  9],
              [ 7,  5,  9, 10]])

# Vetor de constantes
b = np.array([32, 23, 33, 31])

# Resolvendo o sistema usando multiplicação de matrizes: x = A^(-1) * b
x = np.dot(np.linalg.inv(A), b)

# Exibindo os resultados
print("Solução do sistema linear:")
print(f"x = {x[0]:.2f}")
print(f"y = {x[1]:.2f}")
print(f"z = {x[2]:.2f}")
print(f"w = {x[3]:.2f}")
print(f"\nVetor solução: {x}")