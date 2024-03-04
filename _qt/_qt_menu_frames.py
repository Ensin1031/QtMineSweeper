from typing import Optional

from PyQt5 import QtWidgets, uic, QtCore

from utils import WindowMixin, GameParamsType, GameModeEnum

ParamsFormClass, _ = uic.loadUiType('_qt/_qt_designer/_params_window.ui')
InfoFormClass, _ = uic.loadUiType('_qt/_qt_designer/_info_window.ui')


class InfoQDialogMixin(QtWidgets.QDialog, InfoFormClass, WindowMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


class ParamsQDialog(QtWidgets.QDialog, ParamsFormClass, WindowMixin):
    def __init__(self, parent, game_settings_method):
        super().__init__(parent)
        self.setupUi(self)
        self.__new_settings: Optional[GameParamsType] = None
        self.game_settings_method = game_settings_method

    def start(self):
        self.setWindowTitle("Параметры")

        self.buttonGroup.buttonClicked.connect(lambda x: self.__set_clicked_radiobutton(x))

        self.checkBoxAnimation.clicked.connect(self.__set_clicked_values_settings)
        self.checkBoxSound.clicked.connect(self.__set_clicked_values_settings)
        self.checkBoxHelp.clicked.connect(self.__set_clicked_values_settings)
        self.checkBoxContinueSavedGame.clicked.connect(self.__set_clicked_values_settings)
        self.checkBoxSavedGame.clicked.connect(self.__set_clicked_values_settings)
        self.checkBoxQuestionMarks.clicked.connect(self.__set_clicked_values_settings)
        self.checkBoxIAmWoodpecker.clicked.connect(self.__set_clicked_values_settings)

        self.spinBoxHeight.valueChanged.connect(self.__set_clicked_values_settings)
        self.spinBoxWidth.valueChanged.connect(self.__set_clicked_values_settings)
        self.spinBoxCountMines.valueChanged.connect(self.__set_clicked_values_settings)

        self.exec()

    def __set_clicked_values_settings(self):
        if self.__new_settings is None:
            return
        self.__new_settings = GameParamsType(
            height=self.spinBoxHeight.value(),
            width=self.spinBoxWidth.value(),
            mines_count=self.spinBoxCountMines.value(),
            need_animation=self.checkBoxAnimation.isChecked(),
            need_saved_game=self.checkBoxSavedGame.isChecked(),
            need_question_marks=self.checkBoxQuestionMarks.isChecked(),
            need_help=self.checkBoxHelp.isChecked(),
            need_continue_saved_game=self.checkBoxContinueSavedGame.isChecked(),
            need_sound=self.checkBoxSound.isChecked(),
            i_am_woodpecker=self.checkBoxIAmWoodpecker.isChecked(),
        )

    def reject(self):
        """ Перехватываем и переопределяем событие закрытия окна """
        print('reject')
        return super().reject()

    def accept(self):
        """ Перехватываем и переопределяем событие сохранения новых настроек """
        if self.__new_settings != self.game_settings:
            self.game_settings_method(self.__new_settings)
        super().accept()

    def __get_checked_radiobutton(self, mode: GameModeEnum) -> QtWidgets.QRadioButton:
        if mode == GameModeEnum.NEWBIE.value:
            return self.radioButtonNewbie
        if mode == GameModeEnum.AMATEUR.value:
            return self.radioButtonAmateur
        if mode == GameModeEnum.PROFESSIONAL.value:
            return self.radioButtonProfessional

        return self.radioButtonSpecial

    @property
    def game_settings(self) -> GameParamsType:
        return self._game_settings

    @game_settings.setter
    def game_settings(self, settings: GameParamsType):
        mode = GameModeEnum.get_this_type(params=settings)

        checked_radiobutton = self.__get_checked_radiobutton(mode=mode)
        checked_radiobutton.setChecked(True)

        self.spinBoxHeight.setValue(settings.height)
        self.spinBoxWidth.setValue(settings.width)
        self.spinBoxCountMines.setValue(settings.mines_count)

        self.checkBoxAnimation.setChecked(settings.need_animation)
        self.checkBoxSound.setChecked(settings.need_sound)
        self.checkBoxHelp.setChecked(settings.need_help)
        self.checkBoxContinueSavedGame.setChecked(settings.need_continue_saved_game)
        self.checkBoxSavedGame.setChecked(settings.need_saved_game)
        self.checkBoxQuestionMarks.setChecked(settings.need_question_marks)
        self.checkBoxIAmWoodpecker.setChecked(settings.i_am_woodpecker)
        self._game_settings = settings
        self.__new_settings = settings

        self.__disabled_range_fields(mode=mode)

    def __disabled_range_fields(self, mode: GameModeEnum or int):
        is_disabled = True
        if mode == GameModeEnum.SPECIAL.value:
            is_disabled = False
        self.labelHeight.setDisabled(is_disabled)
        self.spinBoxHeight.setDisabled(is_disabled)
        self.labelWidth.setDisabled(is_disabled)
        self.spinBoxWidth.setDisabled(is_disabled)
        self.labelCountMines.setDisabled(is_disabled)
        self.spinBoxCountMines.setDisabled(is_disabled)

    def __set_clicked_radiobutton(self, clicked_radiobutton: QtWidgets.QRadioButton) -> None:
        mode = clicked_radiobutton.toolTipDuration()
        height = GameModeEnum.get_default_height(mode=mode, default_value=self.__new_settings.height)
        width = GameModeEnum.get_default_width(mode=mode, default_value=self.__new_settings.width)
        mines_count = GameModeEnum.get_default_mines_count(mode=mode, default_value=self.__new_settings.mines_count)
        self.spinBoxHeight.setValue(height)
        self.spinBoxWidth.setValue(width)
        self.spinBoxCountMines.setValue(mines_count)

        self.__disabled_range_fields(mode=mode)

        if self.__new_settings is not None:
            self.__new_settings = GameParamsType(
                height=height,
                width=width,
                mines_count=mines_count,
                need_animation=self.__new_settings.need_animation,
                need_saved_game=self.__new_settings.need_saved_game,
                need_question_marks=self.__new_settings.need_question_marks,
                need_help=self.__new_settings.need_help,
                need_continue_saved_game=self.__new_settings.need_continue_saved_game,
                need_sound=self.__new_settings.need_sound,
                i_am_woodpecker=self.__new_settings.i_am_woodpecker,
            )
        else:
            self.__new_settings = GameParamsType(
                height=height,
                width=width,
                mines_count=mines_count,
                need_animation=self.game_settings.need_animation,
                need_saved_game=self.game_settings.need_saved_game,
                need_question_marks=self.game_settings.need_question_marks,
                need_help=self.game_settings.need_help,
                need_continue_saved_game=self.game_settings.need_continue_saved_game,
                need_sound=self.game_settings.need_sound,
                i_am_woodpecker=self.game_settings.i_am_woodpecker,
            )


class HelpGameQDialog(InfoQDialogMixin):

    def start(self):
        self.setWindowTitle("Справка")
        self.exec()


class AboutGameQDialog(InfoQDialogMixin):

    def start(self):
        self.setWindowTitle("О программе")
        new_text = QtWidgets.QLabel(parent=self.widgetInfo)
        new_text.setText(f"Сюда обычно никто не заглядывает,\n"
                         f"поэтому можно нести всякую хрень!\n\n"
                         f"Эту игру я написал самолично со скуки\n"
                         f"хотелось, знаете-ли нормальный\n"
                         f"Сапер под Линух!\n\n"
                         f"С уважением, Ensin.\n\n"
                         f"Щучу! Без уважения!!\n\n"
                         f"Версия игры {self.program_version}, 2024г.")
        new_text.move(35, 0)
        new_text.setAlignment(QtCore.Qt.AlignCenter)
        self.exec()


class OtherGamesQDialog(InfoQDialogMixin):

    def start(self):
        self.setWindowTitle("Другие игры в Интернете")
        new_text = QtWidgets.QLabel(parent=self.widgetInfo)
        new_text.setText("Вот скажи, дятел, что ты\n"
                         "ожидал тут увидеть?\n\n"
                         "Хочешь других игр,\n"
                         "собака неблагодарная?!\n"
                         "А вот хрен тебе!\n\n"
                         "С уважением, Ensin.\n"
                         "Щучу, щучу! Без уважения!!\n\n")
        new_text.move(75, 0)
        new_text.setAlignment(QtCore.Qt.AlignCenter)
        self.exec()
