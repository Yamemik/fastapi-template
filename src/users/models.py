# from fastapi_users.db import SQLAlchemyBaseUserTableUUID
# from sqladmin import ModelView




class UsersAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-sharp fa-solid fa-user"
    column_list = "__all__"