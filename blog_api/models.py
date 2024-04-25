from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import func


from blog_api.constants import db

class BlogPost(db.Model):
   __tablename__ = "blog_post"

   id: Mapped[int] = mapped_column(primary_key=True)
   title: Mapped[str]
   subtitle: Mapped[Optional[str]]
   body: Mapped[str]
   created_at: Mapped[datetime] = mapped_column(server_default=func.now())
   updated_at: Mapped[datetime] = mapped_column(onupdate=lambda : datetime.now(timezone.utc), server_default=func.now())





    
