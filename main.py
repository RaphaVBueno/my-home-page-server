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
    return {"games_radar": games_radar, "games_pot": games_pot, "forbes": forbes, "g1": g1, "cnn": cnn}
    

