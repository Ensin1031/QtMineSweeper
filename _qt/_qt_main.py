import random
import sys
from typing import Tuple, List

from PyQt5 import uic, QtWidgets

from _db import Connection
from _qt._qt_menu_frames import ParamsQDialog
from utils import WindowMixin, GameParamsType, BTN_SIZE, FRAME_MARGIN_SIZE

FormClass, _ = uic.loadUiType('_qt/_qt_designer/_main_window.ui')


class ViewGame(WindowMixin):

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.__db_connector = Connection()
        self.__db_connector.connect()
        self.game_settings = self.set_game_settings(params=self.__db_connector.params)

        self.main_window = MainWindow(db_connector=self.__db_connector)

    def start(self):

        self.main_window.start()
        self.main_window.game_settings = self.game_settings
        self.main_window.program_version = self.program_version

        self.main_window.show()
        sys.exit(self.app.exec_())

    def set_game_settings(self, params: GameParamsType) -> GameParamsType:
        self.window_width = 30 + params.width * BTN_SIZE + 30
        self.window_height = params.height * BTN_SIZE + params.height * 3 + 95 + 10

        return params


class MainWindow(QtWidgets.QMainWindow, FormClass, WindowMixin):

    def __init__(self, db_connector: Connection):
        super().__init__()
        self.__db_connector = db_connector
        self.__bomb_idx: Tuple = ()

    def start(self):
        self.setupUi(self)
        self.pushButton_001.clicked.connect(lambda x: self.__pushButton(self.pushButton_001))

        # установка новых параметров игры
        self.action_01_new_game.triggered.connect(lambda x: self.reboot_game(self.game_settings))
        self.action_03_params.triggered.connect(self.__params_dialog)
        self.action_05_exit.triggered.connect(self.finish)

    def finish(self):
        self.close()

    @property
    def program_version(self) -> str:
        return self._program_version

    @program_version.setter
    def program_version(self, version: str):
        self.setWindowTitle(f'Сапер - v.{version}')
        self._program_version = version

    @property
    def game_settings(self) -> GameParamsType:
        return self._game_settings

    @game_settings.setter
    def game_settings(self, settings: GameParamsType):
        self._game_settings = settings
        bomb_idx_list: List = []
        range_list: List = list(range(settings.mines_count))

        for _ in range_list:
            bomb_id = random.randint(1, settings.width * settings.height)
            if bomb_id not in bomb_idx_list:
                bomb_idx_list.append(bomb_id)
            else:
                range_list.append(0)

        self.__bomb_idx: Tuple = tuple(bomb_idx_list)

        self.setFixedWidth(settings.width * BTN_SIZE + FRAME_MARGIN_SIZE * 2)
        self.setFixedHeight(settings.height * BTN_SIZE + FRAME_MARGIN_SIZE * 6)

    def reboot_game(self, params: GameParamsType):
        self.__db_connector.update_params(params=params)
        self.game_settings = params
        print('params ===', params)

    def __params_dialog(self):
        params_dialog = ParamsQDialog(self, self.reboot_game)
        params_dialog.program_version = self.program_version
        params_dialog.game_settings = self.game_settings
        params_dialog.start()

    def __pushButton(self, pb: QtWidgets.QPushButton):
        print('__pushButton ===', self.game_settings, pb)
        print('__bomb_idx ===', self.__bomb_idx)
        print('action_03_params.__dir__() ===', self.action_03_params.__dir__())
        print('action_03_params.isCheckable() ===', self.action_03_params.isCheckable())
