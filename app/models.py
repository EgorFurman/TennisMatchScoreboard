from uuid import uuid4, UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, JSON


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = 'Player'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)

    matches: Mapped[list["Match"]] = relationship(
        primaryjoin="""and_(or_(Player.id == Match.player1_id, Player.id == Match.player2_id), 
        Match.winner_id != None)"""
    )

    def __repr__(self):
        return f"Player: (id = {self.id}, name = {self.name})"


class Match(Base):
    __tablename__ = 'Match'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(String(36), default=uuid4)
    player1_id: Mapped[int] = mapped_column(ForeignKey("Player.id", ondelete="CASCADE"), nullable=False)
    player2_id: Mapped[int] = mapped_column(ForeignKey("Player.id", ondelete="CASCADE"), nullable=False)
    winner_id: Mapped[int] = mapped_column(ForeignKey("Player.id", ondelete="CASCADE"), nullable=True)
    score: Mapped[JSON] = mapped_column(JSON)

    player1: Mapped["Player"] = relationship(back_populates="matches", foreign_keys="Match.player1_id")
    player2: Mapped["Player"] = relationship(back_populates="matches", foreign_keys="Match.player2_id")
    winner: Mapped["Player"] = relationship(back_populates="matches", foreign_keys="Match.winner_id")

    def __repr__(self):
        return (f"Match: (id = {self.id}, "
                f"uuid = {self.uuid}, "
                f"player1 = {self.player1_id}, "
                f"player2 = {self.player2_id}, "
                f"winner = {self.winner_id}, "
                f"score = {self.score})")




