from sqlalchemy import text

from infrastructure.database import Base, session_manager


async def truncate_tables():
    Session = session_manager.get_session()
    async with Session() as session:
        for table_name in Base.metadata.tables:
            query = text(f"""TRUNCATE "{table_name}" CASCADE""")
            await session.execute(query)
        await session.commit()
