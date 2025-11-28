from fastapi import FastAPI

server = FastAPI();

@server.get("/")
def read_root():
    return {"Hello": "World"};