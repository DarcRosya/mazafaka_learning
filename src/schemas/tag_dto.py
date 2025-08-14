from pydantic import BaseModel

# if TYPE_CHECKING:
#     from src.schemas.task_dto import TaskRead

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagRead(TagBase):
    id: int

    class Config:
        from_attributes = True

# class TagsWithTaskRead(TagRead):
#     tasks: list["TaskRead"]