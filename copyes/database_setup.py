import sys  
# для настройки баз данных 
from sqlalchemy import Column, ForeignKey, Integer, String  
  
# для определения таблицы и модели 
from sqlalchemy.ext.declarative import declarative_base  
  
# для создания отношений между таблицами
from sqlalchemy.orm import relationship  
from sqlalchemy import Column, Integer, DateTime
# для настроек
from sqlalchemy import create_engine 

# создание экземпляра declarative_base

Base = declarative_base() 

import datetime
# здесь добавим классы 
class Couriers(Base):  
    __tablename__ = 'Couriers'  


    courier_id = Column(Integer,primary_key=True, nullable=False)  
    courier_type = Column(String(4), nullable=False) 
    region = relationship("Regions",backref='Regions',
                                lazy='dynamic')
    working_hours = relationship('Working_hours',backref='Regions',
                                lazy='dynamic')

class Regions(Base):
    __tablename__ = 'Regions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    courier_id = Column(Integer, ForeignKey('Couriers.courier_id'),nullable=False)
    region = Column(Integer, nullable=False)

class Working_hours(Base):
    __tablename__ = 'Working_hours'  
    id = Column(Integer, primary_key=True, autoincrement=True)
    courier_id = Column(Integer, ForeignKey('Couriers.courier_id'),nullable=False)
    start_hours = Column(String(5), nullable=False)  
    end_hours =  Column(String(5), nullable=False)


# создает экземпляр create_engine в конце файла
 

engine = create_engine('mysql://root:Ficka1@2@3@@localhost:3306/couriers')  
  
Base.metadata.create_all(engine)



