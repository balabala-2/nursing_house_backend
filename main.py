from config import create_app

app = create_app()

if __name__ == '__main__':
    import uvicorn
    # linux
    # uvicorn.run(app='main:app', host="0.0.0.0", port=8080, reload=True, debug=True)

    # local
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)