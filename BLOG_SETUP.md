# Publicar o blog no GitHub Pages

Este guia mostra passos mínimos para publicar seu blog Quarto no GitHub Pages usando o workflow fornecido em `.github/workflows/quarto-render.yml`.

1) Crie um repositório no GitHub
- No GitHub, clique em **New repository** e escolha um nome (ex.: `trabalho-python`).

2) Conecte o repositório local ao remoto e faça push
Abra PowerShell na raiz do projeto e execute:

```powershell
# se ainda não for um repositório git
git init
git add .
git commit -m "Prepare blog for GitHub Pages"

git branch -M main
# substitua pelo URL do repositório que você criou
git remote add origin https://github.com/<SEU_USUARIO>/<NOME_DO_REPO>.git
git push -u origin main
```

3) Verifique o workflow
- O arquivo `.github/workflows/quarto-render.yml` renderiza o site e publica a pasta `docs/` no branch `gh-pages` sempre que você der push para `main`.

4) Aguardar o GitHub Actions
- No GitHub vá em **Actions** e verifique o job `Render and deploy Quarto site`. Aguarde ele rodar com sucesso.

5) Verificar URL pública
- Depois que o workflow finalizar, o site ficará disponível em:
  `https://<SEU_USUARIO>.github.io/<NOME_DO_REPO>/`

6) Ajustes finais (opcional)
- Se quiser usar um domínio customizado, adicione `CNAME` ao branch `gh-pages` ou nas configurações do repositório.
- Se preferir que o site seja servido a partir da pasta `docs` no branch `main` em vez de `gh-pages`, altere as configurações do workflow (deploy) e nas Settings > Pages escolha `main` / `/docs`.


Se quiser, eu crio o commit inicial `.github/...` para você já ter o arquivo pronto (já criei localmente neste workspace). O próximo passo é você criar o repositório no GitHub e dar push; depois eu posso ajudar a verificar o Actions e o link público.
