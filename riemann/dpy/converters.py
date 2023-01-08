from dateutil.relativedelta import relativedelta
from discord.ext.commands import Context, Converter

from ..api.utils import parse_time


class TimeConverter(Converter):
    async def convert(self, ctx: Context, duration: str) -> relativedelta:
        return parse_time(duration)
