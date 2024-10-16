import pytest

from app.services import PlayerScore, MatchScore, ScoreboardService


def init_test_match_score(
    first_player_sets, first_player_games, first_player_points,
    second_player_sets, second_player_games, second_player_points
) -> MatchScore:
    return {
        'Player1': PlayerScore(sets=first_player_sets, games=first_player_games, points=first_player_points),
        'Player2': PlayerScore(sets=second_player_sets, games=second_player_games, points=second_player_points),
    }


scoreboard_service = ScoreboardService


class TestScoreboardService:
    @pytest.mark.parametrize(
        'winner_name, score, updated_score',
        [
            (
                'Player1',
                init_test_match_score(
                    0, 1, 40, 0, 2, 30
                ),
                init_test_match_score(
                    0, 2, 0, 0, 2, 0
                ),
            ),
            (
                'Player2',
                init_test_match_score(
                    1, 2, 40, 0, 4, 'AD'
                ),
                init_test_match_score(
                    1, 2, 0, 0, 5, 0
                ),
            ),
            (
                'Player2',
                init_test_match_score(
                    1, 5, 0, 1, 4, 40
                ),
                init_test_match_score(
                    1, 5, 0, 1, 5, 0
                ),
            )
        ]
    )
    def test_update_match_score_win_game(self, winner_name, score, updated_score):
        assert scoreboard_service.update_match_score(score=score, winner_name=winner_name) == updated_score

    @pytest.mark.parametrize(
        'winner_name, score, updated_score',
        [
            (
                    'Player1',
                    init_test_match_score(
                        0, 1, 6, 0, 2, 5
                    ),
                    init_test_match_score(
                        0, 2, 0, 0, 2, 0
                    ),
            ),
            (
                    'Player2',
                    init_test_match_score(
                        1, 2, 4, 0, 4, 6
                    ),
                    init_test_match_score(
                        1, 2, 0, 0, 5, 0
                    ),
            ),
            (
                    'Player2',
                    init_test_match_score(
                        1, 5, 6, 1, 4, 6
                    ),
                    init_test_match_score(
                        1, 5, 0, 1, 5, 0
                    ),
            )
        ]
    )
    def test_update_match_score_tiebreak_win_game(self, winner_name, score, updated_score):
        assert scoreboard_service.update_match_score(score=score, winner_name=winner_name) == updated_score

    @pytest.mark.parametrize(
        'winner_name, score, updated_score',
        [
            (
                'Player1',
                init_test_match_score(
                    0, 5, 40, 1, 2, 15
                ),
                init_test_match_score(
                    1, 0, 0, 1, 0, 0
                )
            ),
            (
                'Player1',
                init_test_match_score(
                    0, 6, 6, 1, 6, 5
                ),
                init_test_match_score(
                    1, 0, 0, 1, 0, 0
                )
            ),
            (
                'Player2',
                init_test_match_score(
                    0, 3, 40, 0, 5, 'AD'
                ),
                init_test_match_score(
                    0, 0, 0, 1, 0, 0
                )
            ),
        ]
    )
    def test_update_match_score_win_set(self, winner_name, score, updated_score):
        assert scoreboard_service.update_match_score(score=score, winner_name=winner_name) == updated_score

    @pytest.mark.parametrize(
        'score',
        [
            init_test_match_score(
                1, 0, 0, 2, 0, 0
            ),
            init_test_match_score(
                2, 0, 0, 0, 0, 0
            ),
            init_test_match_score(
                0, 0, 0, 2, 0, 0
            ),
        ]
    )
    def test_win_match(self, score):
        assert scoreboard_service.is_win(score)

    @pytest.mark.parametrize(
        "winner_score, loser_score, winner_points_res, loser_points_res",
        [
            (PlayerScore(sets=0, games=0, points=0), PlayerScore(sets=0, games=0, points=0), 15, 0),
            (PlayerScore(sets=0, games=0, points=40), PlayerScore(sets=0, games=0, points=0), 0, 0),
            (PlayerScore(sets=0, games=0, points=40), PlayerScore(sets=0, games=0, points=40), 'AD', 40),
            (PlayerScore(sets=0, games=0, points='AD'), PlayerScore(sets=0, games=0, points=40), 0, 0),
            (PlayerScore(sets=0, games=0, points=40), PlayerScore(sets=0, games=0, points='AD'), 40, 40)
        ]
    )
    def test_increment_points(
            self, winner_score: PlayerScore, loser_score: PlayerScore, winner_points_res, loser_points_res
    ):
        winner_score, loser_score = winner_score, loser_score
        scoreboard_service._increment_points(winner_score, loser_score)
        assert winner_score.get('points') == winner_points_res
        assert loser_score.get('points') == loser_points_res






