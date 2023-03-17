from config import DB_USER, DB_NAME, DB_HOST, DB_PASS, DB_PORT
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
