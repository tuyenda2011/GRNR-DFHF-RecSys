"""Replay report checkpoints on the validation protocol used by their training runs."""
from pathlib import Path

import numpy as np
import pyarrow  # noqa: F401 -- load Arrow DLLs before Torch on Windows
import torch
from scipy import sparse
from threadpoolctl import threadpool_limits

from scripts.compare_val_runs import per_user_metrics
from scripts.extra.run_item_baselines import ItemScores
from scripts.verify_results import predict
from src.data.quality_report import warm_cohort
from src.data.sparsity import create_sparse_train_set
from src.evaluation.evaluator import Evaluator
from src.evaluation.metrics import compute_topk_metrics
from src.models.gfcf import GFCF
from src.models.grnr import GRNR


def report_device(name):
    if name == "auto":
        name = "cuda" if torch.cuda.is_available() else "cpu"
    return torch.device(name)


def validation_sample(full_train, validation, density):
    train = create_sparse_train_set(full_train, density, 42)
    warm, _ = warm_cohort(train, validation)
    return train, warm


def rescore(model, run, train, full_train, warm, stats, device, *, full_ease_l2=None):
    with threadpool_limits(limits=4), torch.inference_mode():
        if model in ("gfcf", "ease128", "ease"):
            if model == "gfcf":
                score = GFCF.load(run / "checkpoint.npz").get_user_rating_scores
            else:
                x = GRNR.interaction_matrix(train.u_idx.to_numpy(), train.i_idx.to_numpy(),
                                            stats["num_users"], stats["num_items"]).astype(np.float32)
                if model == "ease128":
                    weights = sparse.load_npz(run / "checkpoint.npz")
                else:
                    from scripts.run_ease import ease

                    weights = ease(x, full_ease_l2)
                score = ItemScores(x, weights).get_user_rating_scores
            evaluator = Evaluator(full_train, warm, stats["num_users"], stats["num_items"], [10, 20], 128,
                                  candidate_items=set(train.i_idx.unique()), popularity_df=train, score_fn=score)
            predictions, _ = evaluator.get_predictions(torch.empty(0), torch.empty(0), torch.device("cpu"))
        else:
            evaluator, predictions = predict(model, run, train, full_train, warm, stats, device, 256)
        predictions = predictions.cpu()
        metrics = compute_topk_metrics(evaluator.ground_truth, predictions, [10, 20])
    return np.asarray(evaluator.eval_users, dtype=np.int64), predictions.numpy(), metrics


def saved_predictions(run: Path):
    return tuple(np.load(run / f"val_{name}.npy").astype(np.int64, copy=False) for name in ("users", "predictions"))


def score_rows(users, predictions, targets):
    truth = np.asarray([targets[int(user)] for user in users], dtype=np.int64)
    values = per_user_metrics(predictions, truth)
    values["Recall@10"] = (predictions[:, :10] == truth[:, None]).any(axis=1).astype(float)
    return users, predictions, values, truth
