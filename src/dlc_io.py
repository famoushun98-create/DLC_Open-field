"""
DeepLabCut pose-estimation CSV 입출력 유틸리티
표준 DLC csv는 3줄 헤더(scorer / bodyparts / coords)를 가짐.
"""
import pandas as pd
import numpy as np


def load_dlc_csv(path, likelihood_cutoff=0.9):
    """
    DeepLabCut 표준 csv를 읽어 {bodypart: DataFrame(x, y, likelihood)} 형태로 반환.
    likelihood_cutoff 미만인 좌표는 NaN 처리 후 선형보간.
    """
    raw = pd.read_csv(path, header=[0, 1, 2], index_col=0)
    bodyparts = sorted(set(raw.columns.get_level_values(1)))

    data = {}
    for bp in bodyparts:
        sub = raw.xs(bp, axis=1, level=1)
        sub.columns = sub.columns.get_level_values(1)  # x, y, likelihood
        sub = sub.rename(columns={"x": "x", "y": "y", "likelihood": "likelihood"})
        low_conf = sub["likelihood"] < likelihood_cutoff
        sub.loc[low_conf, ["x", "y"]] = np.nan
        sub[["x", "y"]] = sub[["x", "y"]].interpolate(limit_direction="both")
        data[bp] = sub

    return data, bodyparts


def list_bodyparts(data):
    return list(data.keys())
