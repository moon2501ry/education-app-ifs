from pycli import *
from config import ConfigTXT
import random as rnd
import requests as req
import time

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
                    print(req.put(api + "/add", params={"o_key": server_code}));
                case "2":
                    server_code = input("Digite o código do servidor: ");
                    print("Conectando no servidor...");
                    print(req.get(api + "/online", params={"o_key": server_code}));
                case "3":
                    print("Saindo...");
                    exit();
            input("O jogo foi começou. Pressione Enter para continuar...");
            run = True
            while run:
                clear();
                operation = rnd.choice(["+","-"]);
                number_1 = rnd.randint(0,100);
                number_2 = rnd.randint(0,100);
                result = (number_1 + number_2) if operation == "+" else (number_1 - number_2);
                print(str(number_1)+""+operation+""+str(number_2));
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