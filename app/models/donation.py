from sqlalchemy import Column, ForeignKey, Text, Integer

from app.core.db import Base, CommonFields


class Donation(Base, CommonFields):

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
