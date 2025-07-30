from loader import bot

async def check_subscription(
        user_id: int, channel_id: int) -> bool:
    try:
        user = await bot.get_chat_member(
            user_id = user_id,
            chat_id = channel_id
        )
        
        return user.status in (
            "member", "owner", "creator", "administrator")
    except:
        False