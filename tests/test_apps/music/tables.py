from __future__ import annotations
from enum import Enum

from piccolo.columns import (
    JSON,
    JSONB,
    BigInt,
    ForeignKey,
    Integer,
    Numeric,
    Serial,
    Text,
    Varchar,
)
from piccolo.columns.readable import Readable
from piccolo.engine.finder import engine_finder
from piccolo.table import Table


engine = engine_finder()
###############################################################################
# Simple example


class Manager(Table):
    id: Serial
    name = Varchar(length=50)

    @classmethod
    def get_readable(cls: type[Manager]) -> Readable:
        return Readable(template="%s", columns=[cls.name])


class Band(Table):
    id: Serial
    name = Varchar(length=50)
    manager = ForeignKey(Manager, null=True)
    popularity = BigInt(default=0)

    @classmethod
    def get_readable(cls: type[Band]) -> Readable:
        return Readable(template="%s", columns=[cls.name])


###############################################################################
# More complex


class Venue(Table):
    id: Serial
    name = Varchar(length=100)
    capacity = Integer(default=0, secret=True)

    @classmethod
    def get_readable(cls: type[Venue]) -> Readable:
        return Readable(template="%s", columns=[cls.name])


class Concert(Table):
    id: Serial
    band_1 = ForeignKey(Band)
    band_2 = ForeignKey(Band)
    venue = ForeignKey(Venue)

    @classmethod
    def get_readable(cls: type[Concert]) -> Readable:
        return Readable(
            template="%s and %s at %s, capacity %s",
            columns=[
                cls.band_1.name,
                cls.band_2.name,
                cls.venue.name,
                cls.venue.capacity,
            ],
        )


class Ticket(Table):
    id: Serial
    concert = ForeignKey(Concert)
    price = Numeric(digits=(5, 2))


class Poster(Table, tags=["special"]):  # type: ignore[call-arg]
    """Has tags for tests which need it."""

    id: Serial
    content = Text()


class Shirt(Table):
    """Used for testing columns with a choices attribute."""

    class Size(str, Enum):
        small = "s"
        medium = "m"
        large = "l"

    id: Serial
    size = Varchar(length=1, choices=Size, default=Size.large)


class RecordingStudio(Table):
    """Used for testing JSON and JSONB columns."""

    id: Serial
    facilities = JSON()
    facilities_b = JSONB()


class Instrument(Table):
    """Used for testing foreign keys to a table with a JSON column."""

    id: Serial
    name = Varchar()
    recording_studio = ForeignKey(RecordingStudio)
