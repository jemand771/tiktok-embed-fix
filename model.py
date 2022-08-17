import json
from dataclasses import asdict, dataclass
from datetime import datetime


def serializer(obj):
    if isinstance(obj, datetime):
        return (obj - datetime(1970, 1, 1)).total_seconds()
    raise TypeError(f"object of type {type(obj)} not serializable")


@dataclass
class Video:
    title: str
    author: str
    url: str
    width: int
    height: int
    last_update: datetime = None

    def __post_init__(self):
        if self.last_update is None:
            self.last_update = datetime.utcnow()

    @classmethod
    def from_json(cls, data):
        # this doesn't work for nested data, but luckily I don't have nested data
        dict_ = json.loads(data)
        dict_["last_update"] = datetime.utcfromtimestamp(dict_["last_update"])
        return cls(**dict_)

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False, default=serializer)
