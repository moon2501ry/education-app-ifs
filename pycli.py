import os

def get_command(text:str):
    return text.split(" ")[0];

def get_params(text:str):
    params = text.split(" ");
    del params[0];
    return params;

def clear():
    os.system("cls" if os.name == "nt" else "clear");