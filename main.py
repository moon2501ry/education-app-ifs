from pycli import *
from config import ConfigTXT
import time
import requests as req

def init():
    print("Iniciado");
    global api
    api = input("Digite a url do servidor: ");

def main():
    match input("1 - Criar um novo servidor;\n2 - Conectar em um servidor;\n3 - Sair;\nOpção: "):
        case "1":
            clear();
            server_code = input("Digite o código do servidor: ");
            max_players = input("Digite a quantidade máxima de jogadores: ");
            user_name = input("Digite um Nome de Exibição: ");
            print("Criando um novo servidor...");
            req.put(api+f"/go_server/{server_code}/{max_players}/{user_name}");
            op = True;
        case "2":
            clear();
            server_code = input("Digite o código do servidor: ");
            user_name = input("Digite um Nome de Exibição: ");
            print("Conectando ao servidor...");
            status = req.put(api+f"/{server_code}/connect/{user_name}").json()["Status"];
            match status:
                case "Offline":
                    print("O servidor se encontra Offline ou não existe.");
                case "Connected":
                    print("Conectado!");
                case "NoConnected":
                    print("Não foi possível se conectar as servidor. Eles está lotado...");
            op = False;
        case "3":
            clear();
            print("Saindo...");
            exit();
    clear();
    players = req.get(api+f"/{server_code}/players").json();
    while players["Nmb"] < players["Max"]:
        print(f"Jogadores: {players["Nmb"]}/{players["Max"]}\nNomes: {players["Names"]}");
        time.sleep(8);
        players = req.get(api+f"/{server_code}/players").json();
        clear();
    print(f"Jogadores: {players["Nmb"]}/{players["Max"]}\nNomes: {players["Names"]}");
    input("Pronto? Pressione Enter para continuar...");
    ready = req.put(api+f"/{server_code}/ready").json()["Ready"];
    while ready == False:
        clear();
        if ready:
            break;
        _ready = req.get(api+f"/{server_code}/get_ready").json();
        ready = _ready["Ready"];
        readys = _ready["Readys"];
        print(f"Jogadores Prontos: {readys}/{players["Nmb"]}");
        time.sleep(1.5);
    equation = req.get(api+f"/{server_code}/get_equation").json()["Equation"];
    print(equation);
    winner = 0;
    while winner == 0:
        clear();
        print(f"Equação: {equation["Numbers"][0]}{equation["Operation"]}{equation["Numbers"][1]}\n");
        result = input("Qual a resposta? ");
        winner = req.put(api+f"/{server_code}/result/{user_name}/{int(result)}").json()["Winner"];
        if winner == 0:
            input("Você errou. Pressione Enter para continuar...");
    if winner == user_name:
        print("VOCÊ foi o vencedor!!!");
    elif winner != user_name:
        print(f"O vencedor foi {winner}...");
    input();

if __name__ == "__main__":
    init();
    while True:
        main();