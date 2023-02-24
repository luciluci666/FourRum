from fastapi import FastAPI
import uvicorn
from starlette.requests import Request
from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run('https_redirect:app', port=80, host='0.0.0.0')