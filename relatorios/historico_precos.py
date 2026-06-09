import csv
import os
from datetime import datetime


ARQUIVO = "output/historico_precos.csv"


def salvar_historico(relatorio):

    existe = os.path.exists(
        ARQUIVO
    )

    with open(

        ARQUIVO,

        "a",

        newline="",

        encoding="utf-8"

    ) as arquivo:

        writer = csv.writer(
            arquivo
        )

        if not existe:

            writer.writerow([

                "data",
                "produto",
                "preco_atual",
                "concorrente",
                "preco_sugerido",
                "lucro"

            ])

        hoje = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )

        for item in relatorio:

            writer.writerow([

                hoje,

                item["produto"],

                item["preco_atual"],

                item["concorrente"],

                item["preco_sugerido"],

                item["lucro"]

            ])

    print(
        "\n✅ Histórico atualizado!"
    )
