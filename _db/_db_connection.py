import sqlite3

from typing import List, Tuple, Optional

from utils import GameParamsType, NEWBIE_HEIGHT, NEWBIE_WIDTH, NEWBIE_MINE_COUNT, USER_NAME


class Connection:

    def __init__(self):
        self.connection = sqlite3.connect('local_minesweeper.db')
        self.cursor = self.connection.cursor()

    def connect(self) -> 'Connection':

        # Таблица параметров. Создаем если отсутствует.
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Params (
        id INTEGER PRIMARY KEY,
        height INTEGER NOT NULL,
        width INTEGER NOT NULL,
        mines_count INTEGER NOT NULL,
        need_animation BOOLEAN NOT NULL DEFAULT FALSE,
        need_sound BOOLEAN NOT NULL DEFAULT FALSE,
        need_help BOOLEAN NOT NULL DEFAULT FALSE,
        need_continue_saved_game BOOLEAN NOT NULL DEFAULT FALSE,
        need_saved_game BOOLEAN NOT NULL DEFAULT FALSE,
        need_question_marks BOOLEAN NOT NULL DEFAULT FALSE,
        i_am_woodpecker BOOLEAN NOT NULL DEFAULT FALSE
        )
        ''')

        # Таблица результатов в режиме "Новичок". Создаем если отсутствует.
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS NewbiesResults (
        id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL DEFAULT '',
        created_at DATETIME TEXT DEFAULT CURRENT_TIMESTAMP,
        seconds INTEGER NOT NULL,
        game_is_win BOOLEAN NOT NULL
        )
        ''')

        # Таблица результатов в режиме "Любитель". Создаем если отсутствует.
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS AmateursResults (
        id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL DEFAULT '',
        created_at DATETIME TEXT DEFAULT CURRENT_TIMESTAMP,
        seconds INTEGER NOT NULL,
        game_is_win BOOLEAN NOT NULL
        )
        ''')

        # Таблица результатов в режиме "Профессионал". Создаем если отсутствует.
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProfessionalsResults (
        id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL DEFAULT '',
        created_at DATETIME TEXT DEFAULT CURRENT_TIMESTAMP,
        seconds INTEGER NOT NULL,
        game_is_win BOOLEAN NOT NULL
        )
        ''')

        # Таблица результатов в режиме "Особый". Создаем если отсутствует.
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS SpecialsResults (
        id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL DEFAULT '',
        created_at DATETIME TEXT DEFAULT CURRENT_TIMESTAMP,
        seconds INTEGER NOT NULL,
        game_is_win BOOLEAN NOT NULL
        )
        ''')

        self.connection.commit()

        return self

    def close(self) -> None:
        self.connection.close()

    @property
    def __params(self) -> Optional[Tuple]:
        self.cursor.execute('''
            SELECT
                height,
                width,
                mines_count,
                need_animation,
                need_sound,
                need_help,
                need_continue_saved_game,
                need_saved_game,
                need_question_marks,
                i_am_woodpecker
            FROM Params
        ''')
        return self.cursor.fetchone()

    @property
    def params(self) -> GameParamsType:
        params = self.__params
        if params is None:
            self.cursor.execute(
                'INSERT INTO Params (height, width, mines_count) VALUES (?, ?, ?)',
                (NEWBIE_HEIGHT, NEWBIE_WIDTH, NEWBIE_MINE_COUNT),
            )
            self.connection.commit()
            params = self.__params
        return GameParamsType(
            height=params[0],
            width=params[1],
            mines_count=params[2],
            need_animation=bool(params[3]),
            need_sound=bool(params[4]),
            need_help=bool(params[5]),
            need_continue_saved_game=bool(params[6]),
            need_saved_game=bool(params[7]),
            need_question_marks=bool(params[8]),
            i_am_woodpecker=bool(params[9]),
        )

    def update_params(self, params: GameParamsType) -> GameParamsType:
        self.cursor.execute(
            'UPDATE Params SET '
            'height = ?, '
            'width = ?, '
            'mines_count = ?, '
            'need_animation = ?, '
            'need_sound = ?, '
            'need_help = ?, '
            'need_continue_saved_game = ?, '
            'need_saved_game = ?, '
            'need_question_marks = ?, '
            'i_am_woodpecker = ?',
            params.params_arr,
        )
        self.connection.commit()

        return self.params

    @property
    def newbies_results(self) -> List[Tuple]:
        self.cursor.execute('SELECT * FROM NewbiesResults')
        return self.cursor.fetchall()

    def add_newbie(self, seconds: int, game_is_win: bool) -> List[Tuple]:
        self.cursor.execute(
            'INSERT INTO NewbiesResults (user_name, seconds, game_is_win) VALUES (?, ?, ?)',
            (USER_NAME, seconds, game_is_win),
        )
        self.connection.commit()
        return self.newbies_results

    @property
    def newbies_wins_count(self) -> int:
        self.cursor.execute('SELECT id FROM NewbiesResults WHERE game_is_win = true')
        return len(self.cursor.fetchall())

    @property
    def newbies_not_wins_count(self) -> int:
        self.cursor.execute('SELECT id FROM NewbiesResults WHERE game_is_win = false')
        return len(self.cursor.fetchall())

    def clear_newbies(self) -> None:
        self.cursor.execute('DELETE FROM NewbiesResults')
        self.connection.commit()

    @property
    def amateurs_results(self) -> List[Tuple]:
        self.cursor.execute('SELECT * FROM AmateursResults')
        return self.cursor.fetchall()

    def add_amateur(self, seconds: int, game_is_win: bool) -> List[Tuple]:
        self.cursor.execute(
            'INSERT INTO AmateursResults (user_name, seconds, game_is_win) VALUES (?, ?, ?)',
            (USER_NAME, seconds, game_is_win),
        )
        self.connection.commit()
        return self.amateurs_results

    @property
    def amateurs_wins_count(self) -> int:
        self.cursor.execute('SELECT id FROM AmateursResults WHERE game_is_win = true')
        return len(self.cursor.fetchall())

    @property
    def amateurs_not_wins_count(self) -> int:
        self.cursor.execute('SELECT id FROM AmateursResults WHERE game_is_win = false')
        return len(self.cursor.fetchall())

    def clear_amateurs(self) -> None:
        self.cursor.execute('DELETE FROM AmateursResults')
        self.connection.commit()

    @property
    def professionals_results(self) -> List[Tuple]:
        self.cursor.execute('SELECT * FROM ProfessionalsResults')
        return self.cursor.fetchall()

    def add_professional(self, seconds: int, game_is_win: bool) -> List[Tuple]:
        self.cursor.execute(
            'INSERT INTO ProfessionalsResults (user_name, seconds, game_is_win) VALUES (?, ?, ?)',
            (USER_NAME, seconds, game_is_win),
        )
        self.connection.commit()
        return self.professionals_results

    @property
    def professionals_wins_count(self) -> int:
        self.cursor.execute('SELECT id FROM ProfessionalsResults WHERE game_is_win = true')
        return len(self.cursor.fetchall())

    @property
    def professionals_not_wins_count(self) -> int:
        self.cursor.execute('SELECT id FROM ProfessionalsResults WHERE game_is_win = false')
        return len(self.cursor.fetchall())

    def clear_professionals(self) -> None:
        self.cursor.execute('DELETE FROM ProfessionalsResults')
        self.connection.commit()

    @property
    def specials_results(self) -> List[Tuple]:
        self.cursor.execute('SELECT * FROM SpecialsResults')
        return self.cursor.fetchall()

    def add_special(self, seconds: int, game_is_win: bool) -> List[Tuple]:
        self.cursor.execute(
            'INSERT INTO SpecialsResults (user_name, seconds, game_is_win) VALUES (?, ?, ?)',
            (USER_NAME, seconds, game_is_win),
        )
        self.connection.commit()
        return self.specials_results

    @property
    def specials_wins_count(self) -> int:
        self.cursor.execute('SELECT id FROM SpecialsResults WHERE game_is_win = true')
        return len(self.cursor.fetchall())

    @property
    def specials_not_wins_count(self) -> int:
        self.cursor.execute('SELECT id FROM SpecialsResults WHERE game_is_win = false')
        return len(self.cursor.fetchall())

    def clear_specials(self) -> None:
        self.cursor.execute('DELETE FROM SpecialsResults')
        self.connection.commit()
