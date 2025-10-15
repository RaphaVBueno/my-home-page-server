import requests
from bs4 import BeautifulSoup

def get_gamespot():
    try:
        response = requests.get('https://www.gamespot.com/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        container_noticia = soup.find('section', class_='promo--container')

        if container_noticia:
            link_noticia = container_noticia.find('a', class_='promo--offset-wide')
            
            if link_noticia:
                titulo_tag = link_noticia.find('h2')

                if titulo_tag:
                    return titulo_tag.get_text(strip=True)

        return "Erro: Não foi possível encontrar o título da notícia principal."

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro na requisição: {e}"
    except Exception as e:
        return f"Ocorreu um erro ao processar o HTML: {e}"
    
def get_gamesradar():
    try:
        response = requests.get('https://www.gamesradar.com/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        container_noticia = soup.find('div', class_='feature-block-item-wrapper item-1')

        if container_noticia:
            titulo_tag = container_noticia.find('span', class_='article-name')
            
            if titulo_tag:
                return titulo_tag.get_text(strip=True)
            else:
                return "Erro: Não foi possível encontrar a tag do título."

        return "Erro: Não foi possível encontrar o contêiner da notícia principal."

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro na requisição: {e}"
    except Exception as e:
        return f"Ocorreu um erro ao processar o HTML: {e}"
    
def get_forbes():
    try:
        response = requests.get('https://forbes.com.br/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        container_noticia = soup.find('li', class_='manchete_loop_1')

        if container_noticia:
            titulo_tag = container_noticia.find('h3')

            if titulo_tag:
                return titulo_tag.get_text(strip=True)
            else:
                return "Erro: Não foi possível encontrar a tag do título."
        
        return "Erro: Não foi possível encontrar o contêiner da notícia principal."

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro na requisição: {e}"
    except Exception as e:
        return f"Ocorreu um erro ao processar o HTML: {e}"   

def get_g1():
    try:
        response = requests.get('https://g1.globo.com/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        container_noticia = soup.find('div', class_='feed-post-body-title')

        if container_noticia:
            titulo_tag = container_noticia.find('p')

            if titulo_tag:
                return titulo_tag.get_text(strip=True)
            else:
                return "Erro: Não foi possível encontrar a tag <p> com o título."
        
        return "Erro: Não foi possível encontrar o contêiner da notícia principal."

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro na requisição: {e}"
    except Exception as e:
        return f"Ocorreu um erro ao processar o HTML: {e}"  

def get_cnn():
    try:
        response = requests.get('https://www.cnnbrasil.com.br/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        container_noticia = soup.find('figcaption')

        if container_noticia:
            titulo_tag = container_noticia.find('h2')

            if titulo_tag:
                return titulo_tag.get_text(strip=True)
            else:
                return "Erro: Não foi possível encontrar a tag <h2> com o título."
        
        return "Erro: Não foi possível encontrar o contêiner da notícia principal."

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro na requisição: {e}"
    except Exception as e:
        return f"Ocorreu um erro ao processar o HTML: {e}"