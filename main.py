from fastapi import FastAPI
import uvicorn

from rotas import router

app = FastAPI()

@app.get("/")
def get_root():
    return {"Mensagem": "API de produtos"}

app.include_router(router, prefix="")

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")