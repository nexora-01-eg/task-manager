from flask import Flask, request, jsonify
from models import db, Task
from schemas import task_schema, tasks_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

ALLOWED_STATUSES = {'todo', 'doing', 'done'}
ALLOWED_PRIORITIES = {'low', 'medium', 'high'}

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    # Validate status and priority
    if data['status'] not in ALLOWED_STATUSES:
        return jsonify({'error': 'Invalid status'}), 422
    if data['priority'] not in ALLOWED_PRIORITIES:
        return jsonify({'error': 'Invalid priority'}), 422
    
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
    
    # Validate status and priority
    if 'status' in data and data['status'] not in ALLOWED_STATUSES:
        return jsonify({'error': 'Invalid status'}), 422
    if 'priority' in data and data['priority'] not in ALLOWED_PRIORITIES:
        return jsonify({'error': 'Invalid priority'}), 422
    
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
