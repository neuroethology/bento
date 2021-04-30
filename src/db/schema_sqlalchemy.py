# schema_sqlalchemy.py
"""
The SQLAlchemy-style python class representation of the Bento SQL schema.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String, Time, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from datetime import date
import enum

Base = declarative_base()

class SexEnum(enum.Enum):
    M = 1
    F = 2
    U = 3

class Animal(Base):
    """ mapper for the animal table """
    __tablename__ = 'animal'

    id = Column(Integer, primary_key=True)
    animal_services_id = Column(Integer)
    dob = Column(Date)
    sex = Column(Enum(SexEnum))     # SexEnum.M, F or U
    genotype = Column(String(128))  # genetic strain
    nickname = Column(String(128))  # investigator-specific identifier
    investigator_id = Column(Integer, ForeignKey('investigator.id'))

    def __repr__(self):
        return "<Animal(nickname='%s', id='%d', dob='%s', sex='%s', genotype='%s')>" % (
            self.nickname, self.animal_services_id, self.dob, self.sex, self.genotype)

class Investigator(Base):
    """ mapper for the investigator table """
    __tablename__ = 'investigator'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(32))
    last_name = Column(String(64))
    first_name = Column(String(64))
    institution = Column(String(64))
    e_mail = Column(String(128))
    sessions = relationship('Session')

    def __repr__(self):
        return "<Investigator(user_name='%s', last_name='%s', first_name='%s', institution='%s', e_mail='%s')>" % (
            self.user_name, self.last_name, self.first_name, self.institution, self.e_mail
        )
    
class Camera(Base):
    """ mapper for the camera table """
    __tablename__ = 'camera'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    model = Column(String(128))
    lens = Column(String(128))
    position = Column(String(128))

    def __repr__(self):
        return "<Camera(id='%d', name='%s', model='%s', kebs='%s', position='%s')>" % (
            self.id, self.name, self.model, self.lens, self.position
        )

class NeuralData(Base):
    """
    Mapper for neural_data table
    """
    __tablename__ = 'neural_data'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(512))
    sample_rate = Column(Float)
    format = Column(String(128))
    start_time = Column(Float)   # needs to be convertible to timecode
    start_frame = Column(Integer)
    stop_frame = Column(Integer)
    trial = Column(Integer, ForeignKey('trial.id'))   # 'Trial.trial_id' is quoted because it's a forward reference

    def __repr__(self):
        return "<NeuralData(file_path='%s', sample_rate='%f', format='%s', start_time='%f', start_frame='%d', stop_frame='%d')>" % (
            self.file_path, self.sample_rate, self.format, self.start_time, self.start_frame, self.stop_frame
        )

class VideoData(Base):
    """
    Mapper for video_data table
    """
    __tablename__ = 'video_data'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(512))
    sample_rate = Column(Float)
    start_time = Column(Float)   # needs to be convertible to timecode
    # start_frame = Column(Integer)
    # stop_frame = Column(Integer)
    camera_id = Column(Integer, ForeignKey('camera.id'))
    camera = relationship('Camera')
    trial = Column(Integer, ForeignKey('trial.id'))
    pose_data = relationship('PoseData')

    def __repr__(self):
        return "<VideoData(file_path='%s', sample_rate='%s', start_time='%s')>" % (
            self.file_path, self.sample_rate, self.start_time
        )

class Annotations(Base):
    """
    Mapper for annotations table
    """
    __tablename__ = 'annotations'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(512))
    sample_rate = Column(Float)
    format = Column(String(128), nullable=False)
    start_time = Column(Float)   # needs to be convertible to timecode
    start_frame = Column(Integer)
    stop_frame = Column(Integer)
    annotator_name = Column(String(128))
    method = Column(String(128))   # e.g. manual, MARS v1_8
    trial = Column(Integer, ForeignKey('trial.id'))

    def __repr__(self):
        return ( "<Annotations(file_path='%s', sample_rate='%s', format='%s',"
            " start_time='%s', start_frame='%s', stop_frame='%s',"
            " annotator_name='%s', method='%s')>" % (
            self.file_path, self.sample_rate, self.format,
            self.start_time, self.start_frame, self.stop_frame,
            self.annotator_name, self.method )
        )

class AudioData(Base):
    """
    Mapper for audio_data table
    """
    __tablename__ = 'audio_data'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(512))
    sample_rate = Column(Float)
    start_time = Column(Float)   # needs to be convertible to timecode
    processed_audio_file_path = Column(String(512))
    annotation_id = Column(Integer, ForeignKey('annotations.id'))
    trial = Column(Integer, ForeignKey('trial.id'))

    def __repr__(self):
        return ( "<AudioData(file_path='%s', sample_rate='%s', start_time='%s',"
            " start_frame='%s', stop_frame='%s', processed_audio_file_path='%s')>" % (
            self.file_path, self.sample_rate, self.start_time,
            self.start_frame, self.stop_time, self.processed_audio_file_path )
        )

class PoseData(Base):
    """
    Mapper for pose_data table
    """
    __tablename__ = 'pose_data'

    pose_id = Column(Integer, primary_key=True)
    file_path = Column(String(512))
    sample_rate = Column(Float)
    start_time = Column(Float)   # needs to be convertible to timecode
    format = Column(String(128), nullable=False)
    video = Column(Integer, ForeignKey('video_data.id'))
    trial = Column(Integer, ForeignKey('trial.id'))

    def __repr__(self):
        return ( "<PoseData(file_path='%s', sample_rate='%s', start_time='%s',"
            " start_frame='%s', stop_frame='%s', format='%s')>" % (
            self.file_path, self.sample_rate, self.start_time,
            self.start_frame, self.stop_frame, self.format )
        )

class OtherData(Base):
    """
    Mapper for other_data table
    """
    __tablename__ = 'other_data'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(512))
    sample_rate = Column(Float)
    start_time = Column(Float)   # needs to be convertible to timecode
    start_frame = Column(Integer)
    stop_frame = Column(Integer)
    format = Column(String(128))
    trial = Column(Integer, ForeignKey('trial.id'))

    def __repr__(self):
        return ( "<OtherData(file_path='%s', sample_rate='%s', start_time='%s',"
            " start_frame='%s', stop_frame='%s', format='%s')>" % (
            self.file_path, self.sample_rate, self.start_time,
            self.start_time, self.stop_frame, self.format )
        )

class Session(Base):
    """
    Mapper for session table
    """
    
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey('animal.id'), nullable=False)
    investigator_id = Column(Integer, ForeignKey('investigator.id'), nullable=False)
    base_directory = Column(String(512))
    experiment_date = Column(Date)
    session_num = Column(Integer)
    trials = relationship('Trial',
        cascade='all, delete, delete-orphan')

    def __repr__(self):
        return ( "<Session(experiment_date='%s',"
            " session_num='%d', animal_id='%s'>" % (
            ( self.experiment_date.isoformat()
                if isinstance(self.experiment_date, date)
                else self.experiment_date ),
            self.session_num, self.animal_id )
        )

class Trial(Base):
    """
    Mapper for trial table
    """
    __tablename__ = 'trial'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('session.id'))
    trial_num = Column(Integer)
    stimulus = Column(String(128))
    video_data = relationship('VideoData',
        cascade='all, delete, delete-orphan')    # could be more than one, e.g. top view, front view
    audio_data = relationship('AudioData',
        cascade='all, delete, delete-orphan')    # could be zero or more
    neural_data = relationship('NeuralData',
        cascade='all, delete, delete-orphan')
    pose_data = relationship('PoseData',
        cascade='all, delete, delete-orphan')
    annotations = relationship('Annotations',
        cascade='all, delete, delete-orphan')
    other_data = relationship('OtherData',
        cascade='all, delete, delete-orphan')

    def __repr__(self):
        return "<Trial(session_id='%d', trial_num='%d', stimulus='%s', base_directory='%s')>" % (
            ( self.session_id, self.trial_num, self.stimulus, self.base_directory )
        )

class LateralityEnum(enum.Enum):
    Nothing = 0
    Left = 1
    Right = 2
    Bilateral = 3

class Surgery(Base):
    """
    Mapper for surgery table
    """
    __tablename__ = 'surgery'

    animal_id = Column(Integer, ForeignKey('animal.id'), primary_key=True)
    investigator_id = Column(Integer, ForeignKey('investigator.id'), primary_key=True)
    date = Column(Date)
    implant_side = Column(Enum(LateralityEnum), default=LateralityEnum.Nothing)
    injection_side = Column(Enum(LateralityEnum), default=LateralityEnum.Nothing)
    procedure = Column(String(128))
    anesthesia = Column(String(128))
    follow_up_care = Column(String(128))

    def __repr__(self):
        return ( "<Surgery(date='%s', implant_side='%s', injection_side='%s',"
            " procedure='%s', follow_up_care='%s')>" % (
            self.date.isoformat(), self.implant_side, self.injection_side,
            self.procedure, self.follow_up_care )
        )

# config = {
#     'host': '192.168.1.10',
#     'port': '3307',
#     'user': 'datajoint',
#     'password': 'DataJoint4Bento!'
#     }

def new_session(username, password, host, port):
    bento_engine = create_engine(f"mysql+mysqldb://{username}:{password}@{host}:{port}/bento")
    return sessionmaker(bind=bento_engine)

def create_tables(session):
    Base.metadata.create_all(session.get_bind())