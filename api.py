from fastapi import FastAPI
import random as rnd

app = FastAPI();
class Servers:
    def __init__(self):
        self.o_keys = {};
    def add_server(self,key:str,qnt_players:int):
        self.o_keys[key] = {
            "Online":False,
            "Public":False,
            "Players":{
                "Max":qnt_players,
                "Nmb":0,
                "Ready":0,
                "Users":{}
            },
            "Rounds":[],
            "GameMode":0
        };
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
        self.o_keys[key]["Players"]["Nmb"] += 1;
        self.o_keys[key]["Players"]["Users"][name] = {
            "Op":False,
            "Points":0
        };
    def get(self,key:str,_var:str):
        return self.o_keys[key][_var];
    
servers = Servers();

@app.put("/go_server/{o_key}/{maxplayers}/{name}")
def add_or_go(o_key:str,maxplayers:int,name:str):
    servers.add_server(o_key,maxplayers);
    servers.go_server(o_key);
    servers.connect_player(o_key,name);

@app.put("/{o_key}/ready")
def update_equation(o_key:str):
    # Terminar
    servers.update_equation(o_key);

@app.put("/{o_key}/result/{user}/{result}")
def note_result(o_key:str,user:str,result:int):
    if result == servers[o_key]["Equation"][-1]:
        servers[o_key]["User"]
        # Terminar

@app.get("/{o_key}/get_equation")
async def get_equation(o_key:str):
    return {"Equation":servers.get(o_key,"Equation")};

@app.get("/{o_key}/players")
async def get_players(o_key:str):
    return {"Players":servers.get(o_key,"Players"),"NmbPlayers":servers.get(o_key,"NmbPlayers"),"MaxPlayer":servers.get(o_key,"MaxPlayer")};

@app.get("/{o_key}/connect/{name}")
async def online(o_key:str,name:str):
    if servers.get(o_key,"Online") == False:
        return {"Status":"Offline"};
    elif servers.get(o_key,"Online"):
        if servers.get(o_key,"NmbPlayers") < servers.get(o_key,"MaxPlayer"):
            servers.connect_player(o_key,name);
            return {"Status":"Connected"};
        else:
            return {"Status":"NoConnected"};

@app.get("/{o_key}")
async def main(o_key:str):
    return servers.o_keys[o_key];

@app.get("/admin")
async def all_for_one():
    return servers.o_keys;