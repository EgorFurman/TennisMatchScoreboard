from typing import Optional

from sqlalchemy import select, update, or_
from sqlalchemy.orm import joinedload

from app.database import Session
from app.models import Player, Match


class PlayersRepository:
    @classmethod
    def get(cls, name: str, with_matches: bool = False) -> Optional[Player]:
        with Session() as session:
            stmt = select(Player).where(Player.name == name)

            if with_matches:
                stmt = (
                    stmt.
                    options(
                        joinedload(Player.matches).
                        options(joinedload(Match.player1)).
                        options(joinedload(Match.player2)).
                        options(joinedload(Match.winner))
                    )
                )

            player = session.execute(stmt).scalars().first()

            return player

    @classmethod
    def list(cls) -> list[Player]:
        with Session() as session:
            stmt = select(Player)
            players = session.execute(stmt).scalars().all()
            return players

    @classmethod
    def add(cls, name: str) -> Player:
        with Session() as session:
            player = Player(name=name)
            session.add(player)
            session.commit()
            session.refresh(player)
            return player


class MatchesRepository:
    @classmethod
    def get(cls, uuid: str, with_players: bool = False) -> Optional[Match]:
        with Session() as session:
            stmt = (
                select(Match).
                where(Match.uuid == uuid)
            )

            if with_players:
                stmt = (
                    stmt.
                    options(joinedload(Match.player1)).
                    options(joinedload(Match.player2)).
                    options(joinedload(Match.winner))
                )

            match = session.execute(stmt).scalars().first()
            return match

    @classmethod
    def list(
            cls,
            with_players: bool = False,
            filter_by_player_id: Optional[int] = None,
            filter_by_winner_id: Optional[int] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> list[Match]:

        with Session() as session:
            stmt = select(Match).where(Match.winner_id != None)

            if filter_by_player_id:
                stmt = stmt.where(or_(Match.player1_id == filter_by_player_id, Match.player2_id == filter_by_player_id))

            if filter_by_winner_id:
                stmt = stmt.where(Match.winner_id == filter_by_winner_id)

            if offset is not None:
                stmt = stmt.offset(offset)

            if limit is not None:
                stmt = stmt.limit(limit)

            if with_players:
                stmt = (
                    stmt.
                    options(joinedload(Match.player1)).
                    options(joinedload(Match.player2)).
                    options(joinedload(Match.winner))
                )

            matches = session.execute(stmt).scalars().all()
            return matches

    @classmethod
    def add(cls, first_player_id: int, second_player_id: int, score: dict) -> Match:
        with Session() as session:
            match = Match(
                player1_id=first_player_id,
                player2_id=second_player_id,
                score=score
            )
            session.add(match)
            session.commit()
            session.refresh(match)
            return match

    @classmethod
    def update(cls, uuid: str, **values) -> None:
        with Session() as session:
            stmt = update(Match).where(Match.uuid == uuid).values(**values)
            session.execute(stmt)
            session.commit()

