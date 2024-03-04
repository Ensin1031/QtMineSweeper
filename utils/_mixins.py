from base64 import b64encode
from typing import Optional, Tuple

from PyQt5 import QtWidgets, QtCore, Qt, QtGui

from ._svg_images import SVGImages
from ._types import GameParamsType


def iconFromBase64(base_64: str) -> QtGui.QIcon:
    svg_base64_str = b64encode(base_64.encode('utf-8'))
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(svg_base64_str), "SVG")
    return QtGui.QIcon(pixmap)


class WindowMixin:
    _program_version: str = ''
    _width = 400
    _height = 300
    _game_settings: GameParamsType = GameParamsType(
        height=16,
        width=30,
        mines_count=99,
        need_animation=False,
        need_sound=False,
        need_help=False,
        need_continue_saved_game=False,
        need_saved_game=False,
        need_question_marks=False,
        i_am_woodpecker=False,
    )
    _title: str = 'Сапер'

    def start(self) -> None:
        raise NotImplementedError

    @property
    def window_width(self) -> int:
        return self._width

    @window_width.setter
    def window_width(self, width: int):
        self._width = width

    @property
    def window_height(self) -> int:
        return self._height

    @window_height.setter
    def window_height(self, height: int):
        self._height = height

    @property
    def window_title(self) -> str:
        return self._title

    @window_title.setter
    def window_title(self, title: str):
        self._title = title

    @property
    def program_version(self) -> str:
        return self._program_version

    @program_version.setter
    def program_version(self, version: str):
        self._program_version = version

    @property
    def game_settings(self) -> GameParamsType:
        return self._game_settings

    @game_settings.setter
    def game_settings(self, settings: GameParamsType):
        self._game_settings = settings


class MineButton(QtWidgets.QPushButton):

    left_click = QtCore.pyqtSignal()
    right_click = QtCore.pyqtSignal()
    middle_click = QtCore.pyqtSignal()

    def __init__(
            self,
            parent: QtWidgets.QFrame,
            bt_id: str,
            bt_number: int,
            bt_column_index: int,
            bt_row_index: int,
            left_click_func,  # функция, которая должна отработать при нажатии на левую кнопку мыши
            right_click_func,  # функция, которая должна отработать при нажатии на правую кнопку мыши
            middle_click_func,  # функция, которая должна отработать при нажатии на среднюю кнопку мыши
            bt_top: Optional['MineButton'] = None,
            bt_top_right: Optional['MineButton'] = None,
            bt_right: Optional['MineButton'] = None,
            bt_bottom_right: Optional['MineButton'] = None,
            bt_bottom: Optional['MineButton'] = None,
            bt_bottom_left: Optional['MineButton'] = None,
            bt_left: Optional['MineButton'] = None,
            bt_top_left: Optional['MineButton'] = None,
            has_bomb: bool = False,  # есть ли бомба на кнопке
            has_flag: bool = False,  # установлен ли флаг на кнопке (блокировка)
            is_empty_pressed: bool = False,  # кнопка без бомбы нажата
            count_bombs_around: int = 0,  # число бомб вокруг.
    ):

        self.bt_id: str = bt_id
        self.bt_number: int = bt_number
        self.bt_column_index: int = bt_column_index
        self.bt_row_index: int = bt_row_index
        self.bt_top: Optional['MineButton'] = bt_top
        self.bt_top_right: Optional['MineButton'] = bt_top_right
        self.bt_right: Optional['MineButton'] = bt_right
        self.bt_bottom_right: Optional['MineButton'] = bt_bottom_right
        self.bt_bottom: Optional['MineButton'] = bt_bottom
        self.bt_bottom_left: Optional['MineButton'] = bt_bottom_left
        self.bt_left: Optional['MineButton'] = bt_left
        self.bt_top_left: Optional['MineButton'] = bt_top_left
        self.has_bomb: bool = has_bomb
        self.has_flag: bool = has_flag
        self.is_empty_pressed: bool = is_empty_pressed
        self.count_bombs_around: int = count_bombs_around

        super().__init__(parent)

        self.left_click.connect(lambda: left_click_func(btn=self))
        self.right_click.connect(lambda: right_click_func(btn=self))
        self.middle_click.connect(lambda: middle_click_func(btn=self))

    def mousePressEvent(self, event):
        if self.is_empty_pressed:
            return
        if event.button() == Qt.Qt.LeftButton:
            self.left_click.emit()
        elif event.button() == Qt.Qt.RightButton:
            self.right_click.emit()
        elif event.button() == Qt.Qt.MidButton:
            self.middle_click.emit()
        super().mousePressEvent(event)

    @property
    def neighbors_collection(self) -> Tuple[
        Optional['MineButton'], Optional['MineButton'], Optional['MineButton'], Optional['MineButton'],
        Optional['MineButton'], Optional['MineButton'], Optional['MineButton'], Optional['MineButton'],
    ]:
        return (
            self.bt_top,
            self.bt_top_right,
            self.bt_right,
            self.bt_bottom_right,
            self.bt_bottom,
            self.bt_bottom_left,
            self.bt_left,
            self.bt_top_left,
        )

    @property
    def number_icon(self) -> QtGui.QIcon:
        if self.has_bomb or self.has_flag or self.count_bombs_around == 0:
            return QtGui.QIcon('')
        return iconFromBase64(SVGImages().get_number_icon(value=str(self.count_bombs_around)))

    def update_btn_neighbors(self):
        self.setStyleSheet('background-color: #bac6dc;')
        self.is_empty_pressed = True
        # TODO логика рекурсивного обхода соседних кнопок
