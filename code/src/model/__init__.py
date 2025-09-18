from .User import User, users_router
from .Department import Department, depart_router
from .UsDep import UsDep, usdep_router

from .Article import Article, article_router
from .Tag import Tag, tag_router


from .Section import Section, section_router


from .File import File, file_router

__all__ = [
    'User',
    'users_router'
    'Department',
    'depart_router'
    'UsDep',
    'usdep_router',
    'Article',
    'article_router',
    'Tag',
    'tag_router',
    'Section',
    'section_router'
    'File',
    'file_router'
    ]
