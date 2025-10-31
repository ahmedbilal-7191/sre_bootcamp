from app.extensions import ma
from app.models.student import Student

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True      # Deserialize into model instances
        include_fk = True         # Include foreign keys if any
        include_relationships = True