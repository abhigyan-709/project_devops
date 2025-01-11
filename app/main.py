from fastapi import FastAPI, Depends
from database.db import db
from routes.user import route2
from routes.utilities import route3

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OpenSource Enterprise Authentication API",
              description="All in ONE advanced Authentication API with User Management.",
              version="1.1.0",
    #           servers=[
    #     {"url": "https://auth.globaltamasha.in", "description": "Staging environment"},
    #     {"url": "https://auth.globaltamasha.com", "description": "Production environment"},
    # ],
    docs_url="/docs",
    contact={
        "name": "Abhigyan Kumar",
        "url": "https://globaltamasha.in/docs",
        "email": "info@globaltamasha.com",

    },
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})


app.openapi_version = "3.0.2"



# Allow all origins for CORS (update this to a specific origin in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(route2)
app.include_router(route3)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
