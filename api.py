from fastapi import FastAPI

server = FastAPI();
class Servers:
    def __init__(self):
        self.o_keys = {};
    def add_server(self,key:str):
        self.o_keys[key] = {"Online":False};
    def go_server(self,key:str):
        if self.o_keys[key]["Online"] == False:
            self.o_keys[key]["Online"] = True;
        elif self.o_keys[key]["Online"]:
            self.o_keys[key]["Online"] = False;
    def get(self,key:str,_var:str):
        return self.o_keys[key][_var];
    
servers = Servers();

@server.put("/add/{o_key}")
def add(o_key: str):
    servers.add_server(o_key);

@server.get("/online/{o_key}")
async def online(o_key: str):
    if servers.get(o_key,"Online") == False:
        return {"Status":"Offline"};
    elif servers.get(o_key,"Online"):
        return {"Status":"Online"};