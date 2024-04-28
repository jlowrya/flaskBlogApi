from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import func, ForeignKey
from flask_login import current_user


from blog_api.constants import db

class User(db.Model):
   __tablename__="users"

   id: Mapped[int] = mapped_column(primary_key=True)
   username: Mapped[str]
   password: Mapped[str]
   blogs: Mapped[List["BlogPost"]] = relationship(back_populates="author")

   @property
   def is_authenticated(self):
      #TODO: implement method
      return current_user.id==self.id
   
   @property
   def is_active(self):
    #TODO: implement method
      return True
   
   @property
   def is_anonymous(self):
      return not self.is_authenticated
   
   def get_id(self):
      return str(self.id)
   
   


class BlogPost(db.Model):
   __tablename__ = "blog_posts"

   id: Mapped[int] = mapped_column(primary_key=True)
   title: Mapped[str]
   subtitle: Mapped[Optional[str]]
   body: Mapped[str]
   created_at: Mapped[datetime] = mapped_column(server_default=func.now())
   updated_at: Mapped[datetime] = mapped_column(onupdate=lambda : datetime.now(timezone.utc), server_default=func.now())
   author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

   author: Mapped["User"] = relationship(back_populates="blogs")








    
