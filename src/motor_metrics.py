"""
Motor activity / motor deficit 관련 지표 계산.
PD 모델에서 흔히 보는 지표: 총 이동거리(distance traveled),
평균/최대 속도, 부동(immobility) 시간 비율 등.
"""
import numpy as np


def compute_speed(x, y, fps, px_to_cm=None):
    """
    프레임 간 이동 속도(px/s 또는 cm/s) 계산.
    px_to_cm: 1픽셀이 몇 cm인지 (arena 실측 크기로 calibration 시 사용).
              None이면 픽셀 단위로 반환.
    """
    dx = np.diff(x, prepend=x[0])
    dy = np.diff(y, prepend=y[0])
    dist_per_frame = np.hypot(dx, dy)

    if px_to_cm is not None:
        dist_per_frame = dist_per_frame * px_to_cm

    speed = dist_per_frame * fps  # 단위/초
    return speed, dist_per_frame


def motor_summary(speed, dist_per_frame, fps, movement_cutoff=2.0):
    """
    movement_cutoff: 이 값(단위/초) 이상일 때 '움직이는 중'으로 간주.
    DLCAnalyzer 기본 관례를 따름 (cm/s 기준 추천).
    """
    total_distance = float(np.nansum(dist_per_frame))
    moving = speed >= movement_cutoff
    pct_time_moving = 100 * float(np.sum(moving)) / len(speed)

    return {
        "total_distance": total_distance,
        "mean_speed": float(np.nanmean(speed)),
        "max_speed": float(np.nanmax(speed)),
        "pct_time_moving": pct_time_moving,
        "pct_time_immobile": 100 - pct_time_moving,
    }
