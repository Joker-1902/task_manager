from .database import Base
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
import uuid
from enum import Enum


class TaskStatus(str, Enum):
    CREATED = 'created'
    IN_PROCESS = 'in_process'
    DONE = 'done'



class Task(Base):
    __tablename__='tasks'
    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(String, default=TaskStatus.CREATED)
    