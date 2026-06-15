import os
from datetime import datetime

def gerar_relatorio(
    relatorio,
    nao_encontrados,
    sem_oferta_centro
):

    # Remove produtos duplicados
    relatorio_unico = []
    vistos = set()

    for item in relatorio:

        produto = item["produto"]

        if produto not in vistos:

            vistos.add(produto)

            relatorio_unico.append(item)

    relatorio = relatorio_unico

    nao_encontrados = list(
        dict.fromkeys(nao_encontrados)
    )

    sem_oferta_centro = list(
        dict.fromkeys(sem_oferta_centro)
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    with open(
        "output/relatorio_precificacao.txt",
        "w",
        encoding="utf-8"
    ) as f:

        agora = datetime.now()

        f.write(
            "RELATÓRIO DE PRECIFICAÇÃO\n"
        )

        f.write(
            f"Gerado em: "
            f"{agora.strftime('%d/%m/%Y %H:%M:%S')}\n"
        )

        f.write(
            "=" * 60 + "\n\n"
        )

        f.write(
            "RELATÓRIO DE PRECIFICAÇÃO\n"
        )

        f.write(
            "=" * 60 + "\n\n"
        )

        aumentar = 0
        reduzir = 0
        manter = 0

        for item in relatorio:

            if item["preco_sugerido"] > item["preco_atual"]:
                aumentar += 1

            elif item["preco_sugerido"] < item["preco_atual"]:
                reduzir += 1

            else:
                manter += 1

        f.write(
            "RESUMO GERAL\n"
        )

        f.write(
            "=" * 60 + "\n"
        )

        f.write(
            f"Produtos analisados: "
            f"{len(relatorio)}\n"
        )

        f.write(
            f"⬆ Aumentar preço: "
            f"{aumentar}\n"
        )

        f.write(
            f"⬇ Reduzir preço: "
            f"{reduzir}\n"
        )

        f.write(
            f"➡ Manter preço: "
            f"{manter}\n"
        )

        f.write(
            f"❌ Não encontrados: "
            f"{len(nao_encontrados)}\n"
        )

        f.write(
            f"⚠ Sem oferta Centro RJ: "
            f"{len(sem_oferta_centro)}\n"
        )

        f.write(
            "\n" + "=" * 60 + "\n\n"
        )

        for item in relatorio:

            f.write(
                f"{item['produto']}\n"
            )

            f.write(
                f"Concorrente: "
                f"R${item['concorrente']:.2f}\n"
            )

            f.write(
                f"Preço Atual: "
                f"R${item['preco_atual']:.2f}\n"
            )

            f.write(
                f"Preço Sugerido: "
                f"R${item['preco_sugerido']:.2f}\n"
            )

            f.write(
                f"Lucro: "
                f"R${item['lucro']:.2f}\n"
            )
            if item["preco_sugerido"] > item["preco_atual"]:

                acao = (
                    f"⬆ AUMENTAR "
                    f"R$ {item['preco_sugerido'] - item['preco_atual']:.2f}"
                )

            elif item["preco_sugerido"] < item["preco_atual"]:

                acao = (
                    f"⬇ REDUZIR "
                    f"R$ {item['preco_atual'] - item['preco_sugerido']:.2f}"
                )

            else:

                acao = "➡ MANTER PREÇO"
                
            f.write(
                f"Status: "
                f"{item['status']}\n"
            )

            f.write(
                f"Ação: "
                f"{acao}\n"
            )

            f.write(
                "-" * 40 + "\n"
            )

        f.write("\n\n")

        f.write(
            "APARELHOS NÃO ENCONTRADOS\n"
        )

        f.write(
            "=" * 40 + "\n"
        )

        if not nao_encontrados:

            f.write("Nenhum\n")

        else:

            for aparelho in nao_encontrados:

                f.write(
                    f"❌ {aparelho}\n"
                )

        f.write("\n\n")

        f.write(
            "SEM OFERTA NO CENTRO RJ\n"
        )

        f.write(
            "=" * 40 + "\n"
        )

        if not sem_oferta_centro:

            f.write("Nenhum\n")

        else:

            for aparelho in sem_oferta_centro:

                f.write(
                    f"⚠ {aparelho}\n"
                )
    
    print(
        "\n✅ Relatório de precificação gerado com sucesso!"
    )
    print(
        "📄 Arquivo: relatorio_precificacao.txt"
    )
