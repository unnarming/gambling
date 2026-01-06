from typing import Any, Callable
import re
from discord.ext import commands

class Status:
    def __init__(self, status: bool = False, message: str | None = None, body: int | str | dict | list | None = None):
        self.status = status
        self.message = message
        self.body = body

# class to hold the check classes/funcs
class Check:
    class StatusCheck:
        def __init__(self, status: bool = False, success_message: str | None = None, fail_message: str | None = None, body: int | str | dict | None = None):
            self.status = status
            self.success_message = success_message
            self.fail_message = fail_message
            self.body = body

        def to_status(self) -> Status:
            return Status(status=self.status, message=self.success_message if self.status else self.fail_message, body=self.body)

    # coinflip status checks
    USER_SAME_ID = StatusCheck(fail_message="You can't challenge yourself silly")
    USER_BAL_SELF = StatusCheck(fail_message="You don't have enough money for that")
    USER_BAL_OTHER = StatusCheck(fail_message="Other user's balance is insufficient")
    CF_EXISTS = StatusCheck(fail_message="You've already challenged that user")
    CF_NOT_EXISTS = StatusCheck(fail_message="Coinflip doesn't exist")
    CF_REQUEST_DNE= StatusCheck(fail_message="Request from that user doesn't exist")
    CF_REQUEST_NOT_YOURS = StatusCheck(fail_message="That request is not yours")

    BOT_CHANNEL = StatusCheck(fail_message="You can't use this command in this channel")

    class FuncCheck:
        def __init__(self, func: Callable, params: list[Any]):
            self.func = func
            self.params = params

        def __call__(self, *args) -> Any:
            res: Any = self.func(self.params, *args)
            return res

    def __init__(func_to_check: Callable, params: list[Any], check_lambda: Callable[[Any], bool], attr: str | None = None, StatusCheck: StatusCheck | None = None, FuncCheck: FuncCheck | None = None) -> Status:
        res: Any = func_to_check(*params)
        if attr:
            res = getattr(res, attr)
        if check_lambda(res):
            if StatusCheck:
                return Status(status=True, message=StatusCheck.success_message, body=res)
            elif FuncCheck:
                return FuncCheck.__call__(res)
        return Status(status=False, message=StatusCheck.fail_message)

class Int():
    class Any(commands.Converter[int]):
        async def convert(self, ctx: commands.Context, argument: str) -> int:
            match = re.search(r'-?\d+', argument)
            if not match:
                raise commands.BadArgument(f'Could not extract a valid amount from "{argument}"')
            return int(match.group())
    
    class Pos(commands.Converter[int]):
        async def convert(self, ctx: commands.Context, argument: str) -> int:
            match = re.search(r'\d+', argument)
            if not match:
                raise commands.BadArgument(f'Could not extract a valid amount from "{argument}"')
            return int(abs(int(match.group())))
    
    class Neg(commands.Converter[int]):
        async def convert(self, ctx: commands.Context, argument: str) -> int:
            match = re.search(r'-?\d+', argument)
            if not match:
                raise commands.BadArgument(f'Could not extract a valid amount from "{argument}"')
            return int(-abs(int(match.group())))
