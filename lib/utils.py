from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def openLabels(path):
    class_names = []
    with open(path, "r") as f:
        class_names = f.read().strip().split("\n")
    return class_names
