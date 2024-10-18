import random
from random import choice

from app.services import DatabaseService


FILLER_PLAYERS = (
    "EvilArthas",
    "ozon671games",
    "Глеб Биохакер",
    "Райан Гослинг",
    "Мориарти",
    "Нейробиолог Алипов",
    "IT Ментор",
    "Раст Коул",
    "Тайлер Дерден",
    "влад пиво",
    "ivanzolo2004",
    "Дерек Зуландер",
    "SHAMAN",
    "Принцесса Мононоке",
    "Elon Musk",
    "Кен Канеки",
    'Патрик Бэйтмен',
    "СЕРЕГА ПИРАТ",
    "Слава КПСС",
    "Мейби Бейби",
    "INSTASAMKA",
    "uebermarginal",
    "Паша Техник",
    "Тинькофф",
    "Уве Болл",
    "Джейсон Стэйтем"
)


def add_filler_matches(count: int = 300):
    for _ in range(count):
        player1 = choice(FILLER_PLAYERS)

        while True:
            player2 = choice(FILLER_PLAYERS)
            if player1 == player2:
                continue
            break

        match = DatabaseService.add_match(
            player1, player2
        )

        winner = random.choice((player1, player2))

        score = match.score
        score[winner] = {'sets': 2, 'games': 0, 'points': 0}

        DatabaseService.update_match_score_by_uuid(
            uuid=match.uuid,
            score=score
        )

        DatabaseService.update_match_winner_by_uuid(
            uuid=match.uuid,
            winner_name=winner
        )




