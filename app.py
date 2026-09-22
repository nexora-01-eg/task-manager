from flask import Flask, request, jsonify
from models import db, Task
from schemas import task_schema, tasks_schema

ALLOWED_STATUSES = {'todo', 'doing', 'done'}
ALLOWED_PRIORITIES = {'low', 'medium', 'high'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    error = validate_task_data(data)
    if error:
        return error
    
    new_task = Task(title=data['title'], description=data['description'], status=data['status'], priority=data['priority'], due_date=data['due_date'])
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = tasks_schema.dump(tasks)
    return jsonify(result)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    
    error = validate_task_data(data)
    if error:
        return error
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.due_date = data.get('due_date', task.due_date)
    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
