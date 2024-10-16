from typing import Optional

from pydantic import BaseModel


class PlayersDTO(BaseModel):
    id: int
    name: str


class PlayersWithMatchesDTO(PlayersDTO):
    matches: list["MatchesDTO"]


class MatchesDTO(BaseModel):
    id: int
    uuid: str
    player1_id: int
    player2_id: int
    winner_id: Optional[int]
    score: dict


class MatchesWithPlayersDTO(MatchesDTO):
    player1: "PlayersDTO"
    player2: "PlayersDTO"
    winner: Optional["PlayersDTO"]

