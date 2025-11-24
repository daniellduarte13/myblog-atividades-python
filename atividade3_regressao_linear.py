import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_point, geom_abline

with open("X.txt", 'r') as f:
    valores_x = np.array([float(linha.strip()) for linha in f.readlines()])

with open("y.txt", 'r') as f:
    valores_y = np.array([float(linha.strip()) for linha in f.readlines()])

n = len(valores_x)
if n > 100_000:
    valores_x = valores_x.astype(np.float32)
    valores_y = valores_y.astype(np.float32)

X = np.column_stack([np.ones_like(valores_x), valores_x])

beta, *_ = np.linalg.lstsq(X, valores_y, rcond=None)

a = float(beta[0])
b = float(beta[1])

print(f"Intercepto (a): {a:.4f}")
print(f"Inclinação (b): {b:.4f}")

df = pd.DataFrame({"x": valores_x, "y": valores_y})

plot = (
    ggplot(df, aes("x", "y"))
    + geom_point()
    + geom_abline(intercept=a, slope=b)
)

plot.save("grafico.png")

print(plot)
