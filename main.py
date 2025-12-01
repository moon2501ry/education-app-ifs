from pycli import *
from config import ConfigTXT
import random as rnd
import time

def init():
    config = ConfigTXT();

def main():
    _input = input();
    params = get_params(_input);
    match get_command(_input):
        case "init_math":
            input("O jogo foi começou. Pressione Enter para continuar...");
            clear();
            operation = rnd.choice(["+","-"]);
            number_1 = rnd.randint(0,100);
            number_2 = rnd.randint(0,100);
            result = (number_1 + number_2) if operation == "+" else (number_1 - number_2);
            result_user = input("")
            print();
            




if __name__ == "__main__":
    init();
    while True:
        main();