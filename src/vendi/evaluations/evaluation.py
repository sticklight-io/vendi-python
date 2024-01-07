import inspect
import json
from typing import Callable

import pandas as pd

from vendi.core.http_client import HttpClient
from vendi.deployments.schema import Deployment
from vendi.evaluations.metrics import Metrics


class EvaluationCase:
    def __init__(
        self,
        name: str,
        type_: str,
        preprocess_callback: Callable[[dict], str],
        deployment: dict,
        eval_metric: list[Metrics],
    ):
        self.name = name
        self.type_ = type_
        self.preprocess_callback = preprocess_callback
        self.deployment = deployment
        self.eval_metrics = eval_metric

    def run_prediction(self, index: int, input: str, url: str, api_key) -> str:
        print(f"Running prediction {index}")
        deployment = Deployment(
            name=self.deployment['model'],
            provider=self.deployment['provider'],
            url=url,
            api_key=api_key,
        )
        res = deployment.predict(input)
        return res

    def run_case(self, df: pd.DataFrame, output_column: str, url: str, api_key: str):
        df['__preprocessed'] = df.apply(lambda row: self.preprocess_callback(row), axis=1)
        df['__prediction'] = df.apply(lambda row: self.run_prediction(row.index, row["__preprocessed"], url, api_key),
                                      axis=1)

        for eval_metric in self.eval_metrics:
            df[f"{self.name}-{eval_metric.name}"] = df.apply(
                lambda row: eval_metric.calc_metric(
                    json.dumps(row["__prediction"]),
                    json.dumps(row[output_column])
                ),
                axis=1
            )

        return df

    def to_dict(self):
        return {
            "name": self.name,
            "type_": self.type_,
            "preprocess_callback": inspect.getsource(self.preprocess_callback),
            "model_server": self.deployment,
            "eval_metric": str([metric.name for metric in self.eval_metrics]),
        }


class Evaluations:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.__api_key = api_key

        self.__client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/api/v1/evaluations"
        )

    def register_eval(
        self,
        name: str,
        dataset_name: str,
        cases: list[EvaluationCase],
        results_dataset: list[dict],
    ):
        self.__client.post(
            uri=f"/register",
            json_data={
                "name": name,
                "dataset": dataset_name,
                "cases": [
                    case.to_dict() for case in cases
                ],
                "results_dataset": results_dataset,
            }
        )

    def run_evaluation(
        self,
        name: str,
        dataset: pd.DataFrame,
        output_column: str,
        cases: list[EvaluationCase],
    ) -> pd.DataFrame:
        for case in cases:
            print(f"Running case: {name}")
            dataset = case.run_case(dataset, output_column, self.url, self.__api_key)

        self.register_eval(
            name=name,
            dataset_name=name,
            cases=cases,
            results_dataset=dataset.to_dict("records"),
        )

        return dataset
