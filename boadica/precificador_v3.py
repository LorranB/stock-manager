def classificar_lucro(lucro):

    if lucro < 0:
        return "⛔ ABAIXO DO CUSTO"

    if lucro < 10:
        return "🔴 CRÍTICO"

    if lucro < 20:
        return "🟡 BAIXO"

    if lucro < 40:
        return "🟢 OK"

    return "🔵 BOM"


def calcular_preco(concorrente, custo):

    if concorrente < 1000:
        sugerido = concorrente - 30
    else:
        sugerido = concorrente - 50

    # Nunca vender abaixo do custo
    if sugerido < custo:
        sugerido = custo
    
    lucro = round(sugerido - custo, 2)

    sugerido = round(sugerido / 10) * 10

    lucro = round(sugerido - custo, 2)

    
    return {
        "concorrente": concorrente,
        "custo": custo,
        "preco_sugerido": sugerido,
        "lucro": lucro,
        "status": classificar_lucro(lucro)
    }
