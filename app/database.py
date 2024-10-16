import pymysql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(
    url=settings.CONNECTION_URL,
    echo=False
)

Session: sessionmaker = sessionmaker(bind=engine)


#with Session() as session:
#    print(1)


# def init_db(
#         database_name: str, host: str = settings.host, user: str = settings.user, password: str = settings.password
# ) -> None:
#     try:
#         with pymysql.connect(host=host, user=user, password=password) as conn:
#             cursor = conn.cursor()
#             cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
#             conn.commit()
#     except:
#         print("Failed to initialize database")
#
#
# def downgrade_db(
#         database_name: str, host: str = settings.host, user: str = settings.user, password: str = settings.password
# ) -> None:
#     try:
#         with pymysql.connect(host=host, user=user, password=password) as conn:
#             cursor = conn.cursor()
#             cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
#             conn.commit()
#     except:
#         print("Failed to downgrade database")