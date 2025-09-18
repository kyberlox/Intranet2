from main import app

if __name__ == "__main__":
    # запуск приложения, например, с помощью uvicorn программно
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)