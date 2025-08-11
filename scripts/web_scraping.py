# Importa as bibliotecas necessárias:
# - BeautifulSoup: para fazer o parsing do HTML
# - requests: para fazer requisições HTTP
# - pandas: para manipulação e exportação de dados em formato tabular (como CSV)
# - urljoin: para construção de URLs completas a partir de URLs relativas
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin

# URL base do site que contém os livros
url = "https://books.toscrape.com/"
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    html_content = response.text  # Armazena o conteúdo HTML da página
    # print("Pagina obtida com sucesso")
else:
    # Se houver erro, imprime o código de status HTTP
    print(f"Erro ao acessar pagina. codigo de saida: {response.status_code}")

# Cria o objeto BeautifulSoup para fazer parsing do HTML da página principal
soup = BeautifulSoup(html_content, "html.parser")


# Função para extrair os links do menu de categorias
def extrair_Menu():
    links_menu = []

    # Procura todas as tags <a> na página e filtra aquelas que levam a categorias de livros
    for link in soup.find_all("a"):
        if "catalogue/category/books/" in link.get("href"):
            texto = link.get_text().strip()  # Nome da categoria
            href = link.get("href")  # URL relativa da categoria
            # Constrói a URL absoluta e adiciona à lista
            links_menu.append((texto, "http://books.toscrape.com/" + href))

    print("categorias extraidas com sucesso")
    return links_menu


# Função que extrai os dados dos livros de uma página de categoria (incluindo paginação)
def extrair_livros_pagina(categoria, url_base):
    livros = []
    proxima_url = url_base  # Inicializa com a URL da primeira página da categoria

    while proxima_url:
        # Requisição da página atual
        resposta = requests.get(proxima_url)
        soup = BeautifulSoup(resposta.text, "html.parser")

        # Para cada livro na página, extrai as informações desejadas
        for item in soup.select("article.product_pod"):
            titulo = item.h3.a["title"]  # Título do livro
            link = urljoin(proxima_url, item.h3.a["href"])  # URL da página do livro
            preco = item.select_one("p.price_color").text.strip()  # Preço
            disponibilidade = item.select_one(
                "p.instock.availability"
            ).text.strip()  # Disponibilidade

            # Extrai o número de estrelas a partir das classes CSS do rating
            classe_rating = item.select_one("p.star-rating")["class"]
            rating_str = [c for c in classe_rating if c != "star-rating"][
                0
            ]  # Ex: "Three"
            estrelas = ["Zero", "One", "Two", "Three", "Four", "Five"].index(rating_str)

            # Constrói a URL da imagem
            src_imagem = item.select_one("div.image_container img")["src"]
            imagem_url = urljoin(proxima_url, src_imagem)

            # Adiciona os dados do livro à lista
            livros.append(
                {
                    "titulo": titulo,
                    "preco": preco,
                    "estrelas": estrelas,
                    "disponibilidade": disponibilidade,
                    "categoria": categoria,
                    "imagem": imagem_url,
                    "link": link,
                }
            )

        # Verifica se há uma próxima página (paginação)
        next_button = soup.select_one("li.next a")
        if next_button:
            proxima_url = urljoin(proxima_url, next_button["href"])
        else:
            proxima_url = None  # Fim da navegação

    return livros


# Função que extrai todos os livros de todas as categorias
def extrair_todos_os_livros():
    todos_livros = []
    categorias = extrair_Menu()  # Obtém a lista de categorias

    for nome_categoria, url_categoria in categorias:
        # Para cada categoria, extrai os livros associados
        livros = extrair_livros_pagina(nome_categoria, url_categoria)
        todos_livros.extend(livros)  # Adiciona à lista geral
    print("Livros extraido com sucesso")
    return todos_livros


# Executa a extração de todos os livros do site
todos_livros = extrair_todos_os_livros()

# Converte os dados para um DataFrame do pandas
df = pd.DataFrame(todos_livros)

# Exporta os dados para um arquivo CSV (em UTF-8 com BOM, compatível com Excel)
print("Excel salvo com sucesso")
df.to_csv("todos_os_livros.csv", index=False, encoding="utf-8-sig")
