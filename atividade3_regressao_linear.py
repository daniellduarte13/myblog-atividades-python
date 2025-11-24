# Atividade 3: Regressão Linear
# Calcula regressão linear usando fórmula matricial: β = (X'X)^(-1)X'y

import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_point, geom_abline

# Lê os dados dos arquivos X.txt e y.txt
with open("X.txt", 'r') as f:
    valores_x = np.array([float(linha.strip()) for linha in f.readlines()])

with open("y.txt", 'r') as f:
    valores_y = np.array([float(linha.strip()) for linha in f.readlines()])

# Calcula a regressão linear usando fórmula matricial
n = len(valores_x)
# Se os dados forem muito grandes, usar float32 para economizar memória (útil em VMs)
if n > 100_000:
    valores_x = valores_x.astype(np.float32)
    valores_y = valores_y.astype(np.float32)

# Cria a matriz de design X (primeira coluna: 1s para intercepto, segunda: valores de x)
X = np.column_stack([np.ones_like(valores_x), valores_x])

# Usa np.linalg.lstsq para maior estabilidade numérica e performance
# beta terá forma (2,) quando y for 1D
beta, *_ = np.linalg.lstsq(X, valores_y, rcond=None)

# Extrai intercepto (a) e inclinação (b)
# `np.linalg.lstsq` normalmente retorna `beta` como vetor 1D quando y é 1D
a = float(beta[0])  # intercepto
b = float(beta[1])  # inclinação

print(f"Intercepto (a): {a:.4f}")
print(f"Inclinação (b): {b:.4f}")

# Cria o gráfico com plotnine (como mostrado nas aulas)
df = pd.DataFrame({"x": valores_x, "y": valores_y})

plot = (
    ggplot(df, aes("x", "y"))
    + geom_point()
    + geom_abline(intercept=a, slope=b)
)

# Salva o gráfico usando o método do objeto `ggplot`
plot.save("grafico.png")

print(plot)
