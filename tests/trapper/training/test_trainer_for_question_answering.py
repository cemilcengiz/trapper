import pytest

from trapper.common.params import Params
from trapper.data.dataset_readers import IndexedDataset
from trapper.training import TransformerTrainer
from trapper.training.train import run_experiment_using_trainer


@pytest.fixture(scope="module")
def temp_output_dir(tmpdir_factory):
    return str(tmpdir_factory.mktemp("outputs"))


@pytest.fixture(scope="module")
def temp_result_dir(tmpdir_factory):
    return str(tmpdir_factory.mktemp("results"))


@pytest.fixture(scope="module")
def temp_cache_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("caches")


@pytest.fixture(scope="module")
def train_file_path(fixtures_root):
    return fixtures_root / "training/question_answering/squad/train.json"


@pytest.fixture(scope="module")
def dev_file_path(fixtures_root):
    return fixtures_root / "training/question_answering/squad/dev.json"


@pytest.fixture(scope="module")
def trainer_params(
    temp_output_dir, temp_result_dir, train_file_path, dev_file_path, temp_cache_dir
):
    params_dict = {
        "pretrained_model_name_or_path": "distilbert-base-uncased",
        "train_file_path": train_file_path,
        "dev_file_path": dev_file_path,
        "tokenizer": {"type": "question-answering"},
        "data_collator": {"type": "question-answering"},
        "dataset_reader": {
            "type": "squad-question-answering",
            "apply_cache": True,
            "cache_directory": temp_cache_dir,
        },
        "model": {"type": "question_answering"},
        "args": {
            "type": "default",
            "output_dir": temp_output_dir + "/checkpoints",
            "result_dir": temp_result_dir,
            "num_train_epochs": 3,
            "per_device_train_batch_size": 3,
            "per_device_eval_batch_size": 2,
            "logging_dir": temp_output_dir + "/logs",
            "no_cuda": True,
            "logging_steps": 2,
            "evaluation_strategy": "steps",
            "save_steps": 3,
            "label_names": ["start_positions", "end_positions"],
            "lr_scheduler_type": "linear",
            "warmup_steps": 2,
            "do_train": True,
            "do_eval": True,
            "save_total_limit": 1,
            "metric_for_best_model": "eval_loss",
            "greater_is_better": False,
        },
        "optimizer": {
            "type": "huggingface_adamw",
            "weight_decay": 0.01,
            "parameter_groups": [
                [
                    ["bias", "LayerNorm\\\\.weight", "layer_norm\\\\.weight"],
                    {"weight_decay": 0},
                ]
            ],
            "lr": 5e-5,
            "eps": 1e-8,
        },
    }
    return Params(params_dict)


@pytest.fixture(scope="module")
def trainer(trainer_params) -> TransformerTrainer:
    return TransformerTrainer.from_params(trainer_params)


def test_trainer_fields(trainer):
    assert type(trainer.tokenizer).__name__ == "DistilBertTokenizerFast"
    assert (
        type(trainer.data_collator).__name__ == "DataCollatorForQuestionAnswering"
    )
    assert isinstance(trainer.train_dataset, IndexedDataset)
    assert isinstance(trainer.eval_dataset, IndexedDataset)
    assert type(trainer).__name__ == "TransformerTrainer"
    assert type(trainer.model).__name__ == "DistilBertForQuestionAnswering"
    assert type(trainer.optimizer).__name__ == "HuggingfaceAdamWOptimizer"


def test_trainer_can_train(trainer):
    run_experiment_using_trainer(trainer)