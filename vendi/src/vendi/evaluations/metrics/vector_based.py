import numpy as np

from .base import Metric


class CosineSimilarity(Metric):
    @staticmethod
    def __cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    @staticmethod
    def __embed_string(text: str) -> np.ndarray:
        raise NotImplementedError

    def calc_metric(self, a: str, b: str) -> float:
        try:
            from sklearn.metrics.pairwise import cosine_similarity
        except ImportError:
            raise ImportError(
                "Please install scikit-learn to use CosineSimilarityMetric"
            )

        a_embedding = self.__embed_string(a)
        b_embedding = self.__embed_string(b)
        return self.__cosine_similarity(a_embedding, b_embedding)


class JaccardIndex(Metric):
    def calc_metric(self, a: str, b: str):
        raise NotImplementedError
