from datetime import datetime
from db.db import Base
from sqlalchemy import (Column, TIMESTAMP, BIGINT,UUID,
                        Integer, ForeignKey, String,text)
from sqlalchemy.orm import Mapped, mapped_column
from schemas.search import *


class Post(Base):
    __tablename__ = 'post'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(String, nullable=False)
    sys_task_id = Column(String, nullable=False)
    count_req = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    def to_read_model(self) -> PostRead:
        return PostRead(
            id=self.id,
            user_id=self.user_id,
            username=self.username,
            email=self.email,
            status=self.status,
            sys_task_id=self.sys_task_id,
            count_req=self.count_req,
            created_at=self.created_at
        )  
    
class Events(Base):
    __tablename__ = 'events'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    run_number = Column(Integer, nullable=False)
    event_number = Column(BIGINT, nullable=False)
    type = Column(String, nullable=False)
    version = Column(String, nullable=False)
    dsid = Column(Integer, ForeignKey('datasets.dsid'), primary_key=True, nullable=False)
    fuid_raw = Column(UUID, nullable=False)


    def to_read_model(self) -> EventRead:
        return EventRead(
            id=self.id,
            run_number=self.run_number,
            event_number=self.event_number,
            type=self.type,
            version=self.version,
            dsid=self.dsid,
            fuid_raw=self.fuid_raw
        )    
    
class Datasets(Base):
    __tablename__ = 'datasets'
    __table_args__ = {'extend_existing': True}
    
    dsid: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    dsn = Column(String, nullable=False)
    date = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'),onupdate=text('CURRENT_TIMESTAMP'))

    def to_read_model(self) -> DATASETS:
        return DATASETS(
            dsid=self.dsid,
            dsn=self.dsn,
            date=self.date
        )    
    
# class AIRFLOW_DATASETS(Base):
#     __tablename__ = 'airflowDataset'
#     __table_args__ = {'extend_existing': True}
    
#     dsid: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
#     dsn = Column(String, nullable=False)
#     date = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'),onupdate=text('CURRENT_TIMESTAMP'))
    
#     def to_read_model(self) -> AirflowDataset:
#         return AirflowDataset(
#             dsid=self.dsid,
#             dsn=self.dsn,
#             date=self.date
#         )       