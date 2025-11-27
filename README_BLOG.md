# Blog Quarto - Trabalho Individual

Este diretório contém a estrutura completa para o blog do trabalho individual.

## Estrutura de Arquivos

```
.
├── _quarto.yml          # Configuração do projeto Quarto
├── index.qmd            # Página inicial do blog
├── atividade1.qmd       # Post da Atividade 1
├── atividade2.qmd       # Post da Atividade 2
├── atividade3.qmd       # Post da Atividade 3
├── styles.css           # Estilos personalizados
├── atividade1_cotacao_dolar.py
├── atividade2_monitoramento_onibus.py
└── atividade3_regressao_linear.py
```

## Como Publicar no GitHub Pages

### 1. Instalar o Quarto

Baixe e instale o Quarto em: https://quarto.org/docs/get-started/

### 2. Renderizar o Blog

No terminal, execute:

```bash
quarto render
```

Isso gerará os arquivos HTML na pasta `docs/`.

### 3. Configurar o GitHub Pages

1. Crie um repositório no GitHub
2. Faça upload dos arquivos (incluindo a pasta `docs/`)
3. Vá em Settings > Pages
4. Configure a source como "Deploy from a branch"
5. Selecione a branch `main` e a pasta `/docs`
6. Salve

### 4. Atualizar o Blog

Sempre que fizer alterações:

```bash
quarto render
git add .
git commit -m "Atualização do blog"
git push
```

O GitHub Pages atualizará automaticamente.

## Dependências Python

Para executar os scripts Python, instale as dependências:

```bash
pip install requests plotly folium python-dotenv numpy pandas plotnine
```

## Arquivo .env

Crie um arquivo `.env` na raiz do projeto com:

```
SPTRANS_TOKEN=290ec966b5f73bb99bfa03cec172ccdcc37237665c8b6a0e2b74725b2d1a8f34
```

**IMPORTANTE**: Adicione `.env` ao `.gitignore` para não versionar o token!

