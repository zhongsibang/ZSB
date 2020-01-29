
from .config import URL, DATABASE_DEBUG
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship

# 状态
STATE_WAITING = 0
STATE_PENDING = 1
STATE_RUNNING = 2
STATE_SUCCESS = 3
STATE_FAILED  = 4
STATE_FINISH  = 5



Base = declarative_base()

# ORM
# 实体类
# 图
class Graph(Base):
    __tablename__ = 'graph'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), unique=True, nullable=False)
    desc = Column(String(200), nullable=True)
    checked = Column(Integer, nullable=False, server_default='0')
    sealed = Column(Integer, nullable=False, server_default='0')

    def __repr__(self):
        return '<Graph {}>'.format(self.id)

# 顶点表
class Vertex(Base):
    __tablename__ = 'vertex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    script = Column(Text, nullable=True)
    input = Column(Text, nullable=True)

    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)

    def __repr__(self):
        return '<Vertex {} {}>'.format(self.id, self.name)

# 边表
class Edge(Base):
    __tablename__ = 'edge'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tail = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    head = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)

    def __repr__(self):
        return "<Edge >"

##############
# pipeline
class Pipeline(Base):
    __tablename__ = 'pipeline'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), unique=True, nullable=False)
    desc = Column(String(200), nullable=True)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)
    state = Column(Integer, nullable=False, default=STATE_WAITING, index=True)

    tracks = relationship('Track', foreign_keys='Track.p_id')

    def __repr__(self):
        return '<Pipeline>'


# track
class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True, autoincrement=True)
    p_id = Column(Integer, ForeignKey('pipeline.id'), nullable=False)
    v_id = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    script = Column(Text, nullable=True)
    input = Column(Text, nullable=True)
    output = Column(Text, nullable=True)
    state = Column(Integer, nullable=False, default=STATE_WAITING, index=True)

    pipeline = relationship('Pipeline')
    vertex = relationship('Vertex')


    def __repr__(self):
        return '<Track>'

#######################
# 创建引擎、会话

from functools import wraps


def singleton(cls):
    instance = None

    @wraps(cls)
    def wrapper(*args, **kwargs):
        """function wrapper"""
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)

        return instance
    return wrapper

@singleton
class Database:
    def __init__(self, url, **kwargs):
        self._engine = create_engine(url, **kwargs)
        # thread-local的session类
        self._session = sessionmaker(bind=self._engine)() # 线程不安全

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine

    def create_all(self):
        Base.metadata.create_all(bind=self._engine)

    def drop_all(self):
        Base.metadata.drop_all(bind=self._engine)

db = Database(URL, echo=DATABASE_DEBUG)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    age = Column(Integer)

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.age)