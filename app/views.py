from app import app
from flask import request, render_template, redirect, url_for

from forms import TodoForm
from models import TodoSQLite
import crud

@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            conn = crud.create_connection(r"todos_database.db")
            crud.create_todo(conn, form.data['title'], form.data['description'], form.data['done'])
            crud.close_connection(conn)
        return redirect(url_for("todos_list"))    
    conn = crud.create_connection(r"todos_database.db")
    todo_list= [TodoSQLite(row[0], row[1], row[2], row[3]) for row in crud.select_all_todos(conn)]
    crud.close_connection(conn)
    return render_template("todos.html", form=form, todos=todo_list, error=error)


@app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    conn = crud.create_connection(r"todos_database.db")
    todo = TodoSQLite(*(crud.select_todo_where(conn, 'id', todo_id))[0])
    crud.close_connection(conn)
    form = TodoForm(data=todo.__dict__)
    if request.method == "POST":
        if form.validate_on_submit():
            conn = crud.create_connection(r"todos_database.db")
            crud.update_todo(conn, todo_id, form.data['done'])
            crud.close_connection(conn)
        return redirect(url_for("todos_list"))
    return render_template("todo.html", form=form, todo_id=todo_id)
