from vendi_sdk.evaluations.metrics.charachter_based import ExactMatch, LevenshteinDistance
from vendi_sdk.evaluations.metrics.vector_based import CosineSimilarity, JaccardIndex

Metrics = [
    ExactMatch,
    CosineSimilarity,
    LevenshteinDistance,
    JaccardIndex,
]
