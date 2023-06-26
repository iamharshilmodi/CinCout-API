from db import db

class StudentModel(db.Model):
    __tablename__ = 'students'
    
    mis = db.Column(db.String(), primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    phone_number = db.Column(db.String(), unique=True, nullable=False)
    department = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    target = db.Column(db.String(), nullable=False)
    # department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)
    
    entries = db.relationship('InOutTime', backref='students', lazy=True)

    # times = db.relationship('InOutTime', backref="student", lazy=True)
    
    
    def json(self):
        return {
            'mis': self.mis,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'department': self.department,
            # 'entries': self.entries
        }

    @classmethod
    def find_by_mis(cls, mis):
        return cls.query.filter_by(mis=mis).first()
    
    @classmethod
    def find_all(cls):
        # return cls.query.options(db.defer(StudentModel.password)).all()
        return cls.query.with_entities(StudentModel.mis, StudentModel.first_name, StudentModel.last_name, StudentModel.email, StudentModel.phone_number, StudentModel.department).all()

    # @classmethod
    # def find_by_id(cls, _id):
    #     return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
