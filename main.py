from fastapi import FastAPI
from scrapers import get_gamespot, get_gamesradar, get_forbes, get_g1, get_cnn



app = FastAPI()

@app.get("/")
async def root():
    games_radar = get_gamesradar()
    games_pot = get_gamespot()
    forbes = get_forbes()
    g1 = get_g1()
    cnn = get_cnn()
    return [{"id": 1, "title": games_radar, "url": "https://www.gamesradar.com/", "source": "gamesradar"}, {"id": 2, "title": games_pot, "url": "https://www.gamespot.com/", "source": "gamespot"}, {"id": 3,  "title": forbes, "url": "https://forbes.com.br/", "source": "forbes"}, {"id": 4,  "title": g1, "url": "https://g1.globo.com/", "source": "g1"}, {"id": 5,   "title": cnn, "url": "https://www.cnnbrasil.com.br/", "source": "cnn"}]
    

