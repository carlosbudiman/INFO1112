import os
import sys
import json
import datetime 
import re
import typing

def displaymenu():
    print("What would you like to do?")
    print("1. Complete tasks")
    print("2. Add a new meeting")
    print("3. Share a task")
    print("4. Share a meeting")
    print("5. Change Jafr's master directory")
    print("6. Exit")

    select = input()

    if select == '1':
        complete_task()
    elif select == '2':
        add_meeting()
    elif select == '3':
        share_task()
    elif select == '4':
        share_meeting()
    elif select == '5':
        change_jafr()
    elif select == '6':
        exit()

def complete_task():
    file = "tasks.md"
    with open(file, "r") as file:
        lines = file.readlines()

    notcompleted = []
    count = 1

    print("Which task(s) would you like to mark as completed?")
    for task in lines:
        if task.startswith("-") and "not complete" in task:
            task_description = task.replace("Due:", "by").replace("-", "").replace("not complete", "").strip()
            print(f"{count}. {task_description}")
            notcompleted.append(task)
            count += 1

    if not notcompleted:
        print("No tasks to complete!")
        return

    num = input()
    chosen = []
    for task_number in num.split(","):
        chosen.append(int(task_number.strip()))

    with open("tasks.md", "w") as file:
        for task in lines:
            if task in notcompleted:
                task_index = notcompleted.index(task)
                if task_index + 1 in chosen:
                    updated_line = task.replace("not complete", "complete")
                    file.write(updated_line)
                else:
                    file.write(task)
            else:
                file.write(task)



def add_meeting():
    description = input("Please enter a meeting description: \n")
    date = input("Please enter a date: \n")
    time = input("Please enter a time: \n")
    print(f"Ok, I have added {description} on {date} at {time}")

    with open("meetings.md", "a") as file:
        file.write(f"##### added by you\n- {description} Scheduled: {time} {date}.")

    share = input("Would you like to share this meeting? [y/n]: ")
    if share == "y":
        print("Who would you like to share with?")
        with open("passwd", "r") as file:
            lines = file.readlines()

        userlist = {}
      
        for i in lines:
            text = i.strip().split(":")
            username = text[0]
            id = text[2]
            print(f"{username} {id}")
            userlist[id] = username
        
        numuser = input()

        username = userlist.get(numuser)
        user_settings_path = os.path.join(username, ".jafr", "user-settings.json")
        with open(user_settings_path, "r") as json_file:
            settings = json.load(json_file)
            master_directory = settings.get("master", "")

        meetings_file_path = (master_directory + "/meetings.md").replace("/home/", "")
        with open(meetings_file_path, "a") as file:
            file.write(f"##### added by you\n- {description} Scheduled: {time} {date}.\n")

def share_task():
    file = "tasks.md"
    with open(file, "r") as file:
        lines = file.readlines()

    count = 1
    placeholder = []

    print("Which task would you like to share?")
    for task in lines:
        if task.startswith("-"):
            placeholder.append(task)
            task_description = task.replace("Due:", "").replace("-", "").replace("not complete", "").replace("complete", "").strip()
            print(f"{count}. {task_description}")
            count += 1
    #- Study 2's complement Due: 08/08/23 not complete\
    numtask = int(input())

    print("Who would you like to share with?")
    with open("passwd", "r") as file:
        lines = file.readlines()

    userlist = {}

    for i in lines:
        text = i.strip().split(":")
        username = text[0]
        id = text[2]
        print(f"{username} {id}")
        userlist[id] = username

    numuser = input()

    username = userlist.get(numuser)
    user_settings_path = os.path.join(username, ".jafr", "user-settings.json")
    with open(user_settings_path, "r") as json_file:
        settings = json.load(json_file)
        master_directory = settings.get("master", "")

    meetings_file_path = (master_directory + "/tasks.md").replace("/home/", "")
    with open(meetings_file_path, "a") as file:
        file.write(f"##### added by you\n{placeholder[numtask+1]}")

def share_meeting():
    file = "meetings.md"
    with open(file, "r") as file:
        lines = file.readlines()

    count = 1
    placeholder = []

    print("Which meeting would you like to share?")
    for meeting in lines:
        if meeting.startswith("-"):
            placeholder.append(meeting)
            dateformat = r"\d{2}/\d{2}/\d{2}"
            date = re.findall(dateformat, meeting)
            timeformat = r"\d{2}:\d{2}"
            time = re.findall(timeformat, meeting)
            task_description = meeting.replace("Scheduled:", "").replace("-", "").replace(time[0], "").replace(date[0], "").strip()
            print(f"{count}. {task_description} {date[0]}")
            count += 1
    #- Study 2's complement Due: 08/08/23 not complete\
    numtask = int(input())

    print("Who would you like to share with?")
    with open("passwd", "r") as file:
        lines = file.readlines()

    userlist = {}

    for i in lines:
        text = i.strip().split(":")
        username = text[0]
        id = text[2]
        print(f"{username} {id}")
        userlist[id] = username

    numuser = input()

    username = userlist.get(numuser)
    user_settings_path = os.path.join(username, ".jafr", "user-settings.json")
    with open(user_settings_path, "r") as json_file:
        settings = json.load(json_file)
        master_directory = settings.get("master", "")

    meetings_file_path = (master_directory + "/meetings.md").replace("/home/", "")
    with open(meetings_file_path, "a") as file:
        file.write(f"##### added by you\n{placeholder[numtask-1]} \n")


def change_jafr():
    newjafr = input("Which directory would you like Jafr to use?\n")

    with open(".jafr/user-settings.json", "r") as config:
        current = json.load(config)

    
    current["master"] = newjafr

    with open(".jafr/user-settings.json", "w") as config:
        json.dump(current, config, indent=4)


def main():
    sessioncount = 0
    displaymenu()
    sessioncount = sessioncount + 1
    while sessioncount>0:
        print("Just a friendly reminder! You have these tasks to finish today.")
         
        currentdate = datetime.date.today().strftime("%d/%m/%y")

        file = "tasks.md"

        with open(file, "r") as file:
            lines = file.readlines()

        todaytask = 0
        for task in lines:
            if currentdate in task:
                print(task)
                todaytask += 1
        if todaytask == 0:
            print("No tasks today")

        print("These tasks need to be finished in the next three days!")

        onedays = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%y")

        twodays = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%d/%m/%y")

        threedays = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%d/%m/%y")

        taskcount = 0
        for task in lines:
            if str(onedays) in task or str(twodays) in task or str(threedays) in task:
                print(task)
                taskcount += 1
        if taskcount == 0:
            print("No tasks for the next three days")

        print("You have the following meetings today!")
        with open("meetings.md", "r") as file:
            lines = file.readlines()

        todaymeeting = 0
        for meeting in lines:
            if currentdate in meeting:
                print(meeting)
                todaymeeting += 1
        if todaymeeting == 0:
            print("No meetings today")

        print("You have the following meetings scheduled over the next week!")

        displaymenu()

if __name__ == '__main__':
    main()
