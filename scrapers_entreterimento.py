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
    
def get_gamesradarfeed():
    try:        
        response = requests.get('https://www.gamesradar.com/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        recent_news_sidebar = soup.find('div', class_='list-text-links')

        if recent_news_sidebar:
            noticia_tag = recent_news_sidebar.find('h3', class_='article-name')
            
            if noticia_tag:
                return noticia_tag.get_text(strip=True)
            else:
                return "Erro: Título da notícia não encontrado dentro de Recent News."
        
        return "Erro: Seção 'Recent News' não encontrada."

    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {e}"
    except Exception as e:
        return f"Erro ao processar o HTML: {e}"
    
def get_gamespotfeed():
    try:
        response = requests.get('https://www.gamespot.com/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        river_section = soup.find('section', id='river')

        if river_section:
            noticia_tag = river_section.find('h4', class_='card-item__title')
            
            if noticia_tag:
                return noticia_tag.get_text(strip=True)
            else:
                return "Erro: Título da notícia não encontrado na seção Latest."
        
        return "Erro: Seção 'Latest' (river) não encontrada."

    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {e}"
    except Exception as e:
        return f"Ocorreu um erro ao processar o HTML: {e}"
    
def get_adrenaline():
    try:        
        response = requests.get('https://www.adrenaline.com.br/hardware/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        noticia_tag = soup.find('h2', class_='feed-title')

        if noticia_tag:
            return noticia_tag.get_text(strip=True)
        else:
            return "Erro: Título da notícia não encontrado (classe 'feed-title')."

    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {e}"
    except Exception as e:
        return f"Erro ao processar o HTML: {e}"
    

def get_palmeiras():
    try:
        response = requests.get('https://nossopalestra.com.br/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        noticia_tag = soup.find('h2', class_='post-title-feed-sm')

        if noticia_tag:
            return noticia_tag.get_text(strip=True)
        else:
            return "Erro: Título da notícia não encontrado."

    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {e}"
    except Exception as e:
        return f"Erro ao processar o HTML: {e}"