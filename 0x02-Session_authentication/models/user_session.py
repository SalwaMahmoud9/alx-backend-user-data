#!/usr/bin/env python3
""" user_session
"""
from models.base import Base
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid


class UserSession(Base):
    """ UserSession """
    def __init__(self, *args: list, **kwargs: dict):
        """ init """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
