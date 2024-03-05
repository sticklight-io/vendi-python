from typing import Optional, List

from vendi.core.http_client import HttpClient
from vendi.finetune.schema import TrainData, TrainJob
from vendi.models.schema import ModelInfo, ModelProvider

# TODO
class Finetune:
    def __init__(self, url: str, api_key: str):
        self.__client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix="/v1"
        )

    def run(
        self,
        run_name: str,
        model_name: str,
        model_description: str,
        dataset_id: str,
        model_max_length: Optional[int] = 1024,
        split_eval: Optional[float] = 0.1,
        eval_steps: Optional[int] = 10,
        save_steps: Optional[int] = 50,
        per_device_train_batch_size: Optional[int] = 1,
        per_device_eval_batch_size: Optional[int] = 1,
        num_train_epochs: Optional[int] = 3,
        max_steps: Optional[int] = 50,
        save_total_limit: Optional[int] = 5,
        load_best_model_at_end: Optional[bool] = True,
        learning_rate: Optional[float] = 0.00002,
        gradient_accumulation_steps: Optional[int] = 1,
        warmup_steps: Optional[int] = 0,
        warmup_ratio: Optional[float] = 0.03,
        lora_r: Optional[int] = 32,
        lora_alpha: Optional[int] = 32,
        lora_dropout: Optional[float] = 0.05,
        lora_target_modules=None,
        q_lora: bool = True,
        compute_resource: Optional[str] = None,
    ) -> TrainJob:

        if lora_target_modules is None:
            lora_target_modules = [
                "q_proj",
                "o_proj",
                "up_proj",
                "v_proj",
                "gate_proj",
                "down_proj",
                "k_proj",
                "lm_head"
            ]

        res = self.__client.post(
            uri="/train/train-lora",
            json_data={
                "run_name": run_name,
                "model_name": model_name,
                "model_description": model_description,
                "dataset_id": dataset_id,
                "compute_resource": compute_resource,
                "training_params": {
                    "model_max_length": model_max_length,
                    "split_eval": split_eval,
                    "eval_steps": eval_steps,
                    "save_steps": save_steps,
                    "per_device_train_batch_size": per_device_train_batch_size,
                    "per_device_eval_batch_size": per_device_eval_batch_size,
                    "num_train_epochs": num_train_epochs,
                    "max_steps": max_steps,
                    "save_total_limit": save_total_limit,
                    "load_best_model_at_end": load_best_model_at_end,
                    "learning_rate": learning_rate,
                    "gradient_accumulation_steps": gradient_accumulation_steps,
                    "warmup_steps": warmup_steps,
                    "warmup_ratio": warmup_ratio,
                    "lora_r": lora_r,
                    "lora_alpha": lora_alpha,
                    "lora_dropout": lora_dropout,
                    "lora_target_modules": lora_target_modules,
                    "q_lora": q_lora
                }
            }
        )
        return TrainJob(**res)

    def logs(self, model_id: str) -> TrainData:
        """
        Get the logs for a finetune model by ID
        """
        res = self.__client.get(uri=f"/train/trainings/{model_id}/data")
        return TrainData(**res)

    def available_models(self, provider: ModelProvider = ModelProvider.VENDI) -> List[ModelInfo]:
        res = self.__client.get(uri=f"/providers/{provider}/models")
        return [ModelInfo(**model) for model in res[provider]]
