import argparse
import csv
import os
import re
import time
from dotenv import load_dotenv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv(".env")

DEFAULT_CODIGOS = [
    "2506", "2507", "2508", "2509", "2510", "8000", "8001", "7000", "7001",
    "107T", "107P", "34028", "34029", "34030"
]


def auth_session():
    s = requests.Session()
    token = os.getenv("SPTRANS_TOKEN")
    if not token:
        print("Aviso: variável SPTRANS_TOKEN não encontrada em .env. Tentando sem autenticação.")
        return s
    try:
        res = s.post(
            f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}", timeout=10
        )
        # API devolve 200 mesmo quando token ok; não checamos conteúdo aqui
    except Exception as e:
        print(f"Erro ao autenticar: {e}")
    return s


def fetch_paradas(session, codigo, retries=3, timeout=10):
    url = f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo}"
    for attempt in range(1, retries + 1):
        try:
            res = session.get(url, timeout=timeout)
            data = res.json()
            if isinstance(data, list):
                return {"codigo": codigo, "status": "ok", "count": len(data), "paradas": data}
            if isinstance(data, dict) and "Message" in data:
                return {"codigo": codigo, "status": "error", "message": data.get("Message")}
            return {"codigo": codigo, "status": "empty", "count": 0}
        except Exception as e:
            if attempt < retries:
                time.sleep(0.5 * attempt)
                continue
            return {"codigo": codigo, "status": "exception", "message": str(e)}


def buscar_por_termo(session, termo, limit=50):
    url = f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={termo}"
    try:
        res = session.get(url, timeout=10)
        data = res.json()
        if isinstance(data, list):
            # extrai códigos (campo 'cl') e remove duplicatas
            cods = []
            for item in data[:limit]:
                cl = item.get("cl")
                if cl and cl not in cods:
                    cods.append(cl)
            return cods
    except Exception:
        pass
    return []


def expand_range(range_str):
    # aceita formato "100-110" e retorna lista de códigos como strings
    m = re.match(r"^(\d+)-(\d+)$", range_str.strip())
    if not m:
        return []
    start, end = int(m.group(1)), int(m.group(2))
    if start > end:
        start, end = end, start
    return [str(i) for i in range(start, end + 1)]


def save_csv(results, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["codigo", "status", "count", "message"])
        for r in results:
            writer.writerow([r.get("codigo"), r.get("status"), r.get("count", ""), r.get("message", "")])


def main():
    parser = argparse.ArgumentParser(description="Testa códigos de linha na API do Olho Vivo SPTrans")
    parser.add_argument("--codes", help="Lista de códigos separados por vírgula (ex: 2506,2507)")
    parser.add_argument("--file", help="Arquivo com um código por linha")
    parser.add_argument("--pattern", help="Termo para busca rápida via endpoint Linha/Buscar (ex: 250)")
    parser.add_argument("--range", help="Intervalo numérico (ex: 100-110)")
    parser.add_argument("--exclude", help="Excluir códigos (vírgula-separados) ou @arquivo_com_codigos")
    parser.add_argument("--exclude-default", action="store_true", help="Excluir os códigos presentes em DEFAULT_CODIGOS")
    parser.add_argument("--parallel", type=int, default=8, help="Número de threads em paralelo")
    parser.add_argument("--output", help="Salvar resultados em CSV (ex: saida.csv)")
    parser.add_argument("--limit-search", type=int, default=50, help="Limite de resultados ao usar --pattern")
    parser.add_argument("--verbose", action="store_true", help="Modo verboso")

    args = parser.parse_args()

    session = auth_session()

    # construir lista de códigos a testar
    codigos = []
    if args.codes:
        codigos.extend([c.strip() for c in args.codes.split(",") if c.strip()])
    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        codigos.append(line)
        except Exception as e:
            print(f"Erro ao ler arquivo {args.file}: {e}")
    if args.range:
        codigos.extend(expand_range(args.range))
    if args.pattern:
        encontrados = buscar_por_termo(session, args.pattern, limit=args.limit_search)
        if encontrados:
            codigos.extend(encontrados)

    # processar exclusões
    excludes = set()
    if args.exclude:
        ex = args.exclude.strip()
        if ex.startswith("@"):
            fn = ex[1:]
            try:
                with open(fn, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            excludes.add(line)
            except Exception as e:
                print(f"Aviso: não foi possível ler arquivo de exclusão {fn}: {e}")
        else:
            for c in ex.split(","):
                c = c.strip()
                if c:
                    excludes.add(c)

    if args.exclude_default:
        excludes.update(DEFAULT_CODIGOS)

    # se nenhuma opção foi passada, usa a lista padrão
    if not codigos:
        codigos = DEFAULT_CODIGOS.copy()

    # remover duplicatas, manter a ordem
    seen = set()
    codigos_uniq = []
    for c in codigos:
        if c not in seen:
            seen.add(c)
            codigos_uniq.append(c)

    # aplicar exclusões finais
    if excludes:
        codigos_uniq = [c for c in codigos_uniq if c not in excludes]

    print(f"Testando {len(codigos_uniq)} códigos de linha...\n")

    results = []
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futures = {ex.submit(fetch_paradas, session, codigo): codigo for codigo in codigos_uniq}
        for fut in as_completed(futures):
            r = fut.result()
            results.append(r)
            if args.verbose:
                print(r)
            else:
                if r.get("status") == "ok":
                    print(f"✓ {r['codigo']}: {r.get('count',0)} paradas")
                elif r.get("status") in ("empty", "error"):
                    msg = r.get("message") or "Sem paradas"
                    print(f"✗ {r['codigo']}: {msg}")
                else:
                    print(f"✗ {r['codigo']}: {r.get('message')}")

    valid = [r for r in results if r.get('status') == 'ok' and r.get('count', 0) > 0]
    if valid:
        print("\nLinhas válidas encontradas:")
        for r in valid:
            print(f"  {r.get('codigo')}: {r.get('count', 0)} paradas")
    else:
        print(f"\nLinhas válidas encontradas: []")

    if args.output:
        save_csv(results, args.output)
        print(f"Resultados salvos em {args.output}")


if __name__ == '__main__':
    main()
