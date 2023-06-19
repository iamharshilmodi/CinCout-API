from db import db 

class Blocklist(db.Model):
    __tablename__ = 'blocklist'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(), unique=True)
    
    def __init__(self, jti):
        self.jti = jti
        
        
    @classmethod
    def is_jti_revoked(cls, jti):
        # db = current_app.db
        revoked_token = cls.query.filter_by(jti=jti).first()
        return bool(revoked_token)
    
    # @classmethod
    # def find_by_jti(cls, jti):
    #     return cls.query.filter_by(jti=jti)