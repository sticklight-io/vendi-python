from vendi.evaluations.metrics.charachter_based import ExactMatch, LevenshteinDistance
from vendi.evaluations.metrics.vector_based import CosineSimilarity, JaccardIndex

Metrics = [
    ExactMatch,
    CosineSimilarity,
    LevenshteinDistance,
    JaccardIndex,
]
