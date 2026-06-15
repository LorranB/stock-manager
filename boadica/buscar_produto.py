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

    nome = nome.upper()

    partes = nome.split()

    modelo = []

    for parte in partes:

        if "/" in parte:
            break

        if "GB" in parte:
            break

        modelo.append(
            normalizar(parte)
        )

    modelo_final = "".join(modelo)

    print("EXTRAINDO:", nome)
    print("MODELO EXTRAIDO:", modelo_final)

    return modelo_final

def produto_compativel(nome_estoque, titulo_boadica):

    estoque = normalizar(nome_estoque)
    titulo = normalizar(titulo_boadica)

    # Extrai armazenamento e RAM diretamente do nome do estoque
    memorias = re.findall(
        r'(\d+)GB',
        nome_estoque.upper()
    )

    if len(memorias) < 2:
        return False

    armazenamento = memorias[0] + "GB"
    ram = memorias[1] + "GB"

    if armazenamento not in titulo:
        return False

    if ram not in titulo:
        return False

    # Verifica PRO MAX
    if "PROMAX" in estoque:

        if "PROMAX" not in titulo:
            return False

    else:

        if "PROMAX" in titulo:
            return False

    # Verifica PRO
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
    print("ARMAZENAMENTO:", armazenamento)
    print("RAM:", ram)

    # REDMI PAD 2
    if modelo_estoque.startswith("REDMIPAD2") and "PRO" not in modelo_estoque:

        if "PADSE" in titulo:
            return False

        if "PAD2PRO" in titulo:
            return False

        if "REDMIPAD2" not in titulo:
            return False


    # REDMI PAD 2 PRO
    elif "REDMIPAD2PRO" in modelo_estoque:

        if "REDMIPAD2PRO" not in titulo:
            return False


    # REDMI PAD SE
    elif modelo_estoque.startswith("REDMIPADSE"):

        if "REDMIPADSE" not in titulo:
            return False


    else:

        titulo_limpo = titulo

        titulo_limpo = titulo_limpo.replace(
            "POCO(BYXIAOMI)/POCO",
            "POCO"
        )

        titulo_limpo = titulo_limpo.replace(
            "POCO(BYXIAOMI)/",
            "POCO"
        )

        titulo_limpo = titulo_limpo.replace(
            "REALME/",
            "REALME"
        )

        titulo_limpo = titulo_limpo.replace(
            "XIAOMI(MI)/",
            ""
        )

        if modelo_estoque not in titulo_limpo:
            return False

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

