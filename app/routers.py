from fastapi import APIRouter, Depends, HTTPException
from .database import get_db
from .models import Task, TaskStatus
from sqlalchemy.orm import Session
from .schemas import TaskCreate, TaskOut, TaskUpdate
from uuid import UUID


router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get('/', summary='Получить списаок всех задач', response_model=list[TaskOut])
def get_list(db:Session=Depends(get_db)):
    return db.query(Task).all()


@router.get('/{uuid}', summary='Получить нужную задачу по uuid', response_model=TaskOut)
def get(uuid:UUID, db:Session=Depends(get_db)):
    task = db.query(Task).filter(Task.uuid == str(uuid)).first()
    if not task:
        raise HTTPException(status_code=404)
    return task


@router.post('/', summary='Сщздать новую задачу', response_model=TaskOut)
def create_task(new_task:TaskCreate,db:Session=Depends(get_db)):
    task = Task(**new_task.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch('/{uuid}', summary='Обновление всех полей или только нужных в задачах', response_model=TaskOut)
def update_task(uuid:UUID,update_task:TaskUpdate, db:Session=Depends(get_db)):
    task = db.query(Task).filter(Task.uuid == str(uuid)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Такой задачи не существует")
    if task.status == TaskStatus.DONE:
        raise HTTPException(status_code=403, detail="Нельзя менять статус завершенной задачи")

    
    for key,value in update_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete('/delete_all')
def delete_all(db:Session=Depends(get_db)):
    db.query(Task).delete(synchronize_session=False)
    db.commit()
    return {'message':'Все задачи успешно удалены'}


@router.delete('/{uuid}')
def delete_task(uuid:UUID,db:Session=Depends(get_db)):
    task = db.query(Task).filter(Task.uuid == str(uuid)).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail='Данная задача не существует'
        )
    
    db.delete(task)
    db.commit()
    return {"message": f"Задача <{task.title}> успешно удалена"}


