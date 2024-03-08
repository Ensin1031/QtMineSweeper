import random
import sys
from itertools import product
from typing import Tuple, List, Optional

from PyQt5 import uic, QtWidgets, QtCore

from _db import Connection
from _qt._qt_menu_frames import ParamsQDialog, HelpGameQDialog, AboutGameQDialog, OtherGamesQDialog
from utils import (
    WindowMixin, GameParamsType, BTN_SIZE, FRAME_MARGIN_SIZE, INFO_FRAME_WIDTH, MineButton, iconFromBase64, SVGImages
)

FormClass, _ = uic.loadUiType('_qt/_qt_designer/_main_window.ui')


class ViewGame(WindowMixin):

    # Stylesheet = '''
    # QWidget {
    #     background-color:rgb(100,200, 255);
    # }
    # QPushButton {
    #     background-color: #D98C00;
    #     min-width:  30px;
    #     max-width:  30px;
    #     min-height: 30px;
    #     max-height: 30px;
    #     border-radius: 2px;        /* круглый */
    #     border: 2px solid #09009B;
    # }
    # QPushButton:hover:pressed {
    #     background-color: red;
    # }
    # QPushButton:hover {
    #     background-color: #0ff;
    #     border: 2px solid #FFA6D5;
    # }
    # '''

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        # self.app.setStyleSheet(self.Stylesheet)
        self.__db_connector = Connection()
        self.__db_connector.connect()
        self.game_settings = self.set_game_settings(params=self.__db_connector.params)

        self.main_window = MainWindow(db_connector=self.__db_connector)

    def start(self):
        self.main_window.game_settings = self.game_settings
        self.main_window.program_version = self.program_version
        self.main_window.start()

        sys.exit(self.app.exec_())

    def set_game_settings(self, params: GameParamsType) -> GameParamsType:
        self.window_width = 30 + params.width * BTN_SIZE + 30
        self.window_height = params.height * BTN_SIZE + params.height * 3 + 95 + 10

        return params


class MainWindow(QtWidgets.QMainWindow, FormClass, WindowMixin):

    def __init__(self, db_connector: Connection):
        super().__init__()
        self.setupUi(self)
        self.__db_connector = db_connector
        self.__bomb_idx: Tuple = ()

        self.__icon_size = QtCore.QSize(25, 25)

        self.__create_main_game_frame()

    def __create_main_game_frame(self):
        self.frameMainGame = QtWidgets.QFrame(parent=self)
        self.frameMainGame.setStyleSheet("background-color: #151a21;")
        self.frameMainGame.setGeometry(FRAME_MARGIN_SIZE, FRAME_MARGIN_SIZE * 2, FRAME_MARGIN_SIZE, FRAME_MARGIN_SIZE)
        self.frameMainGame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frameMainGame.show()

    def start(self):

        self.frameMainGame.setStyleSheet("background-color: #151a21;")

        self.action_01_new_game.triggered.connect(lambda x: self.reboot_game(self.game_settings))
        self.action_02_statistics.triggered.connect(self.__statistics_dialog)
        self.action_03_params.triggered.connect(self.__params_dialog)
        self.action_04_change_design.triggered.connect(self.__change_design_dialog)
        self.action_05_exit.triggered.connect(self.finish)
        self.action_06_view_help.triggered.connect(self.__help_game_dialog)
        self.action_07_about.triggered.connect(self.__about_game_dialog)
        self.action_08_other_games.triggered.connect(self.__other_games_dialog)

        self.show()

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

        window_width = settings.width * BTN_SIZE + FRAME_MARGIN_SIZE * 2
        self.setFixedWidth(window_width)
        self.setFixedHeight(settings.height * BTN_SIZE + FRAME_MARGIN_SIZE * 6)

        self.frameMainGame.setFixedWidth(self.game_settings.width * BTN_SIZE)
        self.frameMainGame.setFixedHeight(self.game_settings.height * BTN_SIZE)

        common_height = self.game_settings.height * BTN_SIZE + FRAME_MARGIN_SIZE * 2
        self.widgetTime.setGeometry(
            FRAME_MARGIN_SIZE, common_height, INFO_FRAME_WIDTH, BTN_SIZE)
        self.pushButtonPlayOrPause.setGeometry(
            window_width / 2 - BTN_SIZE / 2, common_height, BTN_SIZE, BTN_SIZE)
        self.widgetMineCount.setGeometry(
            window_width - FRAME_MARGIN_SIZE - INFO_FRAME_WIDTH, common_height, INFO_FRAME_WIDTH, BTN_SIZE)

        self.__create_mines_buttons(settings=settings)

    def __create_mines_buttons(self, settings: GameParamsType):
        btn_id = 1
        for column_index, row_index in tuple(product(
            range(1, settings.width + 1),
            range(1, settings.height + 1),
        )):
            btn = MineButton(
                parent=self.frameMainGame,
                bt_id=str(btn_id),
                bt_number=btn_id,
                bt_column_index=column_index,
                bt_row_index=row_index,
                left_click_func=self.__mine_left_click_event,
                right_click_func=self.__mine_right_click_event,
                middle_click_func=self.__mine_middle_click_event,
                has_bomb=btn_id in self.__bomb_idx
            )

            btn.setStyleSheet("background-color: #3044b5;")
            btn.setGeometry(BTN_SIZE * (column_index - 1), BTN_SIZE * (row_index - 1), BTN_SIZE, BTN_SIZE)
            btn.show()
            btn_id += 1

        for btn in self.frameMainGame.children():
            if isinstance(btn, MineButton):
                self.__set_mine_button_configurations(btn=btn, settings=settings)

    def __mine_left_click_event(self, btn: MineButton):
        print('__push_left_click ===', btn, btn.has_bomb, btn.bt_id, btn.count_bombs_around)
        if not btn.has_flag:
            btn.setCheckable(True)
            btn.is_empty_pressed = True
            if btn.has_bomb:
                btn.setIcon(iconFromBase64(SVGImages.MINE))
                btn.setIconSize(self.__icon_size)
                self.game_over(fail=True)
            elif btn.count_bombs_around > 0:
                btn.setIcon(btn.number_icon)
                btn.setIconSize(self.__icon_size)
                btn.setStyleSheet('background-color: #bac6dc;')
            else:
                btn.setStyleSheet('background-color: #bac6dc;')
                btn.update_btn_neighbors()

    def __mine_right_click_event(self, btn: MineButton):
        print('__push_right_click ===', btn, btn.has_bomb, btn.bt_id, btn.count_bombs_around)
        btn.setIcon(iconFromBase64(SVGImages.FLAG_RED))
        btn.setIconSize(self.__icon_size)
        btn.has_flag = True
        btn.is_empty_pressed = True
        # TODO завязать на логику подсчета выявленных мин

    def __mine_middle_click_event(self, btn: MineButton):
        # TODO логика открытия соседних кнопок
        print('__push_middle_click ===', btn, btn.has_bomb, btn.bt_id, btn.count_bombs_around)

    def __set_mine_button_configurations(self, btn: MineButton, settings: GameParamsType) -> None:
        """ Установка данных у кнопки игрового поля """
        bt_column_index: int = btn.bt_column_index
        bt_row_index: int = btn.bt_row_index

        bt_top_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index and x.bt_row_index == bt_row_index - 1,
            self.frameMainGame.children()
        )) if bt_row_index > 1 else ()
        btn.bt_top = bt_top_arr[0] if len(bt_top_arr) > 0 else None

        bt_top_right_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index + 1 and x.bt_row_index == bt_row_index - 1,
            self.frameMainGame.children()
        )) if bt_row_index > 1 and bt_column_index < settings.width else ()
        btn.bt_top_right = bt_top_right_arr[0] if len(bt_top_right_arr) > 0 else None

        bt_right_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index + 1 and x.bt_row_index == bt_row_index,
            self.frameMainGame.children()
        )) if bt_column_index < settings.width else ()
        btn.bt_right = bt_right_arr[0] if len(bt_right_arr) > 0 else None

        bt_bottom_right_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index + 1 and x.bt_row_index == bt_row_index + 1,
            self.frameMainGame.children()
        )) if bt_column_index < settings.width and bt_row_index < settings.height else ()
        btn.bt_bottom_right = bt_bottom_right_arr[0] if len(bt_bottom_right_arr) > 0 else None

        bt_bottom_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index and x.bt_row_index == bt_row_index + 1,
            self.frameMainGame.children()
        )) if bt_row_index < settings.height else ()
        btn.bt_bottom = bt_bottom_arr[0] if len(bt_bottom_arr) > 0 else None

        bt_bottom_left_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index - 1 and x.bt_row_index == bt_row_index + 1,
            self.frameMainGame.children()
        )) if bt_row_index < settings.height and bt_column_index > 1 else ()
        btn.bt_bottom_left = bt_bottom_left_arr[0] if len(bt_bottom_left_arr) > 0 else None

        bt_left_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index - 1 and x.bt_row_index == bt_row_index,
            self.frameMainGame.children()
        )) if bt_column_index > 1 else ()
        btn.bt_left = bt_left_arr[0] if len(bt_left_arr) > 0 else None

        bt_top_left_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index - 1 and x.bt_row_index == bt_row_index - 1,
            self.frameMainGame.children()
        )) if bt_column_index > 1 and bt_row_index > 1 else ()
        btn.bt_top_left = bt_top_left_arr[0] if len(bt_top_left_arr) > 0 else None

        btn.count_bombs_around = len(tuple(
            filter(lambda x: x is not None and x.has_bomb, btn.neighbors_collection)
        )) if not btn.has_bomb else 0

    def reboot_game(self, params: GameParamsType):
        self.frameMainGame.deleteLater()
        self.__db_connector.update_params(params=params)
        self.__create_main_game_frame()
        self.game_settings = params
        print('params ===', params)

    def game_over(self, fail: bool = False, btn: Optional[MineButton] = None):
        print('game over')
        # TODO логика завершения игры

    def __params_dialog(self):
        params_dialog = ParamsQDialog(parent=self, game_settings_method=self.reboot_game)
        params_dialog.program_version = self.program_version
        params_dialog.game_settings = self.game_settings
        params_dialog.start()

    def __change_design_dialog(self):
        change_design_dialog = HelpGameQDialog(parent=self)
        change_design_dialog.program_version = self.program_version
        change_design_dialog.game_settings = self.game_settings
        change_design_dialog.start()

    def __statistics_dialog(self):
        statistics_dialog = HelpGameQDialog(parent=self)
        statistics_dialog.program_version = self.program_version
        statistics_dialog.game_settings = self.game_settings
        statistics_dialog.start()

    def __help_game_dialog(self):
        help_dialog = HelpGameQDialog(parent=self)
        help_dialog.program_version = self.program_version
        help_dialog.game_settings = self.game_settings
        help_dialog.start()

    def __about_game_dialog(self):
        about_dialog = AboutGameQDialog(parent=self)
        about_dialog.program_version = self.program_version
        about_dialog.game_settings = self.game_settings
        about_dialog.start()

    def __other_games_dialog(self):
        other_games_dialog = OtherGamesQDialog(parent=self)
        other_games_dialog.program_version = self.program_version
        other_games_dialog.game_settings = self.game_settings
        other_games_dialog.start()

    def __pushButton(self, pb: QtWidgets.QPushButton):
        print('__pushButton ===', self.game_settings, pb)
        print('__bomb_idx ===', self.__bomb_idx)
        print('action_03_params.__dir__() ===', self.action_03_params.__dir__())
        print('action_03_params.isCheckable() ===', self.action_03_params.isCheckable())
