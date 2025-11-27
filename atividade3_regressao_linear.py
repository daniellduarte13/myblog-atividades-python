import numpy as np
import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_point,
    geom_abline,
    theme_bw,
)
from plotnine import ggsave


def calcular_regressao_linear(valores_x: np.ndarray, valores_y: np.ndarray):
    n = len(valores_x)
    X = np.column_stack([np.ones(n), valores_x])
    y = valores_y.reshape(-1, 1)

    xtx = X.T @ X
    xtx_inv = np.linalg.inv(xtx)
    xty = X.T @ y
    beta = xtx_inv @ xty

    intercepto = float(beta[0, 0])
    inclinacao = float(beta[1, 0])
    return intercepto, inclinacao


def criar_grafico_regressao(
    valores_x: np.ndarray,
    valores_y: np.ndarray,
    intercepto: float,
    inclinacao: float,
):
    df = pd.DataFrame({"x": valores_x, "y": valores_y})

    plot = (
        ggplot(df, aes("x", "y"))
        + geom_point(alpha=0.4, size=1.5)  # pontos mais suaves
        + geom_abline(intercept=intercepto, slope=inclinacao)  # reta
        + theme_bw()  # estética mais limpa
    )

    ggsave(plot, "docs/grafico.png", dpi=300)
    print("Gráfico salvo como docs/grafico.png")


if __name__ == "__main__":
    valores_x = np.loadtxt("X.txt")
    valores_y = np.loadtxt("y.txt")

    a, b = calcular_regressao_linear(valores_x, valores_y)

    print(f"Intercepto: {a:.4f}")
    print(f"Inclinação: {b:.4f}")

    criar_grafico_regressao(valores_x, valores_y, a, b)
