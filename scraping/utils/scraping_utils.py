from bs4 import BeautifulSoup
import requests
import pandas as pd


def request_soup(url):
    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    return soup


def save_people_info(url, state, parlamentar):
    
    parlamentares = {"senadores": 0,
                     "deputados": 1}

    soup = request_soup(url)

    total_table = soup.find_all("table", {"class": "wikitable"})[parlamentares[parlamentar]]
    #tabela em dataframe
    df = pd.read_html(str(total_table))
    df = pd.DataFrame(df[0])

    #transforma em string              #corta onde tiver <tr> (separar como string distinta)
    formatted_string = str(total_table).split("<tr><td")
    #para cada valor dentro da string formatada, ignorando a primeira (texto distinto)
    #corta os elementos antes do href e o que vir depois, corta em "title"
    #cria coluna link e coloca a lista de links
    df["Link"] = [value.split("href=")[1] for value in formatted_string[1:]]
    df["Link"] = [value.split(" title")[0] for value in df["Link"]]

    # Tratamento nome dos deputados
    df["Deputados federais eleitos"] = [name.split("[")[0] for name in df["Deputados federais eleitos"]]

    # transforma tabela em um arquivo csv
    df.to_csv(f"data/{state}/urls_deputados.csv", index=False)

    return df


def separate_table(soup, className, path):
    info = soup.find("table", {"class": className})

    df = pd.read_html(str(info))
    df = pd.DataFrame(df[0])

    df.to_csv(path, index=False)


def list_sections(soup):
    i = 0
    allClassSection = []

    while "mf-section-"+str(i) in str(soup):
        allClassSection.append("mf-section-"+str(i))
        i+=1

    return allClassSection


def separate_texts(soup, path):
    allClassSection = list_sections(soup)

    with open(path, "w") as f:
        for classSection in allClassSection:
            posts = soup.find_all(class_ = classSection)

            for post in posts:
                paragraphs = post.find_all("p")
                for p in paragraphs:
                    f.write(p.text)

                points = post.find_all("ul")
                for ul in points:
                    f.write(ul.text)