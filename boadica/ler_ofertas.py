import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def converter_preco(texto):

    match = re.search(
        r'(\d{1,3}(?:\.\d{3})*,\d{2})',
        texto
    )

    if not match:
        return 0

    preco = match.group(1)

    preco = preco.replace(".", "")
    preco = preco.replace(",", ".")

    return float(preco)


def eh_centro_rj(texto):

    txt = texto.upper()

    return (
        "CENTRO" in txt
        and "RIO DE JANEIRO" in txt
        and "NITEROI" not in txt
        and "DUQUE DE CAXIAS" not in txt
        and "NOVA IGUACU" not in txt
    )


def ler_ofertas(driver, url):

    driver.get(url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".preco-loja")
        )
    )

    ofertas = []

    precos = driver.find_elements(
        By.CSS_SELECTOR,
        ".preco-loja"
    )

    for preco in precos:

        try:

            linha = preco.find_element(
                By.XPATH,
                "./.."
            )

            texto = linha.text

            linhas = texto.split("\n")

            loja = linhas[0]

            preco_float = converter_preco(texto)

            ofertas.append({
                "loja": loja,
                "texto": texto,
                "preco": preco_float,
                "centro_rj": eh_centro_rj(texto)
            })

        except Exception:
            pass

    return ofertas
