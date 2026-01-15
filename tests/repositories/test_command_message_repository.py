from repositories.command_message_repository import CommandMessageRepository


class TestCommandMessageRepository:

    async def test_add_new_message_saves_to_database(
            self,
            command_message_repository: CommandMessageRepository
    ):
        """Тест: add_new_message сохраняет сообщение в базу"""
        test_message_id = 99999

        await command_message_repository.add_new_message(test_message_id)

        messages = await command_message_repository.get_all_messages()
        message_ids = [m.message_id for m in messages]

        assert test_message_id in message_ids

    async def test_get_all_messages_returns_empty_list_when_no_messages(
            self,
            command_message_repository: CommandMessageRepository
    ):
        """Тест: get_all_messages возвращает пустой список если нет сообщений"""
        messages = await command_message_repository.get_all_messages()

        assert messages == []

    async def test_get_all_messages_returns_only_current_bot_messages(
            self,
            command_message_repository: CommandMessageRepository
    ):
        """Тест: get_all_messages возвращает только сообщения текущего бота"""
        await command_message_repository.add_new_message(11111)
        await command_message_repository.add_new_message(22222)

        messages = await command_message_repository.get_all_messages()

        assert len(messages) == 2
        message_ids = [m.message_id for m in messages]
        assert 11111 in message_ids
        assert 22222 in message_ids

    async def test_delete_all_messages_removes_all_messages(
            self,
            command_message_repository: CommandMessageRepository
    ):
        """Тест: delete_all_messages удаляет все сообщения"""
        await command_message_repository.add_new_message(11111)
        await command_message_repository.add_new_message(22222)

        await command_message_repository.delete_all_messages()

        messages = await command_message_repository.get_all_messages()
        assert messages == []

    async def test_delete_all_messages_does_not_fail_when_empty(
            self,
            command_message_repository: CommandMessageRepository
    ):
        """Тест: delete_all_messages не падает если нет сообщений"""
        # Не должно вызвать исключение
        await command_message_repository.delete_all_messages()

        messages = await command_message_repository.get_all_messages()
        assert messages == []