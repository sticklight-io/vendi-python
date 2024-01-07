from .base import Metric


class ModelJudge(Metric):
    def __init__(self, judge_prompt_template: str):
        self.judge_prompt_template = judge_prompt_template
        super().__init__()

    def calc_metric(self, a: str, b: str):
        raise NotImplementedError
