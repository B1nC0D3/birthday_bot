from discord.ext.commands.context import Context
from discord.errors import HTTPException
from discord.member import Member


async def validate_discord_user(context: Context, raw_user_id: str) -> Member | None:
    if raw_user_id is None or len(raw_user_id) < 3:
        return None
    try:
        user_id = int(raw_user_id[2:-1])
    except ValueError:
        return None
    try:
        user = await context.guild.fetch_member(user_id)
    except HTTPException as e:
        print(e)
        return None
    return user
