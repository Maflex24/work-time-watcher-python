# imports
from datetime import datetime, time, date
from useful_functions import debugInfo
from useful_functions import error
from useful_functions import info
from useful_functions import function_test
from useful_functions import clearConsole
from useful_functions import clear
from os.path import exists
import json

# definitions:
def create_json_file(path, file_name):
    # times['session_day'] = session_day.timestamp()
    with open(path + file_name, 'w+') as created_file:
        # json.dump(times, created_file)
        function_test(today_file_is_created())
        
def update_json_file():
    pass

existing_commands = ["help", "start", "stop", "exit", "work", "w", "break", "b", "status", "clear"]
today_file_name = f'{date.today()}_worktime.json'
file_path = 'worktime_jsons/'

def is_command_valid(user_command): 
    for command in existing_commands:
        if user_command == command:
            debugInfo("you choose existed command", user_command)
            return True
    return False

def execute_command(command):
    if command == 'break':
        break_in_work()
    else:
        globals()[command]()

def today_file_is_created():
    is_file_created = exists(file_path + today_file_name)
    return is_file_created

def help():
    info("possible commands:", existing_commands)

def start():
    create_json_file(file_path, today_file_name)

def stop():
    pass
    # TODO

counting = {
    "work_id": 0,
    "break_id": 0,
}

def counting_increase(element, value):
    counting[element] += value
    debugInfo(f"counting[{element}]", counting[element])

def work():
    if today_file_is_created():
        counting_increase("work_id", 1)
        times[f'work_{counting["work_id"]}_start'] = datetime.now().timestamp()
        debugInfo(times)
        # TODO
    else:
        error("first you need to use command 'start' to create today .json file")

def w(): work()

def break_in_work():
    if today_file_is_created():
        counting_increase("break_id", 1)
        # TODO
    else:
        error("first you need to use command 'start' to create today .json file")

def b(): break_in_work()

def status():
    pass
    # TODO

# Dates
today = date.today()
times = {

    }
    

user_command = "not started"
while user_command != 'exit':
    print()
    user_command = input("Write command, type 'help' if you don't know what to choose: ")
    
    if is_command_valid(user_command) and user_command != 'exit':
        execute_command(user_command)
    elif user_command == 'exit':
            debugInfo("exit")
            pass
    else:
        error("Choose valid command!")

clearConsole()

