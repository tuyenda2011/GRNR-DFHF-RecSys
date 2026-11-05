"""Reported models: the three baselines plus GRNR (src.models.grnr) and DFHF (src.models.dfhf).

Earlier research models (RecFlow, SCSR, GRNR ranking tails) were removed; they remain in git history.
"""
from src.models.base import BaseRecommender
from src.models.lightgcn import LightGCN
from src.models.xsimgcl import XSimGCL
from src.models.directau import DirectAU

__all__ = [
    "BaseRecommender",
    "LightGCN",
    "XSimGCL",
    "DirectAU",
]
