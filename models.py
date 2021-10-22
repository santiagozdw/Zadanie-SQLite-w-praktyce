import json


class Todos:
    def __init__(self):
        try:
            with open("todos.json", "r") as f:
                self.todos = json.load(f)
        except FileNotFoundError:
            self.todos = []

    def all(self):
        return self.todos

    def get(self, id):
        return self.todos[id]

    def create(self, data):
        data.pop('csrf_token')
        self.todos.append(data)

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump(self.todos, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.todos[id] = data
        self.save_all()

class TodoSQLite:
    def __init__(self,id,  title, description, done = 'false'):
        self.id = id
        self.title = title
        self.description = description
        self.done = done

    def __repr__(self):
        return f'Todo({self.title}, {self.description}, {self.done})'

todos = Todos()