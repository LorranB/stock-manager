from boadica.navegador import criar_driver
from estoque.leitor_estoque import ler_estoque_pdf
from boadica.buscar_produto import buscar_produto
from boadica.ler_ofertas import ler_ofertas
from boadica.precificador_v3 import calcular_preco
from relatorios.gerar_relatorio import gerar_relatorio
from relatorios.gerador_whatsapp import salvar_lista_whatsapp
from relatorios.gerar_excel import gerar_excel
from relatorios.historico_precos import salvar_historico

NAO_ENCONTRADOS = []

SEM_OFERTA_CENTRO = []

RELATORIO = []

def obter_menor_preco_centro(ofertas):

    ofertas_centro = [

        o for o in ofertas

        if o["centro_rj"]
        and o["preco"] > 0

    ]

    if not ofertas_centro:
        return None

    return min(
        ofertas_centro,
        key=lambda x: x["preco"]
    )


def analisar_produto(driver, produto):

    print("\n" + "=" * 60)

    print(produto["nome"])

    try:

        resultados = buscar_produto(
            driver,
            produto["nome"]
        )

        if not resultados:

            print("❌ Produto não encontrado")

            NAO_ENCONTRADOS.append(
                produto["nome"]
            )

            return

        menor = None

        for resultado in resultados:

            try:

                print(
                    f"Testando: "
                    f"{resultado['titulo']}"
                )

                ofertas = ler_ofertas(
                    driver,
                    resultado["url"]
                )

                menor_local = obter_menor_preco_centro(
                    ofertas
                )

                if menor_local:

                    if (
                        menor is None
                        or menor_local["preco"] < menor["preco"]
                    ):

                        menor = menor_local

            except Exception as erro:

                print(
                    f"⚠ Erro em "
                    f"{resultado['titulo']}"
                )

                continue

        if not menor:

            print(
                "⚠ Nenhuma oferta do Centro RJ"
            )

            SEM_OFERTA_CENTRO.append(
                produto["nome"]
            )

            return

        analise = calcular_preco(
            
            concorrente=menor["preco"],
            
            custo=produto["custo"]
        )

        print(
            f"Preço atual: "
            f"R${produto['preco_atual']:.2f}"
        )

        print(
            f"Concorrente: "
            f"R${menor['preco']:.2f}"
        )

        print(
            f"Preço sugerido: "
            f"R${analise['preco_sugerido']:.2f}"
        )

        print(
            f"Lucro: "
            f"R${analise['lucro']:.2f}"
        )

        print(
            f"Status: "
            f"{analise['status']}"
        )

        print(
            f"Loja: "
            f"{menor['loja']}"
        )

    except Exception as erro:

        print(
            f"Erro: {erro}"
        )

        return

    RELATORIO.append({

        "produto": produto["nome"],

        "cor": produto["cor"],

        "estoque": produto["estoque"],

        "concorrente": menor["preco"],

        "preco_atual": produto["preco_atual"],

        "preco_sugerido": analise["preco_sugerido"],

        "lucro": analise["lucro"],

        "status": analise["status"]

    })

def executar(
    pdf_estoque,
    callback_log=None,
    callback_progresso=None
):

    RELATORIO.clear()
    NAO_ENCONTRADOS.clear()
    SEM_OFERTA_CENTRO.clear()

    driver = criar_driver()

    produtos = ler_estoque_pdf(
        pdf_estoque
    )
    vistos = set()
    produtos_filtrados = []

    for p in produtos:

        chave = (
            p["nome"],
            p.get("cor", "")
        )

        if chave not in vistos:

            vistos.add(chave)

            produtos_filtrados.append(p)

    produtos = produtos_filtrados
    
    print(
        f"\nProdutos encontrados: "
        f"{len(produtos)}"
    )

    total = len(produtos)

    for i, produto in enumerate(produtos):

        if callback_log:
            callback_log(
                f"🔎 {produto['nome']}"
            )

        analisar_produto(
            driver,
            produto
        )

        if callback_progresso:
            callback_progresso(
                i + 1,
                total
            )

    gerar_relatorio(
        RELATORIO,
        NAO_ENCONTRADOS,
        SEM_OFERTA_CENTRO
    )

    gerar_excel(
        RELATORIO
    )
    
    salvar_historico(
        RELATORIO
    )
    
    salvar_lista_whatsapp(
        produtos,
        RELATORIO
    )

    if callback_log:
        callback_log(
            "✅ Arquivos gerados com sucesso!"
        )
    
    if driver:
        driver.quit()

    print(
        "\n🎉 Processo finalizado com sucesso!"
    )

if __name__ == "__main__":
    executar("estoque.pdf")
