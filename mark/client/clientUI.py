from flask import Flask, request, redirect, render_template
import requests
from markupsafe import escape
import json

SERVER_URL = "http://127.0.0.1:8000/"
global userid, useraccess
userid = None
useraccess = None
app = Flask(__name__)

def header(title):
    global userid, useraccess
    credentials = ""
    if userid!=None:
        credentials = f"""Вошел как: {useraccess}. User id: {userid}. <a href="/logout">выйти</a>"""
    else:
        credentials = """Вход не выполнен."""
    header =    f"""<div class="header"><h2><a href="/">[ДМА] Билетная касса.</a> {title}</h2>
                    {credentials}</div>
                """
    return header

@app.get('/')
def index_page():
    if userid==None:
        returned = header("Index page.")+"""
        Начальная страница:<br>
        <a href="/login" class="button">Войти</a> 
        <a href="/register" class="button">зарегистрироваться</a><br>
        """
        return render_template("template.html", content=returned)
    else:
        if useraccess=="admin":
            returned = header("Index page.")+"""
            Select action:
            <a href="/alltickets" class="button">Просмотр билетов</a> 
            <a href="/apptickets" class="button">Билеты по транспорту</a> 
            <a href="/opentickets" class="button">Билеты со свободными местами</a> 
            <a href="/fixedtickets" class="button">Билеты без мест</a> 
            <a href="/addtick" class="button">Добавить билет</a> 
            <a href="/deltick" class="button">Удалить билет</a> 
            <a href="/edittick" class="button">Изменить билет</a> 
            <a href="/regadmin" class="button">Регистрация админа</a> 
            <a href="/logout" class="button">Выход</a> 
            """
            return render_template("template.html", content=returned)
        else:
            returned = header("Index page.")+"""
            Меню:
            <a href="/alltickets" class="button">Билеты</a> 
            <a href="/opentickets" class="button">Свободные билеты</a> 
            <a href="/fixedtickets" class="button">Без мест</a> 
            <a href="/logout" class="button">Выход</a> 
            """
            return render_template("template.html", content=returned)

@app.get('/login')
def login_get():
    returned = header("Login.")+"""
    <form method="post" action="/login">
    Логин: <input type="text" name="username"></input><br>
    Пароль: <input type="password" name="password"></input><br>
    <button type="submit">Отправить</button>
    </form>
    """
    return render_template("template.html", content=returned)

@app.post('/login')
def login_post():
    global userid,useraccess
    username = request.form.get("username")
    password = request.form.get("password")
    print(username + "!!" + password)
    resp = requests.post(SERVER_URL+"users/login", data={"name":username, "password":password})
    if resp.json().get("status") != "failed":
        creds = list(resp.json().get("status"))
        userid = creds[0]
        useraccess = creds[1]
        return redirect("/")
    else:
        returned = header("Log in (failed).")+"""
        Ошибка, попробуйте снова: <a href="/login" method="post">TRY AGAIN</a>
        """
        return render_template("template.html", content=returned)
    
@app.get('/register')
def register_get():
    returned = header("Register.")+"""
    <form method="post" action="/register">
    Логин: <input type="text" name="username"></input><br>
    Пароль: <input type="password" name="password"></input><br>
    <button type="submit">Отправить</button>
    </form>
    """
    return render_template("template.html", content=returned)

@app.post('/register')
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    resp = requests.post(SERVER_URL+"users/register", data={"name":username, "password":password, "access":"user"})
    if resp.json().get("status") == "success":
        returned = header("Register.")+"""Удачно. <a href="/">Вернуться на главную</a> страницу."""
        return render_template("template.html", content=returned)
    else:
        returned = header("Register (failed).")+"""
        Ошибка. <a href="/register">Попробовать снова?</a><br>
        Error message:"""+str(resp.json().get("status"))
        return render_template("template.html", content=returned)

@app.get('/logout')
def logout():
    global userid, useraccess
    userid=None
    useraccess=None
    returned = header("Logout.")+"""Выход успешен. <a href="/">вернуться</a>"""
    return render_template("template.html", content=returned)

@app.get('/alltickets')
def all_tickets():
    resp = requests.get(SERVER_URL+"tickets/list/all")
    if (resp.json().get("success")):
        tickets = eval(resp.json().get("success"))
        result = "<table>"
        result += "<tr><th>Номер билета</th><th>Тип транспорта</th><th>Водитель</th><th>Маршрут</th><th>Места</th></tr>"
        for bug in tickets:
            bugid = bug[0]
            appid = bug[1]
            author = bug[2]
            title = bug[3]
            status = bug[4]
            result+="<tr>"
            result+=f"<td>{bugid}</td><td>{appid}</td><td>{author}</td><td>{title}</td><td>{status}</td>"
            result+="</tr>"
        result += "</table>"
        returned = header("List all tickets.")+result
        return render_template("template.html", content=returned)
    else:
        returned = header("List all tickets (failed).")+str(resp.json())
        return render_template("template.html", content=returned)

@app.get('/apptickets')
def app_tickets():
    returned = header("List tickets from transport.")+"""
    <form method="post" action="/apptickets">
    Транспорт: <input type="text" name="app"></input><br>
    <button type="submit">submit</button>
    </form>
    """
    return render_template("template.html", content=returned)

@app.post('/apptickets')
def app_tickets_post():
    app = request.form.get("app")
    resp = requests.get(SERVER_URL+"tickets/list/transport", params={"transport":app})
    if (resp.json().get("success")):
        tickets = eval(resp.json().get("success"))
        result = "<table>"
        result += "<tr><th>Номер билета</th><th>Тип транспорта</th><th>Водитель</th><th>Маршрут</th><th>Места</th></tr>"
        for bug in tickets:
            bugid = bug[0]
            appid = bug[1]
            author = bug[2]
            title = bug[3]
            status = bug[4]
            result+="<tr>"
            result+=f"<td>{bugid}</td><td>{appid}</td><td>{author}</td><td>{title}</td><td>{status}</td>"
            result+="</tr>"
        result += "</table>"
        returned = header("List tickets from app.")+result
        return render_template("template.html", content=returned)
    else:
        returned = header("List tickets from app (failed).")+str(resp.json())
        return render_template("template.html", content=returned)

@app.get('/opentickets')
def open_tickets():
    resp = requests.get(SERVER_URL+"tickets/list/open")
    if resp.json().get("success"):
        tickets = eval(resp.json().get("success"))
        result = "<table>"
        result += "<tr><th>Номер билета</th><th>Тип транспорта</th><th>Водитель</th><th>Маршрут</th><th>Места</th></tr>"
        for bug in tickets:
            bugid = bug[0]
            appid = bug[1]
            author = bug[2]
            title = bug[3]
            status = bug[4]
            result+="<tr>"
            result+=f"<td>{bugid}</td><td>{appid}</td><td>{author}</td><td>{title}</td><td>{status}</td>"
            result+="</tr>"
        result += "</table>"
        returned = header("List open tickets.")+result
        return render_template("template.html", content=returned)
    else:
        returned = header("List open tickets (failed).")+"There was an error processing request:"+str(resp.json())
        return render_template("template.html", content=returned)

@app.get('/fixedtickets')
def fixed_tickets():
    resp = requests.get(SERVER_URL+"tickets/list/fixed")
    if resp.json().get("success"):
        tickets = eval(resp.json().get("success"))
        result = "<table>"
        result += "<tr><th>Номер билета</th><th>Тип транспорта</th><th>Водитель</th><th>Маршрут</th><th>Места</th></tr>"
        for bug in tickets:
            bugid = bug[0]
            appid = bug[1]
            author = bug[2]
            title = bug[3]
            status = bug[4]
            result+="<tr>"
            result+=f"<td>{bugid}</td><td>{appid}</td><td>{author}</td><td>{title}</td><td>{status}</td>"
            result+="</tr>"
        result += "</table>"
        returned = header("List fixed tickets.")+result
        return render_template("template.html", content=returned)
    else:
        returned = header("List fixed tickets (failed).")+"There was an error processing request:"+str(resp.json())
        return render_template("template.html", content=returned)

@app.get('/addtick')
def add_tickets():
    returned = header("Add ticket.")+"""
    <form method="post" action="/addtick">
    Транспорт: <input type="text" name="appid"></input><br>
    Маршрут: <input type="text" name="title"></input><br>
    <button type="submit">submit</button>
    </form>
"""
    return render_template("template.html", content=returned)

@app.post('/addtick')
def add_tickets_post():
    global userid, useraccess
    appid = request.form.get("appid")
    title = request.form.get("title")
    resp = requests.post(SERVER_URL+"tickets/add", data={"transport":appid, "voditel":userid, "marshrut":title, "mest":20})
    returned = header("Add ticket.")+str(resp.json().get("status"))
    return render_template("template.html", content=returned)

@app.get('/deltick')
def del_bug():
    returned = header("Delete билет.")+"""
    <form method="post" action="/deltick">
    Номер билета: <input type="text" name="bug"></input><br>
    <button type="submit">submit</button>
    </form>
"""
    return render_template("template.html", content=returned)

@app.post('/deltick')
def del_bug_post():
    bugid = request.form.get("bug")
    resp = requests.post(SERVER_URL+"tickets/delete", data={"id":bugid})
    returned = header("Delete ticket.")+str(resp.json().get("status"))
    return render_template("template.html", content=returned)

@app.get('/edittick')
def edit_bug():
    returned = header("Edit билет.")+"""
    <form method="post" action="/edittick">
    Номер билета: <input type="text" name="bugid"></input><br>
    Транспорт: <input type="text" name="appid"></input><br>
    Водитель: <input type="text" name="author"></input><br>
    Маршрут: <input type="text" name="title"></input><br>
    Места: <input type="text" name="status"></input><br>
    <button type="submit">Submit</button>
    </form>
"""
    return render_template("template.html", content=returned)

@app.post('/edittick')
def edit_bug_post():
    bugid = request.form.get("bugid")
    appid = request.form.get("appid")
    authorid = request.form.get("author")
    title = request.form.get("title")
    status = request.form.get("status")
    resp = requests.post(SERVER_URL+"tickets/edit", data={"id":bugid, "transport":appid, "voditel":authorid, "marshrut":title, "mest":status})
    if resp.json().get("status"):
        returned = header("Edit ticket.")+str(resp.json().get("status"))
    else:
        returned = header("Edit ticket (failed).")+"""There was an error processing your request. Error: """+str(resp.json())
    return render_template("template.html", content=returned)

@app.get('/regadmin')
def register_admin_get():
    returned = header("Register new admin.")+"""
    <form method="post" action="/regadmin">
    Логин: <input type="text" name="username"></input><br>
    Пароль: <input type="password" name="password"></input><br>
    <button type="submit">submit</button>
    </form>
    """
    return render_template("template.html", content=returned)

@app.post('/regadmin')
def register_admin_post():
    username = request.form.get("username")
    password = request.form.get("password")
    resp = requests.post(SERVER_URL+"users/register", data={"name":username, "password":password, "access":"admin"})
    if resp.json().get("status") == "success":
        returned = header("Register new admin.")+"""Registered successfully. You can <a href="/">return to index page</a> now."""
        return render_template("template.html", content=returned)
    else:
        returned = header("Register new admin (failed).")+"""
        Registering failed. <a href="/regadmin">Try again?</a><br>
        Error message:"""+str(resp.json().get("status"))
        return render_template("template.html", content=returned)
        
if __name__=='__main__':
    app.run(host="0.0.0.0", debug=True)