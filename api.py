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
    def get_status(self,key:str):
        try:
            if self.get(key,"Online") == False:
                return "Offline";
            elif self.get(key,"Online"):
                if self.o_keys[key]["Players"]["Nmb"] < self.o_keys[key]["Players"]["Max"]:
                    return "Connected";
                else:
                    return "NoConnected";
        except:
            return "NoParty";
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
    def desconnect_player(self,key:str,name:str):
        self.o_keys[key]["Players"]["Nmb"] -= 1;
        del self.o_keys[key]["Players"]["Users"][name];
    def get(self,key:str,_var:str):
        return self.o_keys[key][_var];
    
servers = Servers();

@app.put("/go_party/{key}/{maxplayers}/{name}")
def add_or_go(key:str,maxplayers:int,name:str):
    servers.add_server(key,maxplayers);
    servers.go_server(key);
    servers.connect_player(key,name);

@app.put("/{key}/offline")
def chance_status(key:str):
    servers.go_server(key);

@app.put("/{key}/connect/{name}")
def connect(key:str,name:str):
    # Conecta os jogadores
    status = servers.get_status(key);
    if status == "Connected":
        servers.connect_player(key,name);
    return {"Status":status};

@app.put("/{key}/desconnect/{name}")
def desconnect(key:str,name:str):
    # Desconecta os jogadores
    servers.desconnect_player(key,name);
    if servers.o_keys[key]["Players"]["Ready"] >= servers.o_keys[key]["Players"]["Nmb"]:
        servers.update_equation(key);

@app.put("/{key}/ready")
def update_equation(key:str):
    # Retorna se foi dado o Ready
    ready = False;
    servers.o_keys[key]["Players"]["Ready"] += 1;
    if servers.o_keys[key]["Players"]["Ready"] >= servers.o_keys[key]["Players"]["Nmb"]:
        servers.update_equation(key);
        ready = True;
    return {"Ready":ready};

@app.put("/{key}/result/{user}/{result}")
def note_result(key:str,user:str,result:int):
    # Retorna 0 caso não tenha conseguido acertar ou o nome do jogador
    if servers.o_keys[key]["Players"]["Ready"] != 0: servers.o_keys[key]["Players"]["Ready"] = 0;
    if result == servers.o_keys[key]["Rounds"][-1]["Result"] and servers.o_keys[key]["Rounds"][-1]["Winner"] == 0:
        servers.o_keys[key]["Rounds"][-1]["Winner"] = user;
        servers.o_keys[key]["Players"]["Users"][user]["Points"] += 1;
    return {"Winner":servers.o_keys[key]["Rounds"][-1]["Winner"]};

@app.get("/{key}/get_status")
def get_status(key:str):
    return {"Status":servers.get_status(key)};

@app.get("/{key}/get_ready")
async def get_ready(key:str):
    # Retorna se foi dado o Ready
    ready = False;
    if servers.o_keys[key]["Players"]["Ready"] >= servers.o_keys[key]["Players"]["Nmb"]:
        ready = True;
    return {"Ready":ready,"Readys":servers.o_keys[key]["Players"]["Ready"]};

@app.get("/{key}/get_equation")
async def get_equation(key:str):
    # Retorna a equação
    return {"Equation":servers.o_keys[key]["Rounds"][-1]};

@app.get("/{key}/players")
async def get_players(key:str):
    # Retorna tudo sobre os players
    return {"Names":list(servers.o_keys[key]["Players"]["Users"].keys()),"Nmb":servers.o_keys[key]["Players"]["Nmb"],"Max":servers.o_keys[key]["Players"]["Max"]};

@app.get("/{key}")
async def main(key:str):
    return servers.o_keys[key];