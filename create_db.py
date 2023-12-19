from src.finances.database import engine
from src.finances.tables import Base

Base.metadata.create_all(engine)
