from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

origins = ["http://localhost:3000", "https://programming-list.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def getTitleAndTopPageImage(url: str = ""):
    # BeautifulSoupでurlからhtmlを取得
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # titleを取得
    title = soup.title.text

    # サムネイルの取得
    meta = soup.find_all("meta", property="og:image")
    if len(meta) != 0:
        thumbnails_url = meta[0].get("content")
        return {"title": title, "image": thumbnails_url}

    return {"title": title, "image": ""}
