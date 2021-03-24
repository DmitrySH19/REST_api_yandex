from app import db

class Couriers(db.Model):  
    __tablename__ = 'Couriers'  


    courier_id = db.Column(db.Integer,primary_key=True, nullable=False)  
    courier_type = db.Column(db.String(4), nullable=False) 
    region = db.relationship("Regions",backref='Regions',
                                lazy='dynamic')
    working_hours = db.relationship('Working_hours',backref='Regions',
                                lazy='dynamic')

class Regions(db.Model):
    __tablename__ = 'Regions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courier_id = db.Column(db.Integer, db.ForeignKey('Couriers.courier_id'),nullable=False)
    region = db.Column(db.Integer, nullable=False)

class Working_hours(db.Model):
    __tablename__ = 'Working_hours'  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courier_id = db.Column(db.Integer, db.ForeignKey('Couriers.courier_id'),nullable=False)
    start_hours = db.Column(db.String(5), nullable=False)  
    end_hours =  db.Column(db.String(5), nullable=False)
