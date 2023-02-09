from enum import Enum
from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message

from helpfuncs.jsonfunctions import JSONHandler


json_handler = JSONHandler()


async def check_permissions(user_id: str, level: int = 1) -> bool:
    rights = await json_handler.get_data()
    if user_id in rights:
        rights = rights[user_id]["rights"]
        return rights >= level
    return False


class Rights(Enum):
    moderator = 1
    supermoderator = 2
    lead = 3
    admin = 4


class CheckRights(ABCRule[Message]):
    def __init__(self, level: int = 1) -> None:
        self.level = level

    async def check(self, event: Message) -> bool:
        rights = await json_handler.get_data()
        if str(event.from_id) in rights:
            rights = rights[str(event.from_id)]["rights"]
            permissions = await check_permissions(str(event.from_id), self.level.value)
            return permissions