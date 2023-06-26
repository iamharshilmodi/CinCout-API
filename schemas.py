from marshmallow import Schema, fields

# Define Marshmallow schemas for the database tables

class InOutSchema(Schema):
    in_out_id = fields.Int(dump_only=True)
    mis = fields.Str(required=True)
    time_out = fields.Str(required=True)
    date_out = fields.Str(required=True)
    time_in = fields.Str(required=False)
    date_in = fields.Str(required=False)
    reason = fields.Str(required=True)
    destination = fields.Str(required=True)

    # student = fields.Nested('StudentSchema', exclude=('passoword'), dump_only=True)
    # student = fields.Nested('StudentSchema', exclude=('in_out_times',), dump_only=True)
    # student = fields.Nested('StudentSchema', exclude=("password"), dump_only=True)

class loginSchema(Schema):
    mis = fields.Str(required=True)
    password = fields.Str(required=True)
    
class StudentSchema(Schema):
    mis = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    department = fields.Str(required=True)
    password = fields.Str(required=True)
    target = fields.Str(required=True)
    
    entries = fields.Nested(InOutSchema, many=True, dump_only=True)
    
class InOutTimeUpdateSchema(Schema):
    # id = fields.Int(required=True)
    mis = fields.Str(required=True)
    time_in = fields.Str(required=True)
    date_in = fields.Str(required=True)
    
# class StudentSchema(Schema):
#     mis = fields.Int(required=True)
#     first_name = fields.Str(required=True)
#     last_name = fields.Str(required=True)
#     email = fields.Email(required=True)
#     phone_number = fields.Str(required=True)
#     department = fields.Str(required=True)
#     password = fields.Str(load_only=True)
    
#     # Define a nested DepartmentSchema field to represent the department relationship
#     times = fields.List(fields.Nested(InOutTimeSchema()), dump_only=True)

