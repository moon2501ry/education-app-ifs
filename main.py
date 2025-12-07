from pycli import *
from config import ConfigTXT
import random as rnd
import time

def init():
    print("Iniciado");

def main():
    _input = input();
    params = get_params(_input);
    match get_command(_input):
        case "init_math":
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