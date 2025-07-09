import datetime
import enum
from typing import Optional, Annotated
from sqlalchemy import ForeignKey, Table, Column, Integer, String, MetaData, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256


intpk = Annotated[int, mapped_column(primary_key=True)]
str_100 = Annotated[str, mapped_column(String(100))]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now(datetime.timezone.utc)
    )]


class WorkersORM(Base):
    __tablename__ = "workers"

    id: Mapped[intpk] 
    username: Mapped[str]

    resumes: Mapped[list["ResumesORM"]] = relationship(
        back_populates="worker",
        # backref ="worker",
    )

    resumes_parttime: Mapped[list["ResumesORM"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersORM.id == ResumesORM.worker_id, ResumesORM.workload == 'parttime')",
        order_by="ResumesORM.id.desc()",
        # lazy="selectin", --- неявная подгрузка, вместо в
        # select_workers_with_condition_relationship .option это сделает тоже самое
        # но это не явно - поэтому не круто :)
    )



# backref создаст такое (если нет)
    # worker: Mapped["WorkersORM"] = relationship() 
# устаревшая методика, лучше явно указывать связи 


class WorkLoad(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class ResumesORM(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk] 
    title: Mapped[str_256] = mapped_column(String(256))
    compensation: Mapped[Optional[int]]
    workload: Mapped[WorkLoad]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at] 
    updated_at: Mapped[updated_at] 

    worker: Mapped["WorkersORM"] = relationship( # в кавычках чтобы небыло проблем с импортами при нескольких файлах с моделями
        back_populates="resumes",
    ) 

    repr_cols_num = 4
    repr_cols = ("created_at", )



























metadata_obj = MetaData()

workers_table = Table(
    "workers",  
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

