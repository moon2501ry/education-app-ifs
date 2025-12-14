from fastapi import FastAPI
import random as rnd

app = FastAPI();
class Servers:
    def __init__(self):
        self.o_keys = {};
    def add_server(self,key:str,qnt_players:int):
        self.o_keys[key] = {"Online":False,"MaxPlayer":qnt_players,"NmbPlayers":0,"Players":[]};
    def go_server(self,key:str):
        if self.o_keys[key]["Online"] == False:
            self.o_keys[key]["Online"] = True;
        elif self.o_keys[key]["Online"]:
            self.o_keys[key]["Online"] = False;
    def update_equation(self,key:str):
        operation = rnd.choice(["+","-"]);
        number_1 = rnd.randint(0,100);
        number_2 = rnd.randint(0,100);
        result = (number_1 + number_2) if operation == "+" else (number_1 - number_2);
        self.o_keys[key]["Equation"] = [operation,number_1,number_2,result];
        return self.o_keys[key]["Equation"];
    def connect_player(self,key:str,name:str):
        self.o_keys[key]["NmbPlayers"] += 1;
        self.O_keys[key]["Players"].append(name);
    def get(self,key:str,_var:str):
        return self.o_keys[key][_var];
    
servers = Servers();

@app.put("/go_server/{o_key}/{maxplayers}/{name}")
def add_or_go(o_key:str,maxplayers:int,name:str):
    servers.add_server(o_key,maxplayers);
    servers.go_server(o_key);
    servers.connect_player(o_key,name);

@app.put("/update/{o_key}")
def update_equation(o_key:str):
    servers.update_equation(o_key);

@app.get("/get_equation/{o_key}")
async def get_equation(o_key:str):
    return {"Equation":servers.get(o_key,"Equation")}; 

@app.get("/players/{o_key}")
async def get_players(o_key:str):
    return {"Players":servers.get(o_key,"Players"),"NmbPlayers":servers.get(o_key,"NmbPlayers"),"MaxPlayer":servers.get(o_key,"MaxPlayer")};

@app.get("/connect/{o_key}/{name}")
async def online(o_key:str,name:str):
    if servers.get(o_key,"Online") == False:
        return {"Status":"Offline"};
    elif servers.get(o_key,"Online"):
        if servers.get(o_key,"NmbPlayers") < servers.get(o_key,"MaxPlayer"):
            servers.connect_player(o_key,name);
            return {"Status":"Connected"};
        else:
            return {"Status":"NoConnected"};