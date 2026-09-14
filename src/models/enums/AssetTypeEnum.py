
from enum import Enum

class AssetTypeEnum(str, Enum):
    FILE = "file"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"