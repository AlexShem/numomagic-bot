from aiogram_dialog import Dialog

from states.state_group import DialogSG
from windows.windows import user_option_window, energy_analysis_window

main_dialog = Dialog(user_option_window, energy_analysis_window)
