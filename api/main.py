from fastapi import FastAPI
from controllers import transacao_controller, saldo_controller
from auth import auth_controller
app = FastAPI()
app.include_router(transacao_controller.router)
app.include_router(auth_controller.router)
app.include_router(saldo_controller.router)