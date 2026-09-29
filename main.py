import asyncio
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup


app = FastAPI()

# Configuração de CORS
origins = ["http://localhost:5173", "https://my-homepage-5ir.pages.dev"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

async def fetch_news(client, url, container_tag=None, container_class=None, title_tag=None, title_class=None, container_id=None, is_meta=False):
    """
    Função ultra flexível para scraping assíncrono.
    """
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        if is_meta:
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag and meta_tag.has_attr('content'):
                content = meta_tag['content'].replace("Publicidade ", "", 1)
                return content.split("Medidas antidumping")[0].strip()
            return "Meta tag não encontrada"

        if container_id:
            section = soup.find(container_tag, id=container_id)
        else:
            section = soup.find(container_tag, class_=container_class)
            
        if not section: 
            return "Seção não encontrada"

        if title_tag:
            target = section.find(title_tag, class_=title_class)
            return target.get_text(strip=True) if target else "Título não encontrado"
        
        return section.get_text(strip=True)
    
    except Exception as e:
        return f"Erro: {str(e)}"


async def fetch_rss_title(client, url, index=0):
    """
    Busca o título de uma notícia via feed RSS/XML.
    Usado para sites que bloqueiam scraping ou carregam conteúdo via JS.
    O parâmetro index permite escolher qual item retornar (0 = primeiro, 1 = segundo, etc).
    """
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml-xml')
        
        items = soup.find_all('item')
        if items and len(items) > index:
            title = items[index].find('title')
            return title.get_text(strip=True) if title else "Título não encontrado no RSS"
        elif items:
            title = items[0].find('title')
            return title.get_text(strip=True) if title else "Título não encontrado no RSS"
        return "Nenhum item no RSS"
    
    except Exception as e:
        return f"Erro: {str(e)}"


async def fetch_kotaku_latest(client):
    """
    Busca a primeira notícia da sidebar 'Latest' do Kotaku.
    Estrutura: aside.sidebar > article > a > div > h3.font-bold
    """
    try:
        response = await client.get('https://kotaku.com/', timeout=10.0)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        sidebar = soup.find('aside', class_='sidebar')
        if not sidebar:
            return "Seção não encontrada"
        
        article = sidebar.find('article')
        if not article:
            return "Artigo não encontrado"
        
        h3 = article.find('h3', class_='font-bold')
        return h3.get_text(strip=True) if h3 else "Título não encontrado"
    
    except Exception as e:
        return f"Erro: {str(e)}"


async def fetch_g1_headline(client):
    """
    Busca a manchete principal do G1.
    Estrutura atualizada: div.feed-post-body-title > div > h2 > a > p
    """
    try:
        response = await client.get('https://g1.globo.com/', timeout=10.0)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        title_div = soup.find('div', class_='feed-post-body-title')
        if not title_div:
            return "Seção não encontrada"
        
        # Tenta pegar o <p> dentro de h2 > a (estrutura atualizada)
        p_tag = title_div.find('p')
        if p_tag:
            return p_tag.get_text(strip=True)
        
        # Fallback: pegar texto do h2
        h2 = title_div.find('h2')
        if h2:
            return h2.get_text(strip=True)
        
        return title_div.get_text(strip=True)
    
    except Exception as e:
        return f"Erro: {str(e)}"


async def fetch_infomoney_headline(client):
    """
    Busca a manchete principal do InfoMoney.
    A meta description virou texto genérico, então agora fazemos scraping do conteúdo.
    """
    try:
        response = await client.get('https://www.infomoney.com.br/', timeout=10.0)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Tenta encontrar a manchete principal por diversas abordagens
        # Abordagem 1: h2 ou h3 dentro de elementos de destaque
        for selector in [
            ('h2', 'title'),
            ('h3', 'title'),
            ('a', 'article-card__headline'),
            ('h2', None),
        ]:
            tag, cls = selector
            if cls:
                el = soup.find(tag, class_=lambda c: c and cls in c)
            else:
                # Busca o primeiro h2 dentro do main ou article
                main = soup.find('main') or soup.find('article')
                el = main.find(tag) if main else None
            
            if el:
                text = el.get_text(strip=True)
                if len(text) > 15:  # Evita pegar títulos de seção curtos
                    return text
        
        # Fallback: meta og:title que pode ter algo mais específico
        og = soup.find('meta', property='og:title')
        if og and og.get('content'):
            return og['content']
        
        return "Manchete não encontrada"
    
    except Exception as e:
        return f"Erro: {str(e)}"


@app.get("/")
async def root():
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
        tasks = [
            # GAMES RADAR - Principal (conteúdo carregado via JS, usar RSS)
            fetch_rss_title(client, 'https://www.gamesradar.com/feeds.xml', 0),
            # GAMES RADAR - Últimas (segundo item do RSS)
            fetch_rss_title(client, 'https://www.gamesradar.com/feeds.xml', 1),
            # KOTAKU - Principal (h2 dentro do grid featured)
            fetch_news(client, 'https://kotaku.com/', 'h2', 'font-bold'),
            # KOTAKU - Últimas (sidebar com articles)
            fetch_kotaku_latest(client),
            # IGN BRASIL (conteúdo carregado via JS, usar RSS)
            fetch_rss_title(client, 'https://br.ign.com/cinema-tv.xml'),
            # ADRENALINE (bloqueia scraping com 403, usar RSS)
            fetch_rss_title(client, 'https://www.adrenaline.com.br/feed/'),
            # G1 (estrutura de título atualizada)
            fetch_g1_headline(client),
            # NOSSO PALESTRA
            fetch_news(client, 'https://nossopalestra.com.br/', 'h2', 'post-title-feed-sm'),
            # INFOMONEY (meta description agora é genérica)
            fetch_infomoney_headline(client),
            # TERRA
            fetch_news(client, 'https://www.terra.com.br/', 'a', 'card-news__text--title'),
            # UOL
            fetch_news(client, 'https://www.uol.com.br/', 'h3', 'headlineMain__title'),
        ]

        results = await asyncio.gather(*tasks)

        names = [
            "GamesRadar", "GamesRadar", "Kotaku", "Kotaku", "IGN",
            "Adrenaline", "G1", "Nosso Palestra", "InfoMoney", "Terra", "UOL"
        ]
        
        links = [
            "https://www.gamesradar.com/", "https://www.gamesradar.com/", "https://kotaku.com/", "https://kotaku.com/", "https://br.ign.com/",
            "https://www.adrenaline.com.br/", "https://g1.globo.com/", 
            "https://nossopalestra.com.br/", "https://www.infomoney.com.br/", "https://www.terra.com.br/", "https://www.uol.com.br/"
        ]
        
        return [
            {"id": i + 1, "title": results[i], "url": links[i], "source": names[i]}
            for i in range(len(tasks))
        ]