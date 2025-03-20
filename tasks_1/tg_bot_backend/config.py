from tortoise import Tortoise

TELEGRAM_BOT_TOKEN = "6487693126:AAGw_Fh5_UOfvuopiNUB4NWmo5wZ5h8rbkM"


# async def init_db():
#     await Tortoise.init(
#         db_url="postgres://tg_bot_test_task:password@localhost:1231/test_task_db",
#         modules={"models": ["models"]}
#     )
#     await Tortoise.generate_schemas()