from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

from app.models import Player, Match

if TYPE_CHECKING:
    from app.services import MatchScore


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
    #player1: "PlayersDTO"
    #player2: "PlayersDTO"
    #winner: Optional["PlayersDTO"]


class MatchesWithPlayersDTO(MatchesDTO):
    player1: "PlayersDTO"
    player2: "PlayersDTO"
    winner: Optional["PlayersDTO"]

