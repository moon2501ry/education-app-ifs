from pycli import *
from config import ConfigTXT
import requests as req

def init():
    print("Iniciado");
    global api
    api = input("Digite a API da sua conta: ");

def main():
    _input = input();
    params = get_params(_input);
    match get_command(_input):
        case "init_math":
            match input("1 - Criar um novo servidor;\n2 - Conectar em um servidor;\n3 - Sair;\nOpção: "):
                case "1":
                    server_code = input("Digite o código do servidor: ");
                    print("Criando um novo servidor...");
                    equation = req.put(api + f"/add_server/{server_code}").json()["Equation"];
                    print(equation);
                case "2":
                    server_code = input("Digite o código do servidor: ");
                    print("Conectando no servidor...");
                    print(req.get(api + f"/online/{server_code}"));
                case "3":
                    print("Saindo...");
                    exit();
            input("O jogo foi começou. Pressione Enter para continuar...");
            run = True
            while run:
                clear();
                print(f"{equation[1]}{equation[0]}{equation[2]}");
                result = equation[-1];
                result_user = input("Qual a Resposta? ");
                if int(result_user) == result:
                    input("Você ganhou!!! Pressione Enter para continuar...");
                    # run = False;
                elif int(result_user) != result:
                    print(result,result_user);
                    input("Tente dnv!! Pressione Enter para continuar...");
            clear();

if __name__ == "__main__":
    init();
    while True:
        main();