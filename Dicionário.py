# Desenvolvido por Daniel - 2º Semestre Engenharia de Computação
import requests

API_BASE = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def buscar_palavra(word):
    """Busca a palavra na API e retorna algumas informações básicas."""
    try:
        resposta = requests.get(API_BASE + word, timeout=5)
        if resposta.status_code != 200:
            return None
        dados = resposta.json()
        entrada = dados[0]

        fonetica = entrada.get("phonetic", "")
        if not fonetica and entrada.get("phonetics"):
            fonetica = entrada["phonetics"][0].get("text", "")

        definicao = ""
        if entrada.get("meanings"):
            defs = entrada["meanings"][0].get("definitions", [])
            if defs:
                definicao = defs[0].get("definition", "")

        return {
            "word": entrada.get("word", word),
            "phonetic": fonetica,
            "definition": definicao
        }
    except Exception:
        return None

def main():
    letra = input("Digite uma letra (A-Z): ").strip().lower()

    palavras = ["try", "trust", "tree", "train", "art", "play", "fly", "byte"]

    palavras_filtradas = [p for p in palavras if p.startswith(letra)]

    if not palavras_filtradas:
        print("Nenhuma palavra encontrada com essa letra.")
        return

    # Pega apenas uma palavra qualquer que comece com a letra
    palavra_escolhida = palavras_filtradas[0]
    
    print(f"\nPalavra que começa com '{letra}':\n")
    resultado = buscar_palavra(palavra_escolhida)
    if resultado:
        print(f"- {resultado['word']} {resultado['phonetic']}")
        print(f"  Definição: {resultado['definition']}\n")
    else:
        print(f"- {palavra_escolhida} (não encontrada)\n")

if __name__ == "__main__":
    main()
