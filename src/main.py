from Routes import base,data
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores import LLMProviderFactory , VectorDBProviderFactory

app=FastAPI()


async def startup_span():
    settings=get_settings()
    #كده دول هيخشو مع كل راوت و يقدرو يشوفوه
    app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client=app.mongo_conn[settings.MONGODB_DATABASE]

    llm_provider_factory=LLMProviderFactory(settings)
    vector_db_provider_factory=VectorDBProviderFactory(settings)
    #generation client
    app.generation_client=llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    #embedding client
    app.embedding_client=llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(provider=settings.EMBEDDING_MODEL_ID,
                                                     embedding_size=settings.EMBEDDING_MODEL_SIZE)
    #vector db client
    app.vector_db_client=vector_db_provider_factory.create(provider=settings.VECTORDATABASE_BACKEND)
    app.vector_db_client.connect()
async def shutdown_span():
    app.mongo_conn.close()
    app.vector_db_client.disconnect()

app.router.lifespan.on_startup.append(startup_span)
app.router.lifespan.on_shutdown.append(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
