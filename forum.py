from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
from models import Forum_Replies, Forum_Topics
from pydantic import BaseModel, Field

forum_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ForumTopicCreate(BaseModel):
    course_id: int = Field(..., description="Course ID harus ada")
    student_id: int = Field(..., description="Student ID harus ada")
    title: str
    content: str
    created_at: datetime
    is_pinned: bool
    is_closed: bool

class ForumTopicUpdate(BaseModel):
    course_id: int
    student_id: int
    title: str
    content: str
    created_at: datetime
    is_pinned: bool
    is_closed: bool

class ForumTopicOut(BaseModel):
    topic_id: int
    course_id: int
    student_id: int
    title: str
    content: str
    created_at: datetime
    is_pinned: bool
    is_closed: bool

    class Config:
        orm_mode: True

class ForumReplyCreate(BaseModel):
    topic_id: int = Field(..., description="Topic ID harus ada")
    student_id: int = Field(..., description="Student ID harus ada")
    admin_id: int = Field(..., description="Admin ID harus ada")
    content: str
    created_at: datetime
    upvotes: int

class ForumReplyUpdate(BaseModel):
    topic_id: int
    student_id: int
    admin_id: int
    content: str
    created_at: datetime
    upvotes: int

class ForumReplyOut(BaseModel):
    reply_id: int
    topic_id: int
    student_id: int
    admin_id: int
    content: str
    created_at: datetime
    upvotes: int

    class Config:
        orm_mode: True

@forum_router.post("/create/topic/{course_id}", response_model=ForumTopicOut, status_code=status.HTTP_201_CREATED)
def create_forum_topic(topic: ForumTopicCreate, db: Session = Depends(get_db)):

    new_topic = Forum_Topics(
        course_id=topic.course_id,
        student_id=topic.student_id,
        title=topic.title,
        content=topic.content,
        created_at=topic.created_at,
        is_pinned=topic.is_pinned,
        is_closed=topic.is_closed
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic

@forum_router.post("/create/reply/{topic_id}", response_model=ForumReplyOut, status_code=status.HTTP_201_CREATED)
def create_forum_reply(reply: ForumReplyCreate, db: Session = Depends(get_db)):

    new_reply = Forum_Replies(
        topic_id=reply.topic_id,
        student_id=reply.student_id,
        admin_id=reply.admin_id,
        content=reply.content,
        created_at=reply.created_at,
        upvotes=reply.upvotes
    )
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply

@forum_router.get("/topics/{course_id}", response_model=List[ForumTopicOut])
def get_forum_topics(course_id: int, db: Session = Depends(get_db)):

    topics = db.query(Forum_Topics).filter(Forum_Topics.course_id == course_id).all()
    return topics

@forum_router.get("/replies/{topic_id}", response_model=List[ForumReplyOut])
def get_forum_replies(topic_id: int, db: Session = Depends(get_db)):

    replies = db.query(Forum_Replies).filter(Forum_Replies.topic_id == topic_id).all()
    return replies

@forum_router.put("/update/topic/{topic_id}", response_model=ForumTopicOut)
def update_forum_topic(topic_id: int, topic: ForumTopicUpdate, db: Session = Depends(get_db)):

    topic_to_update = db.query(Forum_Topics).filter(Forum_Topics.topic_id == topic_id).first()
    topic_to_update.course_id = topic.course_id
    topic_to_update.student_id = topic.student_id
    topic_to_update.title = topic.title
    topic_to_update.content = topic.content
    topic_to_update.created_at = topic.created_at
    topic_to_update.is_pinned = topic.is_pinned
    topic_to_update.is_closed = topic.is_closed
    db.commit()
    db.refresh(topic_to_update)
    return topic_to_update

@forum_router.put("/update/reply/{reply_id}", response_model=ForumReplyOut)
def update_forum_reply(reply_id: int, reply: ForumReplyUpdate, db: Session = Depends(get_db)):

    reply_to_update = db.query(Forum_Replies).filter(Forum_Replies.reply_id == reply_id).first()
    reply_to_update.topic_id = reply.topic_id
    reply_to_update.student_id = reply.student_id
    reply_to_update.admin_id = reply.admin_id
    reply_to_update.content = reply.content
    reply_to_update.created_at = reply.created_at
    reply_to_update.upvotes = reply.upvotes
    db.commit()
    db.refresh(reply_to_update)
    return reply_to_update

@forum_router.delete("/delete/topic/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_forum_topic(topic_id: int, db: Session = Depends(get_db)):

    topic_to_delete = db.query(Forum_Topics).filter(Forum_Topics.topic_id == topic_id).first()
    db.delete(topic_to_delete)
    db.commit()
    return {"message": "Topic deleted successfully"}

@forum_router.delete("/delete/reply/{reply_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_forum_reply(reply_id: int, db: Session = Depends(get_db)):

    reply_to_delete = db.query(Forum_Replies).filter(Forum_Replies.reply_id == reply_id).first()
    db.delete(reply_to_delete)
    db.commit()
    return {"message": "Reply deleted successfully"}
