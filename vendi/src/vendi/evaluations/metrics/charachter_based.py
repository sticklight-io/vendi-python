from .base import Metric


class ExactMatch(Metric):
    def calc_metric(self, a: str, b: str):
        if a == b:
            return 1
        return 0


class LevenshteinDistance(Metric):
    def calc_metric(self, a: str, b: str):
        import editdistance
        return editdistance.eval(a, b)
