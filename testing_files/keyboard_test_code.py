import sys, os, keyboard
from datetime import datetime, timedelta
 
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
 
def menu(cmd):
    clearConsole()
    if cmd == 'all':
        print(
              'w - Start work time\n'
              'b - Start break time\n'
              'n - Stop work time\n'
              'e - Exit\n'         
             )
         
    if cmd == 'break':
        print('w - Stop break, continue work time\n')
         
    if cmd == 'stop':
        print(
              'w - Continue work time\n'
              'e - Exit\n'         
             )
 
 
menu('all')
time_break_array = []
time_break_array_length = 0
time_stop_work = datetime.strptime('00:00:00.000000', '%H:%M:%S.%f')
 
time_loop = False
time_break_loop = False
 
while True:
    if keyboard.is_pressed('w'):
        if not time_loop:
            menu('all')
            time_start_work = datetime.now()
            time_stop_work_td = timedelta(hours=time_stop_work.hour, minutes=time_stop_work.minute, seconds=time_stop_work.second)
            time_loop = True
             
        if time_break_loop:
            time_break_loop = False
            time_stop_break = datetime.strptime(str(calculate_time_break), "%H:%M:%S.%f")
            time_break_array.append(timedelta(hours=time_stop_break.hour, minutes=time_stop_break.minute, seconds=time_stop_break.second))
            time_break_array_length = len(time_break_array)
             
 
    if keyboard.is_pressed('n'):
        if time_loop:
            menu('stop')
            time_loop = False
            time_stop_work = datetime.strptime(str(calculate_time_work), "%H:%M:%S.%f")
 
            sys.stdout.write("\rTime work: " + str(calculate_time_work))
            sys.stdout.flush()
 
 
    if keyboard.is_pressed('b'):
        if time_loop and not time_break_loop:
            menu('break')
            time_start_break = datetime.now()
            time_stop_break = datetime.strptime('00:00:00.000000', '%H:%M:%S.%f')
            time_stop_break_td = timedelta(hours=time_stop_break.hour, minutes=time_stop_break.minute, seconds=time_stop_break.second)            
            time_stop_work = datetime.strptime(str(calculate_time_work), "%H:%M:%S.%f")
             
            if time_break_array_length > 0:
                for i in range(time_break_array_length):
                    print(f"Time break [{i + 1}]: {time_break_array[i]}")
             
            time_loop = False
            time_break_loop = True
 
 
    if keyboard.is_pressed('e'):
        if not time_break_loop:
            try:
                clearConsole()
                print(f"Time work: {calculate_time_work}")
 
                if time_break_array_length > 0:
                    for i in range(time_break_array_length):
                        print(f"Time break [{i + 1}]: {time_break_array[i]}")
                else:
                    print('The break was not used!')
            except:
                clearConsole()
            finally:
                exit()
 
    if time_loop:
        calculate_time_work = datetime.now() - time_start_work
        calculate_time_work += time_stop_work_td
         
        sys.stdout.write("\rTime work: " + str(calculate_time_work))
        sys.stdout.flush()
 
    if time_break_loop:
        calculate_time_break = datetime.now() - time_start_break
        calculate_time_break += time_stop_break_td
         
        sys.stdout.write("\rTime break [" + str(time_break_array_length + 1) + "]: " + str(calculate_time_break))