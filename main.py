import asyncio
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()

# Configuração de CORS
origins = ["http://localhost:5173", "https://my-homepage-5ir.pages.dev"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

async def fetch_news(client, url, container_tag=None, container_class=None, title_tag=None, title_class=None, container_id=None, is_meta=False):
    """
    Função ultra flexível para scraping assíncrono.
    """
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Lógica especial para o InfoMoney (Meta Tags)
        if is_meta:
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag and meta_tag.has_attr('content'):
                content = meta_tag['content'].replace("Publicidade ", "", 1)
                return content.split("Medidas antidumping")[0].strip()
            return "Meta tag não encontrada"

        # Lógica para Tags HTML comuns
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

@app.get("/")
async def root():
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
        tasks = [
            # GAMES RADAR - Principal
            fetch_news(client, 'https://www.gamesradar.com/', 'div', 'feature-block-item-wrapper item-1', 'span', 'article-name'),
            # GAMES RADAR - Últimas
            fetch_news(client, 'https://www.gamesradar.com/', 'div', 'list-text-links', 'h3', 'article-name'),
            # GAME SPOT - Principal
            fetch_news(client, 'https://www.gamespot.com/', 'section', 'promo--container', 'h2'),
            # GAME SPOT - Últimas
            fetch_news(client, 'https://www.gamespot.com/', 'section', None, 'h4', 'card-item__title', container_id='river'),
            # IGN BRASIL
            fetch_news(client, 'https://br.ign.com/cinema-tv', 'section', 'broll', 'span', 'caption'),
            # ADRENALINE
            fetch_news(client, 'https://www.adrenaline.com.br/hardware/', 'h2', 'feed-title'),
            # G1
            fetch_news(client, 'https://g1.globo.com/', 'div', 'feed-post-body-title', 'p'),
            # NOSSO PALESTRA
            fetch_news(client, 'https://nossopalestra.com.br/', 'h2', 'post-title-feed-sm'),
            # INFOMONEY
            fetch_news(client, 'https://www.infomoney.com.br/', is_meta=True),
            # TERRA
            fetch_news(client, 'https://www.terra.com.br/', 'a', 'card-news__text--title'),
            # UOL
            fetch_news(client, 'https://www.uol.com.br/', 'h3', 'headlineMain__title'),
        ]

        results = await asyncio.gather(*tasks)

        names = [
            "GamesRadar", "GamesRadar", "GameSpot", "GameSpot", "IGN",
            "Adrenaline", "G1", "Nosso Palestra", "InfoMoney", "Terra", "UOL"
        ]
        
        links = [
            "https://www.gamesradar.com/", "https://www.gamesradar.com/", "https://www.gamespot.com/", "https://www.gamespot.com/", "https://br.ign.com/",
            "https://www.adrenaline.com.br/", "https://g1.globo.com/", 
            "https://nossopalestra.com.br/", "https://www.infomoney.com.br/", "https://www.terra.com.br/", "https://www.uol.com.br/"
        ]
        
        return [
            {"id": i + 1, "title": results[i], "url": links[i], "source": names[i]}
            for i in range(len(tasks))
        ]

