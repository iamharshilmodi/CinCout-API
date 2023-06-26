from db import db 

class InOutTime(db.Model):
    __tablename__ = 'in_out_time'
    
    in_out_id = db.Column(db.Integer, primary_key=True)
    mis = db.Column(
        db.String(), db.ForeignKey('students.mis'), nullable=False
    )
    
    # time_in = db.Column(db.DateTime, nullable=True)
    # time_out = db.Column(db.DateTime, nullable=False)

    time_out = db.Column(db.String(), nullable=False)
    date_out = db.Column(db.String(), nullable=False)
    
    time_in = db.Column(db.String(), nullable=True)
    date_in = db.Column(db.String(), nullable=True)
    
    reason = db.Column(db.String(), nullable=False)
    destination = db.Column(db.String(), nullable=False)

    # Define a relationship to the Student table, using the student_id foreign key
    # student = db.relationship('Student', back_populates='in_out_times')

    def json(self):
        return {
            
            "id": self.in_out_id,
            "mis": self.mis,
            
            # "time_out": self.time_out,
            # "date_out": self.date_out,
            
            # "time_in": self.time_in,
            # "date_in": self.date_in,
            
            # "reason": self.reason,
            # "destination": self.destination

        }

    @classmethod
    def find_by_mis(cls, mis):
        obj = cls.query.filter_by(mis=mis).order_by(InOutTime.in_out_id.desc()).limit(10)
        print(type(obj))
        return obj
    
    @classmethod
    def find_by_id(cls, gid):
        return cls.query.filter_by(in_out_id=gid)
    
    @classmethod
    def find_latest(cls, gmis):
        return cls.query.filter_by(mis=gmis).order_by(InOutTime.in_out_id.desc()).first()
    
    @classmethod
    def find_by_date(cls, date, mis):
        return cls.query.filter_by(date_out=date, mis = mis)

    @classmethod
    def find_all(cls):
        return cls.query.limit(1).all()

    # @classmethod
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def update_to_db(self):
        db.session.commit()

    # @classmethod
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()