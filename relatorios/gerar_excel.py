from openpyxl import Workbook
from datetime import datetime


def gerar_excel(relatorio):

    wb = Workbook()

    ws = wb.active

    ws.title = "Precificação"

    ws.append([

        "Produto",
        "Preço Atual",
        "Concorrente",
        "Preço Sugerido",
        "Lucro",
        "Status"

    ])

    for item in relatorio:

        ws.append([

            item["produto"],
            item["preco_atual"],
            item["concorrente"],
            item["preco_sugerido"],
            item["lucro"],
            item["status"]

        ])

    nome = datetime.now().strftime(
        "output/precificacao_%d-%m-%Y.xlsx"
    )

    wb.save(nome)
    
    return nome

    print(
        f"\n✅ Excel gerado: {nome}"
    )
