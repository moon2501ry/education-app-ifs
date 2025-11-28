from pycli import *
from config import ConfigTXT

def init():
    config = ConfigTXT();

def main():
    _input = input();
    match get_command(_input):
        case connect:
            params = get_params(_input);

if __name__ == "__main__":
    while True:
        main();