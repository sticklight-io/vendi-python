class Metric:
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__

    def calc_metric(self, a: str, b: str) -> float:
        raise NotImplementedError
