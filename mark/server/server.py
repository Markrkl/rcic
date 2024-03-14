from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import RedirectResponse
import mysql.connector

print("creating FastAPI app")
app = FastAPI(
    title="bileti", 
    version="lab1", 
    description="server_description"
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

#=====================================
global db
db = mysql.connector.connect(
  host="127.0.0.1",
  user="admin123",
  password="pass",
  database="bilet_bd"
)
print("connected to MySQL at "+str(db.server_host)+":"+str(db.server_port))

@app.get("/tickets/list/all")
async def ticketsGetAll():
    cursor = db.cursor()
    SQL = "SELECT * FROM `tickets`"
    cursor.execute(SQL)
    data = cursor.fetchall()
    result = str(data)
    return {"success":result}

@app.get("/tickets/list/transport")
async def ticketsGetTransport(transport):
    cursor = db.cursor()
    SQL = "SELECT * FROM `tickets` WHERE transport="+transport
    cursor.execute(SQL)
    data = cursor.fetchall()
    result = str(data)
    return {"success":result}

@app.post("/tickets/add")
async def ticketsAdd(transport: int = Form(...), voditel: int = Form(...), marshrut: str = Form(...), mest: int = Form(...)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM `users`")
    users = cursor.fetchall()
    cursor.execute("SELECT id FROM `transport`")
    apps = cursor.fetchall()
    cursor.execute("SELECT transport, voditel, marshrut, mest FROM `tickets`")
    tickets = cursor.fetchall()
    bug_added = (transport, voditel, marshrut, mest)
    app_found = False
    user_found = False
    bug_already = False
    for app in apps:
        if app[0] == transport:
            app_found = True
    if not app_found:
        return {"status":"transport not found"}
    for user in users:
        if user[0] == voditel:
            user_found = True
    if not user_found:
        return {"status":"user not found"}
    if bug_added in tickets:
        bug_already = True
        return {"status":"ticket already exists"}
    
    sql = "INSERT INTO tickets (transport, voditel, marshrut, mest) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, bug_added)
    db.commit()
    if cursor.rowcount>0:
        return {"status":"success"}
    else:
        return {"status":"failed to add to DB"}

@app.post("/tickets/delete")
async def ticketsDelete(id: int = Form(...)):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM `tickets`")
    tickets = cursor.fetchall()
    if (id,) not in tickets:
        return {"status":"not found"}
    
    sql = "DELETE FROM tickets WHERE id=%s"
    cursor.execute(sql, (id,))
    db.commit()
    if cursor.rowcount>0:
        return {"status":"success"}
    else:
        return {"status":"failed to delete"}


@app.post("/tickets/edit")
async def ticketsEdit(id: int = Form(...), transport: int = Form(...), voditel: int = Form(...), marshrut: str = Form(...), mest: str = Form(...)):
    cursor = db.cursor()
    app_found = False
    user_found = False
    bug_found = False
    cursor.execute("SELECT id FROM `transport`")
    apps = cursor.fetchall()
    for app in apps:
        if app[0] == transport:
            app_found = True
    if not app_found:
        return {"status":"transport not found"}
    cursor.execute("SELECT * FROM `users`")
    users = cursor.fetchall()
    for user in users:
        if user[0] == voditel:
            user_found = True
    if not user_found:
        return {"status":"user not found"}
    cursor.execute("SELECT * FROM `tickets`")
    tickets = cursor.fetchall()
    for bug in tickets:
        if bug[0] == id:
            bug_found = True
    if not bug_found:
        return {"status":"not found"}
    
    sql = "UPDATE tickets SET transport=%s, voditel=%s, marshrut=%s, mest=%s WHERE id=%s"
    cursor.execute(sql, (transport, voditel, marshrut, mest, id))
    db.commit()
    if cursor.rowcount>0:
        return {"status":"success"}
    else:
        return {"status":"failed to update"}
    
@app.get("/tickets/list/open")
async def ticketsGetWorked():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM `tickets` WHERE mest!=0")
    tickets = cursor.fetchall()
    if len(tickets)>0:
        return {"success":str(tickets)}
    else:
        return {"status":"no open tickets"}

@app.get("/tickets/list/fixed")
async def ticketsGetClosed():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM `tickets` WHERE mest=0")
    tickets = cursor.fetchall()
    if len(tickets)>0:
        return {"success":str(tickets)}
    else:
        return {"status":"no fixed tickets"}

@app.post("/users/register")
async def usersRegister(name: str = Form(...), password: str = Form(...), access: str = Form(...)):
    cursor = db.cursor()
    user_found = False
    cursor.execute("SELECT name FROM `users`")
    users = cursor.fetchall()
    if (name,) in users:
        return {"status":"already exists"}
    
    sql = "INSERT INTO users (name, password, access) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, password, access))
    db.commit()
    if cursor.rowcount>0:
        return {"status":"success"}
    else:
        return {"status":"failed to add to DB"}


@app.post("/users/login")
async def usersLogin(name: str = Form(...), password: str = Form(...)):
    cursor = db.cursor()
    user_found = False
    cursor.execute("SELECT * FROM `users`")
    users = cursor.fetchall()
    for user in users:
        checking = (user[1], user[2])
        if checking == (name, password):
            id = user[0]
            access = user[3]
            return {"status":(id, access)}
    return {"status":"failed"}

#=====================================

@app.get("/connection/ping")
def pong():
    return {"message":"pong"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
