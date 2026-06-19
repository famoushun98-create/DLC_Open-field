# PD Open Field — Edge Preference & Motor Deficit 분석 파이프라인

PD(Parkinson's disease) 모델 마우스의 open field 녹화에서
**motor deficit**(운동 결손)과 **depression-like phenotype (edge preference)**를
정량화하기 위한 분석 파이프라인입니다.

현재 PD 모델 데이터가 준비되기 전, 동일 형식의 공개 데이터셋
([Zenodo 8188683](https://zenodo.org/records/8188683), 요힘빈 주사 open field,
ETHZ-INS/Bohacek lab, CC-BY 4.0)으로 파이프라인이 정상 작동하는지
**Google Colab에서 먼저 테스트**합니다.

## 빠른 시작 (Colab)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/famoushun98-create/PD-OpenField-EdgePreference/blob/main/notebooks/test_pipeline_colab.ipynb)

위 배지를 클릭하면 별도 설치 없이 바로 실행할 수 있습니다.
(노트북 안에서 데이터를 Zenodo에서 직접 다운로드합니다.)

## 레포 구조

```
PD-OpenField-EdgePreference/
├── README.md
├── requirements.txt
├── notebooks/
│   └── test_pipeline_colab.ipynb   # Colab 테스트용 메인 노트북
└── src/
    ├── dlc_io.py        # DeepLabCut pose csv 로더
    ├── oft_zones.py      # arena calibration + edge(periphery)/center zone 분류
    └── motor_metrics.py  # 속도/이동거리/부동시간 등 motor 지표
```

## 분석 정의

### Edge (periphery) zone 정의
이 데이터셋을 만든 ETHZ-INS 연구팀의 R 패키지
[`DLCAnalyzer`](https://github.com/ETHZ-INS/DLCAnalyzer)의 `AddOFTZones()` 기본값을
그대로 따릅니다.

- 네 모서리(top-left/top-right/bottom-right/bottom-left) bodypart 좌표로 arena를 보정(calibrate)
- `scale_center = 0.5` → 중심으로부터 50% 이내 = **center**
- `scale_periphery = 0.8` → 중심으로부터 80% 밖 = **periphery (edge)**
  (벽에서 arena 한 변 길이의 약 10% 이내)

### Motor deficit 지표
- 총 이동거리(total distance traveled)
- 평균/최대 속도
- 부동(immobility) 시간 비율

이 지표들은 `src/motor_metrics.py`, edge 관련 지표는 `src/oft_zones.py`에 구현되어 있습니다.

## PD 모델 데이터로 교체하는 방법

노트북 상단의 다음 변수만 수정하면 동일 파이프라인을 PD 데이터에 그대로 사용할 수 있습니다.

| 변수 | 설명 |
|---|---|
| `RECORD_ID` / 데이터 다운로드 셀 | Zenodo 대신 본인 데이터 경로/Google Drive 경로로 교체 |
| `SAMPLE_IDS` | 분석할 동물(파일) 목록 |
| `CORNER_POINTS` | arena 모서리로 쓸 DLC bodypart 이름 (csv마다 다를 수 있음) |
| `CENTER_BODYPART` | 동물 중심점으로 쓸 bodypart 이름 |
| `FPS` | 실제 녹화 fps |

## 데이터 출처 및 인용

```
von Ziegler, L. M., Roessler, F. K., Sturman, O., O'Connor, E. C., & Bohacek, J. (2023).
Raw video and pose estimation data of top view open field mouse behavior recordings
after yohimbine injections [Data set]. Zenodo. https://doi.org/10.5281/zenodo.8188682
        
        
```

라이선스: [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode)

참고: 같은 그룹의 zone 정의 방법론은
[Sturman et al., *Nature Methods* (2024), "Analysis of behavioral flow resolves latent phenotypes"](https://www.nature.com/articles/s41592-024-02500-6)
및 [BehaviorFlow](https://github.com/ETHZ-INS/BehaviorFlow) 레포 참고.

## 참고사항
- 원본 비디오/csv 파일은 용량 문제로 이 레포에 직접 포함하지 않고, 노트북이 Zenodo에서
  필요한 샘플만 그때그때 다운로드합니다.
- 본 레포는 **파이프라인 검증용**이며, 실제 PD 데이터 분석 결과가 아닙니다.
