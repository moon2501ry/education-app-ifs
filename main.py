from pycli import *
from config import ConfigTXT
import time

def init():
    config = ConfigTXT();

def main():
    _input = input();
    params = get_params(_input);
    match get_command(_input):
        case "init_math":




if __name__ == "__main__":
    init();
    while True:
        main();