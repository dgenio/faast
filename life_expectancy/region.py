from enum import Enum, auto


class RegionType(Enum):
    COUNTRY = auto()
    REGION = auto()


class Region(Enum):
    PT = (RegionType.COUNTRY, "PT")
    ES = (RegionType.COUNTRY, "ES")
    EU28 = (RegionType.REGION, "EU28")
    EFTA = (RegionType.REGION, "EFTA")

    def __init__(self, region_type, code):
        self.region_type = region_type
        self.code = code

    @classmethod
    def countries(cls):
        return [
            region for region in cls
            if region.region_type == RegionType.COUNTRY
        ]

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other
        return super().__eq__(other)

    def __str__(self):
        return self.code

    @property
    def value(self):
        return self.code
