from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os, requests
from bs4 import BeautifulSoup
import logging
from io import BytesIO
from PIL import Image

app = FastAPI()

logging.basicConfig(level=logging.INFO)

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory='static'), name='static')


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', response_class=HTMLResponse)
async def get_basic_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/uploadlink/')
async def get_basic_form(request: Request, link: str = Form(...)):
    logging.info("Method has been called")
    url = link
    HEADERS = ({'User-Agent':''})
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    images = soup.find_all("img", class_='hCL kVc L4E MIw')
    images_list = []
    real_image = ""

    for img in images:
        if img.has_attr('src'):
            images_list.append(img['src'])
            
    for i in range(len(images_list)):
        if images_list[i].__contains__('736x'):
            real_image = images_list[i]
             
    r = requests.get(f"{real_image}") 
    image = Image.open(BytesIO(r.content))
    
    if not os.path.exists("media"):
        os.makedirs("media")
    image_path = os.path.join("media", "generated_image.png")
    image.save(image_path)
    
    return {"link": link, 'image path': image_path}


@app.get("/media/generated_image.png/")
async def get_image():
    return FileResponse("media/generated_image.png")


