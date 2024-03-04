import getpass
from enum import IntEnum
from typing import NamedTuple, Tuple

USER_NAME = getpass.getuser()

NEWBIE_HEIGHT = 9
NEWBIE_WIDTH = 9
NEWBIE_MINE_COUNT = 10

AMATEUR_HEIGHT = 16
AMATEUR_WIDTH = 16
AMATEUR_MINE_COUNT = 40

PROFESSIONAL_HEIGHT = 16
PROFESSIONAL_WIDTH = 30
PROFESSIONAL_MINE_COUNT = 99

ACTIVE_BACKGROUND_COLOR = '#CCCCCC'

LABEL_BUTTON_PREFIX = '!labelbutton'

BTN_SIZE = 30
FRAME_MARGIN_SIZE = 20


class GameParamsType(NamedTuple):
    height: int
    width: int
    mines_count: int
    need_animation: bool
    need_sound: bool
    need_help: bool
    need_continue_saved_game: bool
    need_saved_game: bool
    need_question_marks: bool
    i_am_woodpecker: bool

    @property
    def params_arr(self) -> Tuple[int, int, int, bool, bool, bool, bool, bool, bool, bool]:
        return (
            self.height,
            self.width,
            self.mines_count,
            self.need_animation,
            self.need_sound,
            self.need_help,
            self.need_continue_saved_game,
            self.need_saved_game,
            self.need_question_marks,
            self.i_am_woodpecker,
        )


class GameModeEnum(IntEnum):
    NEWBIE = 0
    AMATEUR = 1
    PROFESSIONAL = 2
    SPECIAL = 3

    @classmethod
    def get_this_type(cls, params: GameParamsType):
        if (params.height == NEWBIE_HEIGHT and
                params.width == NEWBIE_WIDTH and
                params.mines_count == NEWBIE_MINE_COUNT):
            return cls.NEWBIE.value
        if (params.height == AMATEUR_HEIGHT and
                params.width == AMATEUR_WIDTH and
                params.mines_count == AMATEUR_MINE_COUNT):
            return cls.AMATEUR.value
        if (params.height == PROFESSIONAL_HEIGHT and
                params.width == PROFESSIONAL_WIDTH and
                params.mines_count == PROFESSIONAL_MINE_COUNT):
            return cls.PROFESSIONAL.value

        return cls.SPECIAL.value

    @classmethod
    def get_default_height(cls, mode: int, default_value: int) -> int:
        if mode == GameModeEnum.NEWBIE.value:
            return NEWBIE_HEIGHT
        if mode == GameModeEnum.AMATEUR.value:
            return AMATEUR_HEIGHT
        if mode == GameModeEnum.PROFESSIONAL.value:
            return PROFESSIONAL_HEIGHT
        return default_value

    @classmethod
    def get_default_width(cls, mode: int, default_value: int) -> int:
        if mode == GameModeEnum.NEWBIE.value:
            return NEWBIE_WIDTH
        if mode == GameModeEnum.AMATEUR.value:
            return AMATEUR_WIDTH
        if mode == GameModeEnum.PROFESSIONAL.value:
            return PROFESSIONAL_WIDTH
        return default_value

    @classmethod
    def get_default_mines_count(cls, mode: int, default_value: int) -> int:
        if mode == GameModeEnum.NEWBIE.value:
            return NEWBIE_MINE_COUNT
        if mode == GameModeEnum.AMATEUR.value:
            return AMATEUR_MINE_COUNT
        if mode == GameModeEnum.PROFESSIONAL.value:
            return PROFESSIONAL_MINE_COUNT
        return default_value
