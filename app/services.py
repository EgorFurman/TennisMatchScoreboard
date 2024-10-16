import re
from typing import TypedDict, TypeAlias, Optional

from app.models import Player, Match
from app.schemas import PlayersDTO, MatchesDTO, MatchesWithPlayersDTO
from app.repositories import PlayersRepository, MatchesRepository
from app.exceptions import (
    MatchNotFoundError, InvalidUsernameError, UpdateMatchScoreForFinishedMatchError
)


class PlayerScore(TypedDict):
    sets: int
    games: int
    points: int | str


MatchScore: TypeAlias = dict[str, PlayerScore]


class ScoreboardService:
    POINTS = [0, 15, 30, 40]
    GAME_WIN_THRESHOLD = 6  # Игрок должен выиграть не менее 6 игр, чтобы выиграть сет
    TIEBREAK_THRESHOLD = 7  # Тай-брейк играется до 7 очков
    SET_WIN_THRESHOLD = 2  # Игрок должен выиграть 2 сета, чтобы победить в матче

    @classmethod
    def update_match_score(cls, score: MatchScore, winner_name: str):
        cls._check_match_finished(score)

        winner_score = score[winner_name]

        # Определяем имя проигравшего игрока
        loser_name = next(player for player in score if player != winner_name)
        loser_score = score[loser_name]

        # Определяем режим тай-брейка
        is_tiebreak = winner_score['games'] == 6 and loser_score['games'] == 6

        # Обновляем очки
        if is_tiebreak:
            winner_score['points'] += 1
            if winner_score['points'] == cls.TIEBREAK_THRESHOLD:
                cls._win_game(winner_score, loser_score, is_tiebreak)
        else:
            cls._increment_points(winner_score, loser_score)

        # Проверка завершения игры
        if not is_tiebreak and winner_score['games'] >= cls.GAME_WIN_THRESHOLD and (
                winner_score['games'] - loser_score['games']) >= 2:
            cls._win_game(winner_score, loser_score)

        # # Проверка завершения матча
        # if winner_score['sets'] == cls.SET_WIN_THRESHOLD:
        #     is_win = True

        return score

    @classmethod
    def _increment_points(cls, winner_score: PlayerScore, loser_score: PlayerScore):
        """Обновляет очки игрока и проверяет победу в игре."""
        current_winner_points = winner_score['points']
        current_loser_points = loser_score['points']

        if current_winner_points in cls.POINTS and current_winner_points < 40:
            winner_score['points'] = cls.POINTS[cls.POINTS.index(current_winner_points) + 1]
        else:
            if current_winner_points == 40:
                if current_loser_points == 40:
                    winner_score['points'] = "AD"
                elif current_loser_points == "AD":
                    loser_score['points'] = 40
                else:
                    cls._win_game(winner_score, loser_score)
            else:
                if current_loser_points == "AD":
                    loser_score['points'] = 40
                else:
                    cls._win_game(winner_score, loser_score)

    @classmethod
    def _win_game(cls, winner_score: PlayerScore, loser_score: PlayerScore, tiebreak: bool = False):
        """Обрабатывает победу в гейме и сбрасывает очки."""
        winner_score['games'] += 1
        winner_score['points'] = 0
        loser_score['points'] = 0

        # Переход к следующему сету, если достигнут порог геймов

        if tiebreak and winner_score['games'] >= cls.GAME_WIN_THRESHOLD:
            cls._win_set(winner_score, loser_score)

        if winner_score['games'] >= cls.GAME_WIN_THRESHOLD and (
                winner_score['games'] - loser_score['games']) >= 2:
            cls._win_set(winner_score, loser_score)

    @classmethod
    def _win_set(cls, winner_score: PlayerScore, loser_score: PlayerScore):
        """Обрабатывает победу в сете и сбрасывает геймы."""
        winner_score['sets'] += 1
        winner_score['games'] = 0
        loser_score['games'] = 0

    @classmethod
    def _check_match_finished(cls, score: MatchScore) -> None:
        if cls.is_win(score):
            raise UpdateMatchScoreForFinishedMatchError

    @classmethod
    def is_win(cls, score: MatchScore) -> bool:
        return any(player_score['sets'] == cls.SET_WIN_THRESHOLD for player_score in score.values())


class MatchesCacheService:
    _cache: dict = {}
    _MATCHES_PER_PAGE = 10

    @classmethod
    def get_cached_data(cls, player_name: Optional[str] = None):
        key = player_name if player_name else "all_matches"
        return cls._cache.get(key)

    @classmethod
    def cache_data(cls, player_name: Optional[str], total_pages: int):
        key = player_name if player_name else "all_matches"
        cls._cache[key] = total_pages

    @classmethod
    def invalidate_cache(cls):
        cls._cache = {}

    @classmethod
    def calculate_total_pages(cls, total_matches: int) -> int:
        total_pages = (total_matches // cls._MATCHES_PER_PAGE) + (1 if total_matches % cls._MATCHES_PER_PAGE != 0 else 0)

        if total_pages == 0:
            return 1
        return total_pages


class DatabaseService:
    @classmethod
    def add_match(cls, first_player_name: str, second_player_name: str) -> "MatchesDTO":
        cls._verify_player_name(first_player_name)
        cls._verify_player_name(second_player_name)

        first_player = PlayersRepository.get(name=first_player_name)
        second_player = PlayersRepository.get(name=second_player_name)

        if first_player is None:
            first_player = PlayersRepository.add(name=first_player_name)

        if second_player is None:
            second_player = PlayersRepository.add(name=second_player_name)

        match = MatchesRepository.add(
            first_player_id=first_player.id,
            second_player_id=second_player.id,
            score=cls._init_score(first_player_name, second_player_name)
        )

        return MatchesDTO.model_validate(match, from_attributes=True)

    @classmethod
    def get_match_by_uuid(cls, uuid: str) -> "MatchesDTO":
        match = MatchesRepository.get(uuid=uuid)

        cls._verify_match_exists(
            uuid=uuid,
            match=match
        )

        return MatchesDTO.model_validate(match, from_attributes=True)

    @classmethod
    def get_match_by_uuid_with_players(cls, uuid: str) -> "MatchesWithPlayersDTO":
        match = MatchesRepository.get(uuid=uuid, with_players=True)

        cls._verify_match_exists(
            uuid=uuid,
            match=match
        )

        return MatchesWithPlayersDTO.model_validate(match, from_attributes=True)

    @classmethod
    def get_matches_list(
            cls,
            filter_by_player_name: Optional[str] = None,
            filter_by_winner_name: Optional[str] = None,
            offset: Optional[int] = None,
            count: Optional[int] = None
    ) -> list["MatchesWithPlayersDTO"]:

        player_id = None
        winner_id = None

        if filter_by_player_name:
            player_id = PlayersRepository.get(filter_by_player_name).id

        if filter_by_winner_name:
            winner_id = PlayersRepository.get(filter_by_winner_name).id

        matches = MatchesRepository.list(
            with_players=True,
            filter_by_player_id=player_id,
            filter_by_winner_id=winner_id,
            offset=offset,
            limit=count
        )

        return [MatchesWithPlayersDTO.model_validate(match, from_attributes=True) for match in matches]

    @classmethod
    def get_players_list(cls) -> list["PlayersDTO"]:
        return [PlayersDTO.model_validate(player, from_attributes=True) for player in PlayersRepository.list()]

    @classmethod
    def update_match_score_by_uuid(cls, uuid: str, winner_name: str):
        match = MatchesRepository.get(uuid=uuid, with_players=True)

        cls._verify_match_exists(
            uuid=uuid,
            match=match
        )

        score = ScoreboardService.update_match_score(score=match.score, winner_name=winner_name)

        if ScoreboardService.is_win(score):
            MatchesRepository.update(
                uuid=uuid,
                score=score,
                winner_id=match.player1.id if match.player1.name == winner_name else match.player2.id
            )
        else:
            MatchesRepository.update(
                uuid=uuid,
                score=score,
            )

    @staticmethod
    def _init_score(first_player_name: str, second_player_name: str) -> MatchScore:
        score: MatchScore = {
            first_player_name: PlayerScore(sets=0, games=0, points=0),
            second_player_name: PlayerScore(sets=0, games=0, points=0)
        }

        return score

    @staticmethod
    def _verify_player_name(name: str):
        if len(name) < 2 or len(name) > 20 or not re.match(r'^[\w\s]+$', name):
            raise InvalidUsernameError(name)

    @staticmethod
    def _verify_match_exists(uuid: str, match: Optional["Match"]) -> None:
        if match is None:
            raise MatchNotFoundError(uuid=uuid)

