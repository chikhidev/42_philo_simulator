from prettytable import PrettyTable 
import os
from os import system
from time import sleep

RED = "\033[91m"
GREEN = "\033[92m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
END = "\033[0m"
BOLDRED = "\033[1;91m"
BOLDGREEN = "\033[1;92m"
BOLDMAGENTA = "\033[1;95m"

prev_line = None
speed = 0.8

def drawTable(philosophers):
    table = PrettyTable()
    table.title = "Philosophers"
    table.align = "l"
    table.min_width = 150
    table.field_names = ["Philosopher", "Status", "Number of forks", "Time"]
    for philosopher in philosophers:
        if philosopher['status'] == "has taken a fork ":
            philosopher['status'] += "🍴"
        elif philosopher['status'] == "is eating ":
            philosopher['status'] += "🍝"
        elif philosopher['status'] == "is sleeping ":
            philosopher['status'] += "😴"
        elif philosopher['status'] == "is thinking ":
            philosopher['status'] += "💭"
        elif philosopher['status'] == "died":
            philosopher['status'] += "💀"
        table.add_row([philosopher['name'], philosopher['status'], philosopher['nforks'], philosopher['time']])
    print(table)

def testCase(numOfPhilosophers, timeToDie, timeToEat, timeToSleep, numOfMeals):
    global prev_line

    system("clear")
    cmd = "./philo " + str(numOfPhilosophers) + " " + str(timeToDie) + " " + str(timeToEat) + " " + str(timeToSleep) + " "
    if (numOfMeals != -1):
        cmd += str(numOfMeals)

    philosophers = []

    for i in range(numOfPhilosophers):
        philosophers.append({ 'name': i+1, 'status': "Initial state", 'nforks': 0,'time': 0 })

    print(BOLDMAGENTA + "Running the philosophers..." + END)
    res = os.popen(cmd).read()

    step = 1

    lines = res.splitlines()

    for line in lines:
        try:
            split = line.split()
            time = int(split[0])
            name = int(split[1])
            status = ""
            for i in range(2, len(split)):
                status += split[i] + " "
            philosophers[name-1]['status'] = status

            if ((philosophers[name-1]['status'] == "has taken a fork ") and philosophers[name-1]['nforks'] < 2):
                philosophers[name-1]['nforks'] += 1
            else:
                philosophers[name-1]['nforks'] = 0

            philosophers[name-1]['time'] = time
            philosophers[name-1]['name'] = name
            system("clear")
            drawTable(philosophers)
            print("Total forks taken: " + BLUE + str(sum([philosopher['nforks'] for philosopher in philosophers])) + "\n" + END)
            print("current action:\n" + GREEN + line + END)
            print("previous action:\n" + MAGENTA + prev_line + END) if prev_line != None else None
            prev_line = line
            print("Step " + str(step) + " of " + str(len(lines)))
            step += 1
            sleep(speed)
        except Exception as e:
            print(e)

    

if __name__ == '__main__':
    print(BOLDMAGENTA + "Welcome to the philosophers tester!" + END)

    if (os.path.exists("philo") == False):
        print(BOLDRED + "Error: philo executable not found!" + END)
        exit(1)
    
    if (os.path.exists("Makefile") == False):
        print(BOLDRED + "Error: Makefile not found!" + END)
        exit(1)

    prompt = ""
    try:
        while (prompt ==  ""):
            prompt = input("Enter the prompt: ")
        inputs = prompt.split()
        numOfPhilosophers = int(inputs[0])
        timeToDie = int(inputs[1])
        timeToEat = int(inputs[2])
        timeToSleep = int(inputs[3])
        try:
            nm = inputs[4]
        except:
            nm = ""
        if (nm == ""):
            numOfMeals = 50
            print("simulating 50 meals as a limit...")
        else:
            numOfMeals = int(nm)

        speed_input = input("Enter the speed of the simulation (0.1 - 1) <0.8> by default: ")
        if (speed_input == ""):
            speed = 0.8
        else:
            speed = float(speed_input)

        testCase(numOfPhilosophers, timeToDie, timeToEat, timeToSleep, numOfMeals)

        print(BOLDGREEN + "Simulation ended!" + END)
    except Exception as e:
        print("Wrong prompt!")
