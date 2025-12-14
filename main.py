from pycli import *
from config import ConfigTXT
import requests as req

def init():
    print("Iniciado");
    global api
    api = input("Digite a url do servidor: ");

def main():
    _input = input();
    params = get_params(_input);
    match get_command(_input):
        case "init_math":
            match input("1 - Criar um novo servidor;\n2 - Conectar em um servidor;\n3 - Sair;\nOpção: "):
                case "1":
                    clear();
                    server_code = input("Digite o código do servidor: ");
                    max_players = input("Digite a quantidade máxima de jogadores: ");
                    user_name = input("Digite um Nome de Exibição: ");
                    print("Criando um novo servidor...");
                    req.put(api + f"/go_server/{server_code}/{max_players}/{user_name}");
                    op = True;
                case "2":
                    clear();
                    server_code = input("Digite o código do servidor: ");
                    user_name = input("Digite um Nome de Exibição: ");
                    print("Conectando ao servidor...");
                    status = req.get(api + f"/connect/{server_code}/{user_name}").json()["Status"];
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
            players = req.get(api+f"/players/{server_code}").json();
            while players["NmbPlayers"] < players["MaxPlayer"]:
                print(f"Jogadores: {players["NmbPlayers"]}/{players["MaxPlayer"]}");
                players = req.get(api+f"/players/{server_code}").json();
            req.put(api+f"/update/{server_code}");
            equation = req.get(api+f"/get_equation/{server_code}").json()["Equation"];
            print(equation);
            input("O jogo começou. Pressione Enter para continuar...");
            clear();

if __name__ == "__main__":
    init();
    while True:
        main();