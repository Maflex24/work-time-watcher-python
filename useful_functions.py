from colorama import init, Fore, Back, Style
init(autoreset=True)

show_debug_info = False
def debugInfo(*args):
    if show_debug_info:    
        print(Fore.BLUE + Style.BRIGHT + 'debug info:', args)

def error(*args):
    print(Fore.RED + "Error: ",  args)

def info(description, *args):
    print(Fore.CYAN + description, args)

def function_test(function):
    if function:
        info(f'{function} passed')
    else:
        error(f"{function} not passed")

def todo(*args):
    print(Fore.LIGHTRED_EX + 'TODO this', args )

# https://www.delftstack.com/howto/python/python-clear-console/
import os
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def clear():
    clearConsole()