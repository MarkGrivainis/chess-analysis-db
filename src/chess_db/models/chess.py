from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://your_user:your_password@localhost:5432/your_database"

Base = declarative_base()


class ChessGameModel(Base):
    __tablename__ = "chess_games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_url = Column(String, unique=True, nullable=False)
    white_player = Column(String, nullable=False)
    black_player = Column(String, nullable=False)
    game_date = Column(String, nullable=True)
    moves = Column(JSONB, nullable=False)  # Stores our validated Pydantic JSON dump


# Setup SQLAlchemy Session
engine_db = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine_db)

# Create table if it doesn't exist
Base.metadata.create_create_all(engine_db)
