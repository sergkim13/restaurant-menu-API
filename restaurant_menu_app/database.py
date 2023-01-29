from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER  # , DB_SERVICE

# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


# Локальная синхронная база
SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Локальная асинхронная база
# SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# База для контейнеров
# SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_SERVICE}/{DB_NAME}'

# Асинхронная база для контейнеров
# SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_SERVICE}/{DB_NAME}'
Base = declarative_base()

# Синхорнный движок
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Асихнронный движок
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# async_session = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )

# async def get_session():
#     try:
#         session: AsyncSession = async_session()
#         yield session
#     finally:
#         await session.close()
