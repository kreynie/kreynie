from vkbottle.user import Message, UserLabeler

from helpfuncs.jsonfunctions import DictionaryFuncs, JSONHandler
from helpfuncs.vkfunctions import VKHandler

from .rules import CheckPermissions, Groups, Rights

admin_labeler = UserLabeler()
admin_labeler.vbml_ignore_case = True
admin_labeler.custom_rules["access"] = CheckPermissions
json_handler = JSONHandler()
dict_handler = DictionaryFuncs()


@admin_labeler.private_message(
    access=[Groups.MODERATOR, Rights.ADMIN], text="Права <user_id> <group> <value>"
)
async def change_rights(message: Message, user_id: str, group: str, value: str) -> None:
    if user_id is None:
        await message.answer("Забыл ссылку на страницу!")
        return

    user_info = await VKHandler.get_user_info(user_id)
    if user_info == None:
        await message.answer("Ссылка на страницу должна быть полной и корректной")
        return

    data = json_handler.get_data()
    code, result = await dict_handler.edit_value(data, group, value)
    if code == "not_found":
        await message.answer("Не найден ключ")
    if code == "success":
        json_handler.save_data(result)
        await message.answer("Готово")
