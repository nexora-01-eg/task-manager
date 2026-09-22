from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    status = fields.String(required=True)
    priority = fields.String(required=True)
    due_date = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
