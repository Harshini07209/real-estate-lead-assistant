from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# create database + table
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    property TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

# input model
class Lead(BaseModel):
    name: str
    phone: str
    property: str

# home
@app.get("/")
def home():
    return {"message": "API is working"}

# add lead
@app.post("/add-lead")
def add_lead(lead: Lead):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO leads (name, phone, property, status) VALUES (?, ?, ?, ?)",
        (lead.name, lead.phone, lead.property, "new")
    )

    conn.commit()
    conn.close()

    return {"message": "Lead added"}

# get leads
@app.get("/leads")
def get_leads():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads")
    data = cursor.fetchall()

    conn.close()

    return data
class StatusUpdate(BaseModel):
    status: str

@app.put("/update-status/{lead_id}")
def update_status(lead_id: int, data: StatusUpdate):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE leads SET status = ? WHERE id = ?",
        (data.status, lead_id)
    )

    conn.commit()
    conn.close()

    return {"message": "Status updated"}