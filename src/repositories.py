import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import Session

import models


class TodoRepo:

    async def create(db: Session, id:int, title:str,completed:bool,order:int,url:str):
        db_todos = models.Todos(id=id,title=title, completed=completed, order=order,url=url)
        db.add(db_todos)
        db.commit()
        db.refresh(db_todos)
        return db_todos

    def fecth_is_exists(db:Session,_id):
        exists=db.query(
            db.query(models.Todos).filter_by(id=_id).exists()
        ).scalar()
        return exists

    def fetch_by_id(db: Session, _id):
        return db.query(models.Todos).filter(models.Todos.id == _id).first()

    def fetch_get_completed(db: Session, _id):
        return db.query(models.Todos.completed).filter(models.Todos.id ==_id)

    def fetch_get_order(db: Session, _id):
        return db.query(models.Todos.order).filter(models.Todos.id == _id)

    def fetch_get_url(db: Session, _id):
        return db.query(models.Todos.url).filter(models.Todos.id == _id)

    def fetch_get_title(db: Session, _id):
        return db.query(models.Todos.title).filter(models.Todos.id == _id)

    def fetch_by_name(db: Session, title):
        return db.query(models.Todos).filter(models.Todos.title == title).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Todos).offset(skip).limit(limit).all()

    def fetch_get_last_key(db: Session,):
        # session.query(func.count(Congress.id)).scalar()
        data = db.query(func.count(models.Todos.id)).scalar()
        return data

    async def delete(db: Session, todo_id):
        db_todo = db.query(models.Todos).filter_by(id=todo_id).first()
        db.delete(db_todo)
        db.commit()

    async def delete_all(db: Session):
        db.query(models.Todos).delete()
        db.commit()

    async def update(db: Session, todo_data):
        updated_todo = db.merge(todo_data)
        db.commit()
        return updated_todo


class TagRepo:

    async def create(db: Session, id:int, title:str,url:str):
        db_tag = models.Tags(id=id,title=title,url=url)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag

    def fetch_by_id(db: Session, _id: int):
        return db.query(models.Tags).filter(models.Tags.id == _id).first()

    # def fetch_by_name(db: Session, name: str):
        # return db.query(models.Store).filter(models.Store.name == name).first()
    def fetch_get_url(db: Session, _id):
        return db.query(models.Tags.url).filter(models.Todos.id == _id)

    def fetch_get_title(db: Session, _id):
        return db.query(models.Tags.title).filter(models.Todos.id == _id)

    def fecth_is_exists(db: Session, _id):
        exists = db.query(
            db.query(models.Tags).filter_by(id=_id).exists()
        ).scalar()
        return exists
    def fetch_get_last_key(db: Session,):
        # session.query(func.count(Congress.id)).scalar()
        data = db.query(func.count(models.Tags.id)).scalar()
        return data

    async def delete_all(db: Session):
        db.query(models.Tags).delete()
        db.commit()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Tags).offset(skip).limit(limit).all()

    async def delete(db: Session, _id: int):
        db_tags = db.query(models.Tags).filter_by(id=_id).first()
        db.delete(db_tags)
        db.commit()

    def fecth_is_exists(db: Session, _id):
        exists = db.query(
            db.query(models.Tags).filter_by(id=_id).exists()
        ).scalar()
        return exists

    async def update(db: Session, tag_data):
        updated_tag =db.merge(tag_data)
        db.commit()
        return updated_tag

class Relation:
    async def create(db: Session, id_todo: int, id_tag: int):
        db_rel = models.Relat(id_todo=id_todo, id_tag=id_tag)
        db.add(db_rel)
        db.commit()
        db.refresh(db_rel)
        return db_rel

    def fetch_all_by_id_todo(db: Session, id_todo:int, skip: int = 0, limit: int = 100):
        q= db.query(models.Tags)\
            .select_from(models.Tags)\
            .join(models.Relat, models.Relat.id_tag==models.Tags.id)\
            .filter(models.Relat.id_todo==id_todo)
        return q.all()

    def fetch_all_by_id_tag(db: Session, id_tag:int, skip: int = 0, limit: int = 100):
        q= db.query(models.Todos)\
            .select_from(models.Todos)\
            .join(models.Relat, models.Relat.id_tag==models.Todos.id)\
            .filter(models.Relat.id_tag==id_tag)
        return q.all()


    def fecth_is_exists(db: Session, _id_todo,_id_tag):
        exists = db.query(
            db.query(models.Relat).filter_by(id_todo=_id_todo, id_tag=_id_tag).exists()
        ).scalar()
        return exists

    async def delete(db: Session, _id_todo: int, _id_tag:int):
        db_tags = db.query(models.Relat).filter_by(id_todo=_id_todo,id_tag=_id_tag).first()
        db.delete(db_tags)
        db.commit()

    async def delete_all(db: Session):
        db.query(models.Relat).delete()
        db.commit()