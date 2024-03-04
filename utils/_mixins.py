from ._types import GameParamsType


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
