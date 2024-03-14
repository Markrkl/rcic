import requests
import platform
import os

SERVER_URL = "http://127.0.0.1:8000/"
global id, access
id = None
access = None

def clearScreen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def login():
    while(True):
        clearScreen()
        global id, access
        print("Log into the system.")
        login = input("Login: ")
        password = input("Password: ")
        resp = requests.post(SERVER_URL+"users/login", data={"name":login, "password":password})
        if resp.json().get("status") != "failed":
            creds = list(resp.json().get("status"))
            id = creds[0]
            access = creds[1]
            print("logged in.")
            break
        else:
            print("failed, try again?")
            action = input("(y/n): ")
            if action == "y":
                pass
            else:
                break

def register(reg_access="user"):
    while(True):
        clearScreen()
        print("Register in the system.")
        login = input("Login: ")
        password = input("Password: ")
        resp = requests.post(SERVER_URL+"users/register", data={"name":login, "password":password, "access":reg_access})
        if resp.json().get("status") == "success":
            print("Registered successfully. Enter anything to get back to welcome menu.")
            input(": ")
            break
        else:
            print("failed, ["+resp.json().get("status")+"], try again?")
            action = input("(y/n): ")
            if action == "y":
                pass
            else:
                break

def listAllBugs():
    clearScreen()
    resp = requests.get(SERVER_URL+"bugs/list/all")
    if (resp.json().get("success")):
        print(resp.json().get("success"))
    print("enter anything to continue...")
    input(": ")
def listBugsFromApp():
    clearScreen()
    app = input("enter app id:")
    resp = requests.get(SERVER_URL+"bugs/list/app", params={"appid":app})
    if (resp.json().get("success")):
        print(resp.json().get("success"))
    print("enter anything to continue...")
    input(": ")
def listOpenBugs():
    clearScreen()
    resp = requests.get(SERVER_URL+"bugs/list/open")
    print(resp.json().get("status"))
    print("enter anything to continue...")
    input(": ")
def listFixedBugs():
    clearScreen()
    resp = requests.get(SERVER_URL+"bugs/list/fixed")
    print(resp.json().get("status"))
    print("enter anything to continue...")
    input(": ")
def addBug():
    clearScreen()
    appid = input("Enter app id: ")
    title = input("Enter title: ")
    resp = requests.post(SERVER_URL+"bugs/add", data={"appid":appid, "authorid":id, "title":title, "status":"open"})
    print(resp.json().get("status"))
    print("enter anything to continue...")
    input(": ")
def deleteBug():
    clearScreen()
    bugid = input("Enter bug id: ")
    resp = requests.post(SERVER_URL+"bugs/delete", data={"id":bugid})
    print(resp.json().get("status"))
    print("enter anything to continue...")
    input(": ")
def editBug():
    clearScreen()
    bugid = input("Enter bug id: ")
    appid = input("Enter NEW app id: ")
    authorid = input("Enter NEW author id: ")
    title = input("Enter NEW title: ")
    status = input("Enter NEW status: ")
    resp = requests.post(SERVER_URL+"bugs/edit", data={"id":bugid, "appid":appid, "authorid":authorid, "title":title, "status":status})
    print(resp.json().get("status"))
    print("enter anything to continue...")
    input(": ")
def registerAdmin():
    clearScreen()
    register("admin")

while(True):
    clearScreen()
    if id==None or access==None:    
        print("Bug_tracker welcome. \n 1. Login\n 2. Register\n 3. Exit")
        action = input("Selection: ")
        if action == "1":
            login()
        if action == "2":
            register()
        if action == "0":
            print("Exiting...")
            exit()
    else:
        print("WELCOME to the BUG_TRACKER menu. Select action:")
        if(access == "admin"):
            action = input(" 1. List all bugs\n 2. List bugs from app\n 3. List open bugs\n 4. List fixed bugs\n 5. Add bug\n 6. Delete bug\n 7. Edit bug\n 8. Register new admin\n 0. Logout\nSelection: ")
            if action=="1":
                listAllBugs()
            if action=="2":
                listBugsFromApp()
            if action=="3":
                listOpenBugs()
            if action=="4":
                listFixedBugs()
            if action=="5":
                addBug()
            if action=="6":
                deleteBug()
            if action=="7":
                editBug()
            if action=="8":
                registerAdmin()
            if action=="0":
                break
        if(access == "user"):
            action = input(" 1. List bugs from app\n 2. List open bugs\n 3. List fixed bugs\n 4. Add bug\n 0. Logout\nSelection: ")
            if action=="1":
                listBugsFromApp()
            if action=="2":
                listOpenBugs()
            if action=="3":
                listFixedBugs()
            if action=="4":
                addBug()
            if action=="0":
                break