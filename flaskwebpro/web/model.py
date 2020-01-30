
from .config import DATABASE_DEBUG, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship

STATE_WAITING = 0
STATE_PENDING = 1
STATE_RUNNING = 2
STATE_SUCCEED = 3
STATE_FAILED  = 4
STATE_FINISH  = 5

# 基类
Base = declarative_base()

# schema定义
# 图
class Graph(Base):
    __tablename__ = 'graph'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False, unique=True)
    desc = Column(String(500), nullable=True)
    checked = Column(Integer, nullable=True, server_default='0')
    sealed = Column(Integer, nullable=True, server_default='0')

# 顶点表
class Vertex(Base):
    __tablename__ = 'vertex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    input = Column(Text, nullable=True) # 输入参数
    script = Column(Text, nullable=True) # 任务脚本
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)


# 边表
class Edge(Base):
    __tablename__ = 'edge'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tail = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    head = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)


# pipeline表
class Pipeline(Base):
    __tablename__ = 'pipeline'

    id = Column(Integer, primary_key=True, autoincrement=True)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)
    name = Column(String(48), nullable=False)
    state = Column(Integer, nullable=False, default=STATE_WAITING)
    desc = Column(String(200), nullable=True)

    # 从pipeline查轨迹信息
    tracks = relationship('Track', foreign_keys='Track.p_id')


# 历史轨迹track表
class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True, autoincrement=True)
    p_id = Column(Integer, ForeignKey('pipeline.id'), nullable=False)
    v_id = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    state = Column(Integer, nullable=False, default=STATE_WAITING)
    script = Column(Text, nullable=True)
    input = Column(Text, nullable=True)
    output = Column(Text, nullable=True)

    vertex = relationship('Vertex')
    pipeline = relationship('Pipeline')

    def __repr__(self):
        return '<Track {} {} {}>'.format(
            self.id, self.p_id, self.v_id
        )

    __str__ = __repr__


# 单例模式装饰器
from functools import wraps

def singleton(cls):
    instance = None

    @wraps(cls)
    def getinstance(*args, **kwargs):
        print(args, kwargs)
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance
    return getinstance

# 封装数据库引擎、会话

@singleton
class Database:
    def __init__(self, url, **kwargs):
        self._engine = create_engine(url, **kwargs)
        self._session = sessionmaker(bind=self._engine)()

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine

    # 创建表
    def create_all(self):
        Base.metadata.create_all(self._engine)

    # 删除表
    def drop_all(self):
        Base.metadata.drop_all(self._engine)

# 模块加载一次，db一个实例，用了单例装饰器，保证只有这一个实例
db = Database(URL, echo=DATABASE_DEBUG)
















