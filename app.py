from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import fitz

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search_pdf(request: Request, file: UploadFile = File(...), query: str = Form(...)):

    contents = await file.read()
    doc = fitz.open(stream=contents, filetype="pdf")

    results = []

    for page_number in range(len(doc)):
        page = doc[page_number]
        text = page.get_text()

        for line in text.split("\n"):
            if query.lower() in line.lower():
                results.append({
                    "page": page_number + 1,
                    "line": line.strip()
                })

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": results, "query": query}
    )