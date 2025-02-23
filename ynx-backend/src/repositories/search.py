from models.search import *
from utils.repository import SQLAlchemyRepository

class SearchRepository(SQLAlchemyRepository):
    model = [Events, Post, Datasets]
    
