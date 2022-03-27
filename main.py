import os

import psutil,time,sys,copy,platform,subprocess,hashlib
from datetime import datetime
"""
    thanks to https://www.programiz.com/python-programming/datetime/current-datetime for date-time handling
"""



def manual(date1,date2):
    line = None
    counter = 0
    try:
        with open("./statusLog.txt", "r") as file:
            #print("mod%s"%time.ctime(os.path.getmtime("./statusLog.txt")))
            while line != "":
                line = file.readline()
                #print(len(line))
                if(line == ""):
                    continue
                try:
                    updateDate = datetime.strptime(line[0:19],"%d/%m/%Y %H:%M:%S")
                except:
                    print("data corrupted, please delete document and try again")
                    return
                if(date2 <= updateDate and updateDate <= date1):
                    print(line[:-1])
                    counter+=1
        if(counter==0):
            print("no logs were founds")

    except:
        print("file could not be opened")


def writeMonitorData(list1,dt_string,operSYstem):
    try:
        with open("./serviceList.txt", "w") as file:  # open new file
            file.write(f"data logging time: {dt_string}\n")
            file.write("services:\n")
            ptt = subprocess.check_output(["service","--status-all"])
            if(operSYstem == "Linux"):
                LinuxServices = subprocess.check_output(["service", "--status-all"]).decode("utf-8")
                for serv in LinuxServices.split("\n"):
                    if(len(serv) == 0):
                        continue
                    name = serv[8:]
                    if(serv[3] == '-'):
                        list1[name] = "stopped"
                    else:
                        list1[name] = "running"
                        file.write(name + "\n")

                    #print(serv[3])
            elif(operSYstem == "Windows"):
                for i in psutil.win_service_iter():
                    list1[i.name()] = i.status()
                    if(i.status() == "running"):
                        file.write(str(i.name()) + "\n")

    except Exception as e:
        print(str(e))

def fileWrite(filename,message):
    try:
        with open("./" + filename, "a") as file:  # open new file
            file.write(message)
    except Exception as e:
        print(str(e))

def compareDicts(list1, list2, dt_string):
    for key in list1.keys():
        if key not in list2:
            fileWrite("statusLog.txt",f"{dt_string}: {key} is now {list1[key]}\n")
            print(f"{dt_string}: {key} is added and {list1[key]}")
        elif(list2[key] != list1[key]):
            fileWrite("statusLog.txt",f"{dt_string}: {key} is now {list1[key]}\n")
            print(f"{dt_string}: {key} is now {list1[key]}")

    for key in list2.keys():
        if key not in list1:
            fileWrite("statusLog.txt",f"{dt_string}: {key} is deleted\n")
            print(f"{dt_string}: {key} is deleted")

def initialInputHandler():
    #print("enter mode type (monitor or manual):")
    #print(platform.system())
    operSystem = platform.system()

    if not os.path.exists("./serviceList.txt"):
        with open("./serviceList.txt", "w") as file:
            pass
    if not os.path.exists("./statusLog.txt"):
         with open("./statusLog.txt", "w") as file:
             pass

    mode = input("enter mode type (monitor or manual): ")
    if(mode == "monitor"):
        validInput = False
        while not validInput:
            try:
                Intervaltime = int(input("enter time interval "))
                validInput = True
            except:
                print("invalid input")
        list1 = {}
        list2 = {}
        fitstTime = True
        while True:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            list1 = {}
            writeMonitorData(list1, dt_string,operSystem)
            if not fitstTime:
                compareDicts(list1,list2,dt_string)
            fitstTime = False
            list2 = copy.deepcopy(list1)
            time.sleep(Intervaltime)

    elif(mode == "manual"):
        """
        date and time input - thanks to:
        https://www.code4example.com/python/python-user-input-date-and-time/"""
        #print("enter first date and time: (format: yyyy/mm/dd hh:mm:ss)")

        dateEnter = False
        my_date1 = None
        my_date2 = None
        while not dateEnter:
            try:
                my_string = str(input('Enter date 1 (yyyy-mm-dd hh:mm:ss): '))
                my_date1 = datetime.strptime(my_string, "%Y-%m-%d %H:%M:%S")

                my_string2 = str(input('Enter date 2 (yyyy-mm-dd hh:mm:ss): '))
                my_date2 = datetime.strptime(my_string2, "%Y-%m-%d %H:%M:%S")
                dateEnter = True
            except:
                print("invalid date or time")


        if(my_date2 > my_date1):
            temp = my_date2
            my_date2 = my_date1
            my_date1 = temp
        manual(my_date1,my_date2)




initialInputHandler()