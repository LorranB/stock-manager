import pdfplumber
import re


def normalizar_nome(nome):

    ram = re.search(
        r'(\d+)GB RAM',
        nome,
        re.IGNORECASE
    )

    memorias = re.findall(
        r'(\d+)\s*GB',
        nome,
        re.IGNORECASE
    )

    ram_txt = ram.group(1) if ram else ""

    memoria_txt = ""

    if memorias:
        memoria_txt = memorias[-1]

    nome_base = re.sub(
        r'\d+GB RAM',
        '',
        nome,
        flags=re.IGNORECASE
    )

    if memoria_txt:

        nome_base = re.sub(
            rf'{memoria_txt}\s*GB',
            '',
            nome_base,
            count=1,
            flags=re.IGNORECASE
        )

    nome_base = " ".join(
        nome_base.split()
    )

    if memoria_txt and ram_txt:

        return (
            f"{nome_base} "
            f"{memoria_txt}GB/{ram_txt}GB"
        )

    return nome_base


def separar_nome_cor(parte_nome):

    match = re.search(
        r'(\d+\s*GB)(?!.*\d+\s*GB)',
        parte_nome,
        re.IGNORECASE
    )

    if not match:
        return parte_nome, ""

    fim_memoria = match.end()

    nome_produto = parte_nome[:fim_memoria].strip()

    cor = parte_nome[fim_memoria:].strip()

    return nome_produto, cor


def ler_estoque_pdf(caminho_pdf):

    produtos = []

    texto = ""

    with pdfplumber.open(caminho_pdf) as pdf:

        for pagina in pdf.pages:

            pagina_texto = pagina.extract_text()

            if pagina_texto:

                texto += "\n" + pagina_texto

    linhas = texto.split("\n")

    for linha in linhas:

        linha = linha.strip()

        if not linha:
            continue

        if linha.startswith("Nome"):
            continue

        if linha.startswith("Quantidade"):
            continue

        numeros = re.findall(
            r'[\d\.]+,\d+',
            linha
        )

        if len(numeros) < 5:
            continue

        try:

            estoque = float(
                numeros[0].replace(",", ".")
            )

            if estoque <= 0:
                continue

            custo = float(
                numeros[1]
                .replace(".", "")
                .replace(",", ".")
            )

            preco_venda = float(
                numeros[3]
                .replace(".", "")
                .replace(",", ".")
            )

            match = re.search(
                r'\s\d+,\d+\s',
                linha
            )

            if not match:
                continue

            parte_nome = linha[
                :match.start()
            ].strip()

            nome_produto, cor = separar_nome_cor(
                parte_nome
            )

            produtos.append({

                "nome": normalizar_nome(
                    nome_produto
                ),

                "cor": cor,

                "estoque": int(
                    estoque
                ),

                "custo": custo,

                "preco_atual": preco_venda

            })

        except Exception as erro:

            print(
                f"\nErro ao processar:\n{linha}\n{erro}\n"
            )

    return produtos
