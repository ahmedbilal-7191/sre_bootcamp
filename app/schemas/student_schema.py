from app.extensions import ma
from app.models.student import Student
from marshmallow import validates, ValidationError, fields, validate


class StudentSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    age = fields.Integer(required=True, validate=validate.Range(min=5, max=100))
    grade = fields.String(required=True, validate=validate.Length(min=1, max=20))
    email = fields.Email(required=True)

    class Meta:
        model = Student
        load_instance = True      # Deserialize into model instances
        include_fk = True         # Include foreign keys if any
        fields = ("id", "name", "age", "grade", "email", "created_at", "updated_at")
        dump_only = ("id", "created_at", "updated_at") #Read-only fields

    @validates('name')
    def validate_name(self, value):
        """Custom validation for complex rules built-in validators can't handle"""
        if not value.strip():
            raise ValidationError("Name cannot be empty or whitespace")
        if any(char.isdigit() for char in value):
            raise ValidationError("Name cannot contain numbers")
        