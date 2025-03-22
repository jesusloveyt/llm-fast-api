from fastapi import FastAPI

from views.account import router as account_router
from views.code import router as code_router
from views.file import router as file_router
from views.notice import router as notice_router


from middlewares import cors_config
from middlewares import static_config


app = FastAPI()

cors_config.add(app)
static_config.add(app)

app.include_router(account_router)
app.include_router(code_router)
app.include_router(file_router)
app.include_router(notice_router)
