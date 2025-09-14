from neo4j import AsyncGraphDatabase, AsyncSession
from typing import AsyncGenerator

# Local Neo4j Desktop connection config
NEO4J_URI = "//your_neo4j_uri_here//"
NEO4J_USER = "//your_username_here//"
NEO4J_PASSWORD = "//your_password_here//"

# Create driver
driver = AsyncGraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# FastAPI DB session dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with driver.session() as session:
        yield session
