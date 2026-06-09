from collections import defaultdict
from datetime import datetime

CORES = {
    "Preto": "Black",
    "Azul": "Blue",
    "Verde": "Green",
    "Cinza": "Gray",
    "Branco": "White",
    "Dourado": "Gold",
    "Prata": "Silver",
    "Roxo": "Purple",
    "Púrpura": "Purple",
    "Lilás": "Lilac",
    "Rosa": "Pink",
    "Vermelho": "Red",
    "Laranja": "Orange",
    "Amarelo": "Yellow",
    "Marrom": "Brown",
    "Bege": "Beige",
    "Grafite": "Graphite",
    "Titânio": "Titanium",
    "Titanium": "Titanium"
}


def definir_categoria(nome):

    nome = nome.upper()

    if "PAD" in nome:
        return "TABLETS"

    elif nome.startswith("REDMI"):
        return "REDMI"

    elif nome.startswith("POCO"):
        return "POCO"

    elif nome.startswith("REALME"):
        return "REALME"

    return "OUTROS"


def gerar_lista(produtos):

    grupos = defaultdict(
        lambda: {
            "cores": set(),
            "preco": None
        }
    )

    for produto in produtos:

        if produto.get(
            "estoque",
            1
        ) <= 0:
            continue

        nome = produto.get(
            "nome",
            produto.get("produto")
        )

        preco = produto.get(
            "preco_sugerido",
            produto.get(
                "preco_atual",
                produto.get(
                    "preco",
                    0
                )
            )
        )

        grupos[nome]["preco"] = preco

        cor = produto.get("cor", "")

        if cor:

            grupos[nome]["cores"].add(
                CORES.get(cor, cor)
            )

    categorias = {
        "TABLETS": [],
        "REDMI": [],
        "POCO": [],
        "REALME": [],
        "OUTROS": []
    }

    for nome in grupos:

        categoria = definir_categoria(nome)

        categorias[categoria].append(nome)

    linhas = []

    data = datetime.now().strftime(
        "%d.%m.%Y"
    )

    linhas.append(
        f"Atualizado {data}"
    )

    linhas.append("")

    linhas.append(
        "⚠️ LACRADOS ⚠️"
    )

    linhas.append(
        "📌 RETIRADA CENTRO RJ"
    )

    linhas.append(
        "🚚 Entregamos para todo Brasil"
    )

    linhas.append(
        "💳 Parcelamento disponível"
    )

    ordem = [
        ("TABLETS", "📱 Tablets"),
        ("REDMI", "📱 REDMI"),
        ("POCO", "📱 POCO"),
        ("REALME", "📱 REALME")
    ]

    for chave, titulo in ordem:

        if not categorias[chave]:
            continue

        linhas.append("")
        linhas.append(
            "━━━━━━━━━━━━━━━"
        )

        linhas.append(
            titulo
        )

        linhas.append(
            "━━━━━━━━━━━━━━━"
        )

        linhas.append("")

        for nome in sorted(
            categorias[chave]
        ):

            linhas.append(
                f"📱 {nome}"
            )

            for cor in sorted(
                grupos[nome]["cores"]
            ):

                linhas.append(
                    f"🚥 {cor}"
                )

            preco = round(
                grupos[nome]["preco"]
            )

            preco = (
                f"{preco:,}"
                .replace(",", ".")
            )

            linhas.append(
                f"💵 ${preco}"
            )

            linhas.append("")

    return "\n".join(linhas)


def salvar_lista_whatsapp(
    produtos_pdf,
    relatorio
):

    precos_sugeridos = {

        item["produto"].upper().strip(): item

        for item in relatorio

    }
                

    produtos_finais = relatorio.copy()

    for produto in produtos_pdf:

        nome_produto = produto["nome"].upper().strip()

        if nome_produto in precos_sugeridos:

            produto["preco_sugerido"] = (
                precos_sugeridos[nome_produto]["preco_sugerido"]
            )

        else:

            produto["preco_sugerido"] = (
                produto["preco_atual"]
            )

            produtos_finais.append({

                "nome": produto["nome"],

                "cor": produto.get(
                    "cor",
                    ""
                ),

                "estoque": produto.get(
                    "estoque",
                    1
                ),

                "preco_atual": produto[
                    "preco_atual"
                ]

            })

    texto = gerar_lista(
        produtos_finais
    )

    with open(

        "output/lista_whatsapp.txt",

        "w",

        encoding="utf-8"

    ) as arquivo:

        arquivo.write(
            texto
        )

    print(
        "\n✅ Lista WhatsApp gerada com sucesso!"
    )

    print(
        "📄 Arquivo: output/lista_whatsapp.txt"
    )
