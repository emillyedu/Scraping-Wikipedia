from utils.scraping_utils import * # chamar funcoes do scraping utils
import os
import json
import shutil

if os.path.exists("data"):
    shutil.rmtree("data")

os.mkdir("data")

#leitura do json
with open("utils/wiki_urls.json", "r") as file:
    wiki_urls = json.load(file)

#em cada um dos estados
for state in wiki_urls:
    #cria pasta para cada estado
    os.mkdir(f"data/{state}")
    #chamar url de cada estado
    url_state = wiki_urls[state]
    deputados = save_people_info(url_state, state, "deputados")

    os.mkdir(f"data/{state}/deputados")
    
    #em cada link
    for i, url_deputado in enumerate(deputados["Link"]):
        try:
            #links de cada pagina dos deputados
            url_deputado = "https://pt.m.wikipedia.org" + eval(url_deputado)
        except:
            continue
        
        soup = request_soup(url_deputado)
        
        #nome do deputado conforme o indice
        deputado = deputados["Deputados federais eleitos"][i]

        # Criar pasta
        try:
            os.mkdir(f"data/{state}/deputados/{deputado}")
        except:
            continue

        # Salvar tabela lateral
        className = "infobox infobox_v2"

        if className in str(soup):
            path = f"data/{state}/deputados/{deputado}/tabela_lateral.csv"
            separate_table(soup, className, path)

        # Salvar corpo da página
        className = "mf-section-"

        if className in str(soup):
            path = f"data/{state}/deputados/{deputado}/corpo_da_pagina.txt"
            separate_texts(soup, path)

        # Salvar tabela final
        className = "toccolours"

        if className in str(soup):
            path = f"data/{state}/deputados/{deputado}/tabela_final.csv"
            separate_table(soup, className, path)