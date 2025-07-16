from fastapi import FastAPI
from controllers import transacao_controller

app = FastAPI()
app.include_router(transacao_controller.router)