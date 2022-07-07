from DAO.table.scene import *
from DAO.table.user import *
from DAO.config import engine

base.metadata.create_all(engine)