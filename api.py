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
        self.o_keys[key]["Rounds"].append({"Operation":operation,"Numbers":[number_1,number_2],"Result":result,"Winner":0});
        return self.o_keys[key]["Rounds"][-1];
    def connect_player(self,key:str,name:str):
        self.o_keys[key]["Players"]["Nmb"] += 1;
        self.o_keys[key]["Players"]["Users"][name] = {
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

@app.put("/{o_key}/connect/{name}")
def online(o_key:str,name:str):
    # Conecta os jogadores
    if servers.get(o_key,"Online") == False:
        return {"Status":"Offline"};
    elif servers.get(o_key,"Online"):
        if servers.o_keys[o_key]["Players"]["Nmb"] < servers.o_keys[o_key]["Players"]["Max"]:
            servers.connect_player(o_key,name);
            return {"Status":"Connected"};
        else:
            return {"Status":"NoConnected"};

@app.put("/{o_key}/ready")
def update_equation(o_key:str):
    # Retorna se foi dado o Ready
    ready = False;
    servers.o_keys[o_key]["Players"]["Ready"] += 1;
    if servers.o_keys[o_key]["Players"]["Ready"] >= servers.o_keys[o_key]["Players"]["Nmb"]:
        servers.update_equation(o_key);
        ready = True;
    return {"Ready":ready};

@app.put("/{o_key}/result/{user}/{result}")
def note_result(o_key:str,user:str,result:int):
    # Retorna 0 caso não tenha conseguido acertar ou o nome do jogador
    if servers.o_keys[o_key]["Players"]["Ready"] != 0: servers.o_keys[o_key]["Players"]["Ready"] = 0;
    if result == servers.o_keys[o_key]["Rounds"][-1]["Result"] and servers.o_keys[o_key]["Rounds"][-1]["Winner"] == 0:
        servers.o_keys[o_key]["Rounds"][-1]["Winner"] = user;
        servers.o_keys[o_key]["Players"]["Users"][user]["Points"] += 1;
    return {"Winner":servers.o_keys[o_key]["Rounds"][-1]["Winner"]};

@app.get("/{o_key}/get_ready")
async def get_ready(o_key:str):
    # Retorna se foi dado o Ready
    ready = False;
    if servers.o_keys[o_key]["Players"]["Ready"] >= servers.o_keys[o_key]["Players"]["Nmb"]:
        ready = True;
    return {"Ready":ready,"Readys":servers.o_keys[o_key]["Players"]["Ready"]};

@app.get("/{o_key}/get_equation")
async def get_equation(o_key:str):
    # Retorna a equação
    return {"Equation":servers.o_keys[o_key]["Rounds"][-1]};

@app.get("/{o_key}/players")
async def get_players(o_key:str):
    # Retorna tudo sobre os players
    return {"Names":list(servers.o_keys[o_key]["Players"]["Users"].keys()),"Nmb":servers.o_keys[o_key]["Players"]["Nmb"],"Max":servers.o_keys[o_key]["Players"]["Max"]};

@app.get("/{o_key}")
async def main(o_key:str):
    return servers.o_keys[o_key];

@app.get("/admin")
async def all_for_one():
    return servers.o_keys;