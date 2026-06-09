from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
    
BASE_URL = "https://boadica.com.br"


def normalizar(texto):
    return (
        texto.upper()
        .replace(" ", "")
        .replace("-", "")
    )


def extrair_modelo(nome):

    nome = normalizar(nome)

    partes = nome.split()

    modelo = []

    for parte in partes:

        if "GB" in parte:
            break

        modelo.append(parte)

    return "".join(modelo)

def extrair_modelo_titulo(titulo):

    titulo = normalizar(titulo)

    titulo = titulo.replace(
        "POCO(BYXIAOMI)/",
        "POCO"
    )

    titulo = titulo.replace(
        "XIAOMI(MI)/",
        ""
    )

    return titulo

def produto_compativel(nome_estoque, titulo_boadica):

    estoque = normalizar(nome_estoque)
    titulo = normalizar(titulo_boadica)

    # Extrai RAM e armazenamento do estoque
    partes = estoque.split("/")

    if len(partes) < 2:
        return False

    armazenamento = partes[0][-5:]  # ex: 256GB
    ram = partes[1][:3]             # ex: 8GB

    if armazenamento not in titulo:
        return False

    if ram not in titulo:
        return False

    # Verifica PRO
    # PRO MAX

    if "PROMAX" in estoque:

        if "PROMAX" not in titulo:
            return False
    else:
        if "PROMAX" in titulo:
            return False
    # PRO

    if "PRO" in estoque:

        if "PRO" not in titulo:
            return False
    else:
        if "PRO" in titulo:
            return False

    # Verifica 5G
    if "5G" in estoque and "5G" not in titulo:
        return False


    # Verifica modelo

    modelo_estoque = extrair_modelo(
    nome_estoque
    )
    print("MODELO ESTOQUE:", modelo_estoque)
    print("TITULO:", titulo)
    if modelo_estoque not in titulo:
        return False

        print(
        "MODELO:",
        modelo_estoque
    )
    return True


def buscar_produto(driver, nome_produto):

    termo = nome_produto.replace(
        " ",
        "%20"
    )

    url = (
        f"https://boadica.com.br/"
        f"busca-resultado?termo={termo}"
    )

    driver.get(url)

    try:

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".produto")
            )
        )

    except:

        return []

    produtos = driver.find_elements(
        By.CSS_SELECTOR,
        ".produto"
    )

    resultados = []

    for produto in produtos:

        try:

            titulo = produto.find_element(
                By.CSS_SELECTOR,
                "h3 a"
            ).text

            link = produto.find_element(
                By.CSS_SELECTOR,
                "h3 a"
            ).get_attribute("href")

            if produto_compativel(
                nome_produto,
                titulo
            ):

                resultados.append({

                    "titulo": titulo,
                    "url": link

                })

        except:
            continue

    return resultados

