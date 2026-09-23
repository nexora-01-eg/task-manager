from flask import Flask, request, jsonify, send_from_directory
from models import db, Task
from schemas import task_schema, tasks_schema
from datetime import datetime

ALLOWED_STATUSES = {'todo', 'doing', 'done'}
ALLOWED_PRIORITIES = {'low', 'medium', 'high'}

def validate_task_data(data):
    if data['status'] not in ALLOWED_STATUSES:
        return jsonify({'error': f'Invalid status: {data["status"]}. Allowed statuses are: {", ".join(ALLOWED_STATUSES)}'}), 422
    if data['priority'] not in ALLOWED_PRIORITIES:
        return jsonify({'error': f'Invalid priority: {data["priority"]}. Allowed priorities are: {", ".join(ALLOWED_PRIORITIES)}'}), 422
    try:
        datetime.strptime(data['due_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid due date format. Please use ISO format (YYYY-MM-DD)'}), 400
    return None

def validate_page_and_per_page(page, per_page):
    try:
        page = int(page)
        per_page = int(per_page)
    except ValueError:
        return jsonify({'error': 'page and per_page must be integers'}), 422
    if page < 1 or per_page < 1:
        return jsonify({'error': 'page and per_page must be greater than 0'}), 422
    return None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    error = validate_task_data(data)
    if error:
        return error
    
    new_task = Task(title=data['title'], description=data['description'], status=data['status'], priority=data['priority'], due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'))
    db.session.add(new_task)
    db.session.commit()
    return jsonify(task_schema.dump(new_task)), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    q = request.args.get('q', type=str, default=None)
    status = request.args.get('status', type=str, default=None)
    priority = request.args.get('priority', type=str, default=None)
    page = request.args.get('page', type=int, default=1)
    per_page = request.args.get('per_page', type=int, default=10)

    error = validate_page_and_per_page(page, per_page)
    if error:
        return error

    if status and status not in ALLOWED_STATUSES:
        return jsonify({'error': f'Invalid status: {status}. Allowed statuses are: {", ".join(ALLOWED_STATUSES)}'}), 422
    if priority and priority not in ALLOWED_PRIORITIES:
        return jsonify({'error': f'Invalid priority: {priority}. Allowed priorities are: {", ".join(ALLOWED_PRIORITIES)}'}), 422

    query = Task.query
    if q:
        query = query.filter((Task.title.ilike(f'%{q}%')) | (Task.description.ilike(f'%{q}%')))
    if status and status in ALLOWED_STATUSES:
        query = query.filter(Task.status == status)
    if priority and priority in ALLOWED_PRIORITIES:
        query = query.filter(Task.priority == priority)

    tasks = query.paginate(page=page, per_page=per_page, error_out=False)
    result = tasks_schema.dump(tasks.items)
    return jsonify({
        'items': result,
        'page': page,
        'per_page': per_page,
        'total': tasks.total
    })

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task_schema.dump(task))

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
    task.due_date = datetime.strptime(data.get('due_date', task.due_date), '%Y-%m-%d')
    db.session.commit()
    return jsonify(task_schema.dump(task))

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
