# imports
from datetime import datetime, time, date
from useful_functions import debugInfo, info, error, function_test, clearConsole, clear, todo
from os.path import exists
import json
import time

# definitions:
def create_json_file(path, file_name):
    with open(path + file_name, 'w+') as created_file:
        debugInfo('json file created')
        function_test(week_file_is_created())     
        
def update_json_file(path, file_name, element):
    with open(path + file_name, 'w') as created_file:
        json.dump(element, created_file)
        debugInfo('updated json file')

def read_json_file(path, file_name):
    with open(path + file_name, 'r') as readed_file:
        global times
        times = json.load(readed_file)
        debugInfo('readed json file')

def show_json_file_content(path):
    file_name = input("input file date in format: YYYY-MM-DD: ")
    with open(path + file_name + '_worktime.json', 'r') as readed_file:
        json_content = json.load(readed_file)
        info("json file content: ", json_content)

def data():
    try:
        show_json_file_content(path_of_file)
    except FileNotFoundError:
        error("File was not found. Wrong name?")

existing_commands = ["help", "start", "stop", "exit", "work", "w", "break", "b", "status", "clear", "data"]
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

def week_file_is_created():
    is_file_created = exists(path_of_file + today_file_name)
    return is_file_created

def help():
    info("possible commands:", existing_commands)

def start():
    if not week_file_is_created():
        create_json_file(path_of_file, today_file_name)
        times['today_date'] = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day) 
        debugInfo(times["today_date"])
        update_json_file(path_of_file, today_file_name, times)
    else:
        print("Session was already started")
    

def stop():
    todo("stop()")
    # TODO

counting = {
    "work_id": 0,
    "break_id": 0,
}

def work():
    if week_file_is_created():
        times["works"].append({'start': datetime.now().timestamp()})
        update_json_file(path_of_file, today_file_name, times)

        work_in_progress = True
        refresh_loop_id = 0
        while work_in_progress:
            try:
                clear()
                current_work = times['works'][counting["work_id"]]
                current_work['stop'] = datetime.now().timestamp()
                current_work['total'] = current_work['stop'] - current_work['start']
                print_work_time()
                time.sleep(10)

                if refresh_loop_id % 10 == 0: 
                    info("Type:'Ctrl + C to stop refreshing")
                if refresh_loop_id % 5 == 0: 
                    update_json_file(path_of_file, today_file_name, times)

                refresh_loop_id += 1

            except KeyboardInterrupt:
                clear()
                info("waiting loop was stopped")
                update_json_file(path_of_file, today_file_name, times)
                work_in_progress = False

        counting["work_id"] += 1
    else:
        error("first you need to use command 'start' to create today .json file")

salary_per_minute = 7 / 60

def print_work_time():
    total = 0
    global times
    for work_value in times['works']:
        try:
            total += work_value['total']
        except:
            error(work_value, 'has no argument "total"')

    t1 = datetime.fromtimestamp(total)
    salary = ((t1.hour - 1) * salary_per_minute * 60) + (salary_per_minute * t1.minute)
    print()
    info("Today total worktime is:", f'{t1.hour-1} hours and {t1.minute} minutes')
    info(f"You earned today: {round(salary, 2)} Eur")

def w(): work()

def break_in_work():
    if week_file_is_created():
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
    if week_file_is_created(): #FIXME if file is created, but it's empty, json have error
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
        


