from environs import Env
from database.base import get_admin_ids,get_admins_ids

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = [int(x) for x in env.list("ADMINS")]
devv = env.str("dev")
FILMSDATAURL = env.str("FILMSDATAURL")
FILMSDATAID = env.str("FILMSDATAID")
BOTUSERNAME = env.str("BOTUSERNAME")

async def get_admins_ids_from_env():
    admins = await get_admins_ids()  
    if admins:
        return ADMINS + admins
    return ADMINS
