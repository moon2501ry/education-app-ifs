from pycli import *
import time
import requests as req

def init():
    print("Bem vindo ao Educ. Games feito para estudantes do IFS - Itabaiana");
    global api
    api = input("Digite a url do servidor: ");
    try:
        req.get(api+"/");
    except:
        input("Servidor não está ativo!!");
        quit();

def main():
    while True:
        match input("1 - Criar uma nova Party;\n2 - Conectar em uma Party;\n3 - Sair;\nOpção: "):
            case "1":
                clear();
                server_code = input("Digite o código da Party: ");
                if req.get(api+f"/{server_code}/get_status").json()["Status"] != "NoParty":
                    input("Essa Party já está sendo usada!!");
                    continue;
                max_players = input("Digite a quantidade máxima de jogadores: ");
                user_name = input("Digite um Nome de Exibição: ");
                print("Criando uma nova Party...");
                req.put(api+f"/go_party/{server_code}/{max_players}/{user_name}");
                print("Party Criada!!");
                op = True;
                break;
            case "2":
                clear();
                server_code = input("Digite o código da Party: ");
                user_name = input("Digite um Nome de Exibição: ");
                print("Conectando à Party...");
                status = req.put(api+f"/{server_code}/connect/{user_name}").json()["Status"];
                op = False;
                match status:
                    case "Offline":
                        print("A Party se encontra Offline!!");
                    case "Connected":
                        print("Conectado!");
                        break;
                    case "NoConnected":
                        print("Não foi possível se conectar a Party. Ela está lotada...");
                    case "NoParty":
                        print("A Party não existe...");
                    case _:
                        print("Erro Inesperado");
            case "3":
                clear();
                print("Saindo...");
                exit();
        input();
    clear();
    players = req.get(api+f"/{server_code}/players").json();
    while players["Nmb"] < players["Max"]:
        print(f"Jogadores: {players["Nmb"]}/{players["Max"]}\nNomes: {players["Names"]}\nCódigo de Party: {server_code}");
        time.sleep(8);
        players = req.get(api+f"/{server_code}/players").json();
        clear();
    print(f"Jogadores: {players["Nmb"]}/{players["Max"]}\nNomes: {players["Names"]}");
    input("Pronto? Pressione Enter para continuar...");
    ready = req.put(api+f"/{server_code}/ready").json();
    while not ready["Ready"]:
        clear();
        if ready["Ready"]:
            break;
        ready = req.get(api+f"/{server_code}/get_ready").json();
        print(f"Jogadores Prontos: {ready["Readys"]}/{players["Nmb"]}");
        time.sleep(1.5);
    while True:
        equation = req.get(api+f"/{server_code}/get_equation").json()["Equation"];
        print(equation);
        winner = 0;
        while winner == 0:
            clear();
            print(f"Equação: {equation["Numbers"][0]}{equation["Operation"]}{equation["Numbers"][1]}\n");
            result = input("Qual a resposta? ");
            winner = req.put(api+f"/{server_code}/result/{user_name}/{result}").json()["Winner"];
            if winner == 0:
                input("Você errou. Pressione Enter para continuar...");
        if winner == user_name:
            print("VOCÊ foi o vencedor!!!");
        elif winner != user_name:
            print(f"O vencedor foi {winner}...");
        input();
        clear();
        while True:
            if op:
                match input("1 - Continuar;\n2 - Desligar Party;\nOpção: "):
                    case "1":
                        ready = req.put(api+f"/{server_code}/ready").json();
                        desconnect = False;
                    case "2":
                        req.put(api+f"/{server_code}/offline");
                        req.put(api+f"/{server_code}/desconnect/{user_name}");
                        desconnect = True;
                    case _:
                        input("Opção não disponível!!");
                        continue;
            elif not op:
                match input("1 - Continuar;\n2 - Desconectar da Party\nOpção: "):
                    case "1":
                        ready = req.put(api+f"/{server_code}/ready").json();
                        desconnect = False;
                    case "2":
                        req.put(api+f"/{server_code}/desconnect/{user_name}");
                        desconnect = True;
                    case _:
                        input("Opção não disponível!!");
                        continue;
            break;
        if req.get(api+f"/{server_code}/get_status").json()["Status"] == "Offline" and not desconnect:
            req.put(api+f"/{server_code}/desconnect/{user_name}");
            input("A Party foi encerrada");
            desconnect = True;
        if desconnect:
            clear();
            break;
        players = req.get(api+f"/{server_code}/players").json();
        while not ready["Ready"]:
            ready = req.get(api+f"/{server_code}/get_ready").json();
            if ready["Ready"]:
                break;
            print(f"Jogadores Prontos: {ready["Readys"]}/{players["Nmb"]}");
            time.sleep(1.5);
            clear();
    del desconnect;
                    
if __name__ == "__main__":
    init();
    while True:
        main();