"""
DLCAnalyzer(R, ETHZ-INS)의 AddOFTZones() 로직을 Python으로 재구현.
네 모서리(top-left, top-right, bottom-right, bottom-left) bodypart 좌표의
중앙값으로 arena를 보정(calibrate)하고, arena 중심을 기준으로
center / periphery(edge) / corner 영역을 정의한다.

기본값은 원 저자 패키지와 동일:
    scale_center    = 0.5  -> 중심부 50%
    scale_periphery = 0.8  -> 바깥쪽 20% (양쪽 벽에서 각 10%)가 edge/periphery
    scale_corners   = 0.4  -> 네 모서리 40% 영역
"""
import numpy as np


def calibrate_arena(data, corner_points=("tl", "tr", "br", "bl")):
    """
    네 모서리 bodypart의 중앙값 좌표로 arena의 중심, 한 변 길이(반경)를 추정.
    반환: dict(center_x, center_y, half_size)
    """
    missing = [c for c in corner_points if c not in data]
    if missing:
        raise KeyError(
            f"corner bodypart {missing} 가 csv에 없습니다. "
            f"사용 가능한 bodypart: {list(data.keys())} 중에서 corner_points를 다시 지정하세요."
        )

    xs = [np.nanmedian(data[c]["x"]) for c in corner_points]
    ys = [np.nanmedian(data[c]["y"]) for c in corner_points]

    center_x = float(np.mean(xs))
    center_y = float(np.mean(ys))
    # 중심에서 모서리까지 평균 거리 -> arena 절반 크기(대각선 기준 보정)
    half_size = float(np.mean([np.hypot(x - center_x, y - center_y) for x, y in zip(xs, ys)]) / np.sqrt(2))

    return {"center_x": center_x, "center_y": center_y, "half_size": half_size}


def classify_zone(x, y, arena, scale_center=0.5, scale_periphery=0.8):
    """
    좌표(x, y) 배열을 받아 'center' / 'periphery' 라벨 배열로 분류.
    scale_periphery=0.8 -> 중심으로부터 0.8*half_size 바깥은 periphery(edge)
    scale_center=0.5    -> 중심으로부터 0.5*half_size 이내는 center
    그 사이는 'middle'로 둠 (필요시 분석에서 제외하거나 periphery에 합산 가능)
    """
    dx = (x - arena["center_x"]) / arena["half_size"]
    dy = (y - arena["center_y"]) / arena["half_size"]
    dist = np.maximum(np.abs(dx), np.abs(dy))  # 정사각형 arena 기준 Chebyshev distance

    zone = np.full(dist.shape, "middle", dtype=object)
    zone[dist <= scale_center] = "center"
    zone[dist > scale_periphery] = "periphery"
    return zone


def edge_preference_summary(zone_labels, fps):
    """
    zone 라벨 시계열로부터 edge(periphery) preference 지표 계산.
    """
    n = len(zone_labels)
    periphery_frames = int(np.sum(zone_labels == "periphery"))
    center_frames = int(np.sum(zone_labels == "center"))

    return {
        "total_frames": n,
        "total_time_s": n / fps,
        "time_periphery_s": periphery_frames / fps,
        "time_center_s": center_frames / fps,
        "pct_time_periphery": 100 * periphery_frames / n,
        "pct_time_center": 100 * center_frames / n,
    }
