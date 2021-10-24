# imports
from datetime import datetime, date, timedelta
from os.path import exists
from useful_functions import debugInfo, info, error, function_test, clearConsole, clear, todo
import json
import time


# variables
week = datetime.now().isocalendar()[1]
debugInfo("week", week)
weekday = datetime.now().weekday()
debugInfo("weekday", weekday)
today = date.today()
debugInfo("today", today)
file_name = f'week{week}_worktime.json'
debugInfo("file_name", file_name)
jsons_folder_path = 'worktime_jsons/'
existing_commands = ["help", "start", "exit", "work", "clear", "week"]
salary_per_hour = 7

week_worktimes = {
    'week': week,
    'work_days': [

    ]
}

# definitions
def week_file_is_created():
    is_file_created = exists(jsons_folder_path + file_name)
    return is_file_created

def create_json_file(path, file_name):
    with open(path + file_name, 'w+'):
        # todo obsługa tworzenia katalogu, jeśli ten nie istnieje
        debugInfo('json file was created')

def fetch_json_data(path, file_name):
    with open(path + file_name, 'r') as readed_file:
        global week_worktimes
        week_worktimes = json.load(readed_file)
        debugInfo('fetched json file')

def update_json_file(path, file_name, element):
    with open(path + file_name, 'w') as created_file:
        json.dump(element, created_file)
        debugInfo('updated json file')

def is_command_valid(user_command): 
    for command in existing_commands:
        if user_command == command:
            debugInfo("you choose existed command", user_command)
            return True
    return False

def execute_command(command):
    globals()[command]()

def help():
    info("possible commands:", existing_commands)

def fill_week_data():
    global week_worktimes
    global weekday

    temp_date = None
    if weekday > 0:
        temp_date = date.today() - timedelta(days=weekday)

    else: 
        temp_date = date.today()

    zero_date = temp_date
    for i in range(0, 7):
            temp_date = zero_date + timedelta(days=i)
            week_worktimes['work_days'].append(
                {
                    'weekday': temp_date.weekday(),
                    'date': {
                        'year': temp_date.year,
                        'month': temp_date.month,
                        'day': temp_date.day
                    },
                    'works': []
                }
            )
    debugInfo(week_worktimes)

def start():
    if not week_file_is_created():
        create_json_file(jsons_folder_path, file_name)
        fill_week_data()
        update_json_file(jsons_folder_path, file_name, week_worktimes)
    else:
        print("Week file was created earlier")

def week():
    print_work_stats('week')

def add_work_information(key):
    week_worktimes['work_days'][weekday]['works'].append(
        {
            f'{key}': datetime.now().timestamp()
        }
    )

def update_work_data():
    id = len(week_worktimes['work_days'][weekday]['works']) - 1
    debugInfo("id", id)
    work_session_data = week_worktimes['work_days'][weekday]['works'][id]
    debugInfo("work_session_data", work_session_data)

    work_session_data['stop'] = datetime.now().timestamp()
    work_session_data['total'] = work_session_data['stop'] - work_session_data['start']

def print_salary(salary_per_hour, timestamp):
    date = datetime.utcfromtimestamp(timestamp)

    salary = (date.hour * salary_per_hour) + (salary_per_hour / 60 * date.minute)
    info(f'You earned today: {round(salary, 2)} Eur')

def return_salary(salary_per_hour, timestamp):
    date = datetime.utcfromtimestamp(timestamp)

    salary = (date.hour * salary_per_hour) + (salary_per_hour / 60 * date.minute)
    return round(salary, 2)

def print_work_stats(time_range):
    if time_range == 'today':
        clear()
        total_time = 0
        for works in week_worktimes['work_days'][weekday]['works']:
            total_time += works['total']

        total_date = datetime.utcfromtimestamp(total_time)
        info(f'You worked today:', f'{total_date.hour} hours and {total_date.minute} minutes')
        print_salary(salary_per_hour, total_time)

    if time_range == 'week':
        clear()
        total_for_day = 0
        week_total = 0

        for days in week_worktimes['work_days']:
            # days to cały dany dzień
            for works in days['works']:
                # works to już zapisy pracy w danym dniu
                total_for_day += works['total']

            debugInfo(f'total for day {days["weekday"]} ({days["weekday"] + 1}) is: {total_for_day}')

            date_day = datetime.utcfromtimestamp(total_for_day)
            info(f"You worked {days['date']['day']}.{days['date']['month']}.{days['date']['year']} {date_day.hour} hours and {date_day.minute} minutes, earned: {return_salary(salary_per_hour, total_for_day)} EUR")

            week_total += total_for_day
            total_for_day = 0

        debugInfo("")
        debugInfo('total for week is:', week_total)
        week_work_time = datetime.utcfromtimestamp(week_total)

        print('')
        info(f"You worked this week: {week_work_time.hour} hours and {week_work_time.minute} minutes")
        info(f'You earned this week: {return_salary(salary_per_hour, week_total)} EUR')

def work_loop(meter):
    try:
        update_work_data()
        print_work_stats('today')

        if meter % 3 == 0:
            update_json_file(jsons_folder_path, file_name, week_worktimes)

        meter += 1
        time.sleep(15)
        work_loop(meter)

    except KeyboardInterrupt:
            info("waiting loop was stopped")
            update_json_file(jsons_folder_path, file_name, week_worktimes)

def work():
    if week_file_is_created():
        add_work_information('start')
        update_json_file(jsons_folder_path, file_name, week_worktimes)
        work_loop(0)

    else:
        error("first you need to use command 'start' to create today .json file")

# main section
user_command = 'not started'
def main():
    if week_file_is_created(): #FIXME if file is created, but it's empty, json have error
        fetch_json_data(jsons_folder_path, file_name)
    
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