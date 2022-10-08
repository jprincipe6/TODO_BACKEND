from sqlalchemy import Column, Integer, String, Boolean

from db import Base


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), nullable=False, unique=True, index=True)
    completed = Column(Boolean, nullable=True)
    order = Column(Integer, nullable=True)
    url = Column(String(150), nullable=True)

    @classmethod
    def to_json(self):
        to_serialize = ['id', 'title', 'completed', 'order', 'url']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)

    def __repr__(self):
        return '{id:%s,title:%s, completed:%s,order:%s,url:%s}' % (
        self.id, self.title, self.completed, self.order, self.url)


class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), nullable=True)
    url = Column(String(150), nullable=True)

    def __repr__(self):
        return 'TagsModel{id:%s,title:%s,url:%s}' % (self.id, self.title, self.url)


class Relat(Base):
    __tablename__ = "relation"
    id_todo = Column(Integer, primary_key=True, index=True)
    id_tag = Column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return 'Relation{id_todo:%s,id_tag:%s}' % (self.id_todo, self.id_tag)
