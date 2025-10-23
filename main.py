from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scrapers import get_gamespot, get_gamesradar, get_infomoney, get_g1, get_cnn, get_terra



app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://my-homepage-5ir.pages.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    games_radar = get_gamesradar()
    games_pot = get_gamespot()
    infomoney = get_infomoney()
    g1 = get_g1()
    cnn = get_cnn()
    terra = get_terra()
    return [{"id": 1, "title": games_radar, "url": "https://www.gamesradar.com/", "source": "gamesradar"}, {"id": 2, "title": games_pot, "url": "https://www.gamespot.com/", "source": "gamespot"}, 
            {"id": 3,  "title": infomoney, "url": "https://www.infomoney.com.br/", "source": "forbes"}, {"id": 4,  "title": g1, "url": "https://g1.globo.com/", "source": "g1"}, 
            {"id": 5,   "title": cnn, "url": "https://www.cnnbrasil.com.br/", "source": "cnn"}, {"id": 6,   "title": terra, "url": "https://www.terra.com.br/", "source": "terra"}]

