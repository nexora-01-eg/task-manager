# Task Manager

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/task-manager.git
   cd task-manager
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install Flask pytest
   ```

## Running Locally

1. Start the Flask application:
   ```sh
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

## API Endpoints

### List Tasks
- **Endpoint**: `/tasks`
- **Method**: `GET`
- **Parameters**:
  - `q` (optional): Search query.
  - `status` (optional): Filter by status.
  - `priority` (optional): Filter by priority.

### Create Task
- **Endpoint**: `/tasks`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "title": "Task Title",
    "description": "Task Description",
    "status": "todo",
    "priority": "low"
  }
  ```

### Update Task Status
- **Endpoint**: `/tasks/<int:id>`
- **Method**: `PUT`
- **Request Body**:
  ```json
  {
    "status": "done"
  }
  ```

### Delete Task
- **Endpoint**: `/tasks/<int:id>`
- **Method**: `DELETE`

## Running Tests

To run the tests, use the following command:
