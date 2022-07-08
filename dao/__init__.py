from dao.table.scene import *
from dao.table.user import *
from dao.config import engine

base.metadata.create_all(engine)