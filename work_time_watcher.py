# imports
from datetime import datetime, time, date
from useful_functions import debugInfo, info, error, function_test, clearConsole, clear
from os.path import exists
import json
import time

# definitions:
def create_json_file(path, file_name):
    # times['session_day'] = session_day.timestamp()
    with open(path + file_name, 'w+') as created_file:
        # json.dump(times, created_file)
        debugInfo('json file created')
        function_test(today_file_is_created())
        
        
def update_json_file(path, file_name, element):
    with open(path + file_name, 'w') as created_file:
        json.dump(element, created_file)
        debugInfo('updated json file')

def read_json_file(path, file_name):
    with open(path + file_name, 'r') as readed_file:
        global times
        times = json.load(readed_file)
        debugInfo('readed json file')

existing_commands = ["help", "start", "stop", "exit", "work", "w", "break", "b", "status", "clear"]
today_file_name = f'{date.today()}_worktime.json'
path_of_file = 'worktime_jsons/'

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
    is_file_created = exists(path_of_file + today_file_name)
    return is_file_created

def help():
    info("possible commands:", existing_commands)

def start():
    if not today_file_is_created():
        create_json_file(path_of_file, today_file_name)
        times['today_date'] = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day) 
        debugInfo(times["today_date"])
        update_json_file(path_of_file, today_file_name, times)
    else:
        print("Session was already started")
    

def stop():
    pass
    # TODO

counting = {
    "work_id": 0,
    "break_id": 0,
}

def work():
    if today_file_is_created():
        times["works"].append({'start': datetime.now().timestamp()})
        update_json_file(path_of_file, today_file_name, times)

        work_in_progress = True
        refresh_loop_id = 0
        while work_in_progress:
            try:
                current_work = times['works'][counting["work_id"]]
                current_work['stop'] = datetime.now().timestamp()
                current_work['total'] = current_work['stop'] - current_work['start']
                # debugInfo(current_work)
                print_work_time()
                time.sleep(10)

                if refresh_loop_id % 10 == 0: 
                    info("Type:'Ctrl + C to stop refreshing")
                if refresh_loop_id % 5 == 0: 
                    update_json_file(path_of_file, today_file_name, times)

                refresh_loop_id += 1

            except KeyboardInterrupt:
                info("waiting loop was stopped")
                
                update_json_file(path_of_file, today_file_name, times)
                work_in_progress = False
        counting["work_id"] += 1
    else:
        error("first you need to use command 'start' to create today .json file")

def print_work_time():
    total = 0
    global times
    for work_value in times['works']:
        try:
            total += work_value['total']
        except:
            error(work_value, 'has no argument "total"')

    t1 = datetime.fromtimestamp(total)
    info("total worktime is:", f'{t1.hour-1} hours and {t1.minute} minutes')
    print()

def w(): work()

def break_in_work():
    if today_file_is_created():
        # TODO
        pass
    else:
        error("first you need to use command 'start' to create today .json file")

def b(): break_in_work()

def status():
    pass
    # TODO

# Dates
today = date.today()
times = {
        'today_date': '',
        'worktime_hours': None,
        'worktime_minutes': None,
        'total_worktime': None,
        'total_breaktime': None,
        'works': [],
        'breaks': []
    }

user_command = "not started"
def main():
    if today_file_is_created(): #FIXME if file is created, but it's empty, json have error
        read_json_file(path_of_file, today_file_name)
        counting["work_id"] = len(times["works"])
        counting["break_id"] = len(times["breaks"])

    global user_command
    while user_command != 'exit':
        print()
        user_command = input("Write command, type 'help' if you don't know what to choose: ")
        
        if is_command_valid(user_command) and user_command != 'exit':
            execute_command(user_command)
        elif user_command == 'exit':
                debugInfo("exit")
                clearConsole()
                pass
        else:
            error("Choose valid command!")
            pass   
    
main()  
        


