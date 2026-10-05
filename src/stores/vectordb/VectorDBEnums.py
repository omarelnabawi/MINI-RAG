from enum import Enum

class VectorDBType(Enum):
    QDRANT = "QDRANT"
    CHROMA = "CHROMA"

class DistanceMethodEnum(Enum):
    COSINE = "cosine"
    DOT = "dot"