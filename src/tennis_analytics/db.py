from sqlalchemy import create_engine, String, Integer, Text, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from .config import DATABASE_URL

class Base(DeclarativeBase): pass

class Category(Base):
    __tablename__ = "categories"
    category_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)

class Competition(Base):
    __tablename__ = "competitions"
    competition_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    competition_name: Mapped[str] = mapped_column(String(150), nullable=False)
    parent_id: Mapped[str | None] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    level: Mapped[str | None] = mapped_column(String(50))
    category_id: Mapped[str | None] = mapped_column(ForeignKey("categories.category_id"))
    raw_json: Mapped[str | None] = mapped_column(Text)

class Complex(Base):
    __tablename__ = "complexes"
    complex_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    complex_name: Mapped[str] = mapped_column(String(150), nullable=False)
    raw_json: Mapped[str | None] = mapped_column(Text)

class Venue(Base):
    __tablename__ = "venues"
    venue_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    venue_name: Mapped[str] = mapped_column(String(150), nullable=False)
    city_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(3))
    timezone: Mapped[str] = mapped_column(String(100), nullable=False)
    complex_id: Mapped[str] = mapped_column(ForeignKey("complexes.complex_id"), nullable=False)
    raw_json: Mapped[str | None] = mapped_column(Text)

class Competitor(Base):
    __tablename__ = "competitors"
    competitor_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(3))
    abbreviation: Mapped[str | None] = mapped_column(String(20))
    raw_json: Mapped[str | None] = mapped_column(Text)

class Ranking(Base):
    __tablename__ = "competitor_rankings"
    rank_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    movement: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    competitions_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    competitor_id: Mapped[str] = mapped_column(ForeignKey("competitors.competitor_id"), nullable=False)
    ranking_type: Mapped[str] = mapped_column(String(30), default="doubles")
    fetched_at: Mapped[str] = mapped_column(String(40), server_default=func.current_timestamp())
    raw_json: Mapped[str | None] = mapped_column(Text)
    __table_args__ = (UniqueConstraint("rank", "competitor_id", "ranking_type"),)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine, expire_on_commit=False)

def init_db():
    Base.metadata.create_all(engine)

def upsert(model, rows, key):
    session = Session()
    try:
        for row in rows:
            obj = session.get(model, row[key])
            if obj is None:
                session.add(model(**row))
            else:
                for field, value in row.items():
                    if field != key: setattr(obj, field, value)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def save_rankings(players, rankings):
    session = Session()
    try:
        for row in players:
            obj = session.get(Competitor, row["competitor_id"])
            if obj is None: session.add(Competitor(**row))
            else:
                for k, v in row.items():
                    if k != "competitor_id": setattr(obj, k, v)
        session.flush()
        session.query(Ranking).delete()
        session.add_all([Ranking(**r) for r in rankings])
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
