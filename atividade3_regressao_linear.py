# Atividade 3: Regressão Linear
# Calcula regressão linear usando fórmula matricial: β = (X'X)^(-1)X'y

import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_point, geom_abline, ggsave

# Lê os dados dos arquivos X.txt e y.txt
with open("X.txt", 'r') as f:
    valores_x = np.array([float(linha.strip()) for linha in f.readlines()])

with open("y.txt", 'r') as f:
    valores_y = np.array([float(linha.strip()) for linha in f.readlines()])

# Calcula a regressão linear usando fórmula matricial
n = len(valores_x)

# Cria a matriz de design X (primeira coluna: 1s para intercepto, segunda: valores de x)
X = np.column_stack([np.ones(n), valores_x])
y = valores_y.reshape(-1, 1)

# Fórmula matricial: β = (X'X)^(-1)X'y
XtX = np.dot(X.T, X)
XtX_inv = np.linalg.inv(XtX)
Xty = np.dot(X.T, y)
beta = np.dot(XtX_inv, Xty)

# Extrai intercepto (a) e inclinação (b)
a = beta[0][0]  # intercepto
b = beta[1][0]  # inclinação

print(f"Intercepto (a): {a:.4f}")
print(f"Inclinação (b): {b:.4f}")

# Cria o gráfico com plotnine (como mostrado nas aulas)
df = pd.DataFrame({"x": valores_x, "y": valores_y})

plot = (
    ggplot(df, aes("x", "y"))
    + geom_point()
    + geom_abline(intercept=a, slope=b)
    + ggsave("grafico.png")
)

print(plot)

