from flask import Flask
import crud


conn = crud.create_connection(r"todos_database.db")
crud.create_todos_table(conn)

app =  Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

from app import views