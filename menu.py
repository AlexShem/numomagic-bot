from aiogram.types import BotCommand

main_menu_commands = [
    BotCommand(command='/start',
               description='Start'),
    BotCommand(command='/analyze',
               description='Energy analysis'),
    BotCommand(command='/help',
               description='Help'),
    BotCommand(command='/support',
               description='Support')
]
