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
    def get(self,key:str,_var:str,default_value:any|None=None);
        try:
            self.o_keys[key][_var];
        except:
            self.o_keys[key][_var] = default_value;
        return self.o_keys[key][_var];
    
servers = Servers();

@server.get("/online/{o_key}")
async def online(o_key: str):
    if 
    return {"Status":"online"}