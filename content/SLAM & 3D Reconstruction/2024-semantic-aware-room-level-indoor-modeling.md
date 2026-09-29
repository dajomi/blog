---
title: "Semantic-aware Room-level Indoor Modeling — 점군에서 방 단위 3D 모델을 자동 생성하는 방법 (JAG 2024)"
date: 2026-09-28
description: "실내 점군을 층별로 수평 단면화해 선형 요소로 2D 공간을 face로 분할하고, 에너지 최소화로 실내 face를 판별한 뒤, KPConv semantic segmentation으로 만든 room semantic map으로 방을 나눠 수직 돌출해 방 단위 3D 모델을 만드는 논문 리뷰"
category: "SLAM & 3D Reconstruction"
tags:
  - paper-review
  - indoor-modeling
  - point-cloud
  - floorplan-reconstruction
  - room-segmentation
  - energy-minimization
aliases:
  - Semantic-aware room-level indoor modeling
  - Chen 2024
paper_title: "Semantic-aware room-level indoor modeling from point clouds"
authors:
  - Dong Chen
  - Lincheng Wan
  - Fan Hu
  - Jing Li
  - Yanming Chen
  - Yueqian Shen
  - Jiju Peethambaran
venue: "International Journal of Applied Earth Observation and Geoinformation, Vol. 127, 103685"
year: 2024
paper_type: journal
doi: "10.1016/j.jag.2024.103685"
url: "https://doi.org/10.1016/j.jag.2024.103685"
verification: full-text
---

> [!info] 검증 범위
> 서지정보는 Crossref와 출판사 페이지에서, 초록·방법·수치는 원문 전문(오픈 액세스, CC BY-NC-ND)에서 확인했다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | Semantic-aware room-level indoor modeling from point clouds |
| 저자 | Dong Chen, Lincheng Wan, Fan Hu, Jing Li, Yanming Chen, Yueqian Shen(교신), Jiju Peethambaran |
| 소속 | Nanjing Forestry University, Hohai University, Saint Mary's University 등 |
| 연도 | 2024 (온라인 공개 2024년 2월) |
| 저널/학회 | International Journal of Applied Earth Observation and Geoinformation(JAG), Vol. 127, Article 103685 |
| 연구 분야 | Indoor 3D Modeling, Floorplan Reconstruction, Point Cloud Semantic Segmentation |
| 핵심 기술 | Horizontal Slicing, RANSAC + MeanShift, Half-edge 구조, MRF 이진 에너지 최소화(Graph Cut), KPConv, 수리 형태학 |
| DOI | [10.1016/j.jag.2024.103685](https://doi.org/10.1016/j.jag.2024.103685) |
| 원문 | [ScienceDirect (Open Access)](https://www.sciencedirect.com/science/article/pii/S1569843224000396) |
| 코드 | [indoor-modeling/indoor-modeling](https://github.com/indoor-modeling/indoor-modeling) |

## 1. 연구 배경

실내 공간 모델을 자동으로 만들려면 방 경계를 어떻게 자동으로 결정할지가 핵심 문제다. 이 문제는 floorplan reconstruction이라는 별도 연구 분야로 발전해 왔다.

3D 실내 모델은 실내 navigation, 실내 가구 배치와 재현, 레이아웃 설계 등 여러 응용에 중요하다. 실내 공간은 보통 LiDAR, SfM, MVS로 얻은 점군(Kinect, Google Tango, HoloLens, Matterport 등)을 추상화해 여러 LoD의 폴리곤 mesh로 재구성한다. 이런 모델은 AR·VR 시각화 요구는 충족하지만, 모델 기반 계산·분석에는 기하 정확도가 낮고 topology가 유효하지 않으며 semantic이 부족하다는 문제가 있다.

저자들은 원인을 세 가지로 본다. 실내 구조가 복잡하다(바닥·천장·벽·창·발코니 같은 고정 요소와 다양한 가구). 점군 품질이 낮다(자기 가림과 가구 가림으로 인한 잡음·이상치·누락). 방법론이 추가 정보에 의존한다.

저자들은 기존 실내 모델링 방법을 네 갈래로 정리한다.

- Primitive 기반: 기하 primitive를 찾아 watertight mesh로 조립한다. 결함 많은 점군에 취약하다. FloorNet, Floor-SP, Point2Roof 같은 딥러닝으로 primitive semantic, 모서리 위치, 연결 관계를 추론하기도 한다.
- Slice 기반: 평면 primitive로 공간을 polyhedral cell이나 polygonal facet으로 나누고 최적화로 선택한다. 견고하지만 최적화가 복잡하다.
- Mesh 단순화: 조밀한 mesh를 점진적으로 줄인다. 인공물의 날카로운 특징이 약해질 수 있다.
- Floorplan 기반: 3D 모델링을 2D 평면도 문제로 바꾸고 방 높이만큼 돌출한다. 누락 데이터에 강하지만 효율이 낮고 방 단위 semantic이 부족하다.

이 논문은 floorplan 기반 방법에 속한다. 도시 건물은 층마다 외형이 수직 방향으로 일관된다는 점을 이용한다.

## 2. 연구 Gap

**기존 연구의 한계**

- 많은 방법이 room semantic map, 스캐너 궤적, 정합된 이미지 같은 추가 데이터를 요구해 적용성과 일반화가 제한된다.
- 문제를 단순화하려고 Manhattan-world, Atlanta-world, 중력 방향 구간 상수 가정을 흔히 쓰는데, 이는 일반화와 확장성을 떨어뜨린다.
- Floorplan 기반 방법은 방 단위 semantic이 부족하다.

**본 연구가 해결하려는 Gap**

점군만으로, Manhattan·Atlanta 가정 없이, 곡선형 벽을 포함한 복잡한 실내의 고정 구조를 재구성한다. 결과 모델은 compact한 기하, 유효한 mesh topology, 그리고 고정 구성요소 semantic과 방 수준 semantic을 함께 가진다.

## 3. 연구 질문

논문의 목적과 기여를 바탕으로 재구성하면 다음과 같다.

1. 3D 방 모델링 문제를 2D 평면도의 face 조립 문제로 바꿔 복잡도를 줄일 수 있는가?
2. 2D face를 실내·실외로 정확히 구분하는 전역 최적화를 설계할 수 있는가?
3. 점군 semantic segmentation으로 얻은 room semantic을 이용해 방 단위의 세밀한 모델을 만들 수 있는가?

## 4. 핵심 기여

저자들이 제시한 기여는 세 가지다.

1. 2D face 조립으로 3D 방 모델링을 2D 평면도 재구성 문제로 변환해 실내 구성의 복잡도를 줄였다.
2. 정합(alignment) 항과 문맥(contextual) 항을 함께 고려하는 이진 에너지 최소화로 실내·실외 2D face를 인식하는 전역 최적화 알고리즘을 제안했다.
3. CNN 기반 semantic segmentation으로 얻은 semantic 점에서 room semantic을 만들어, 방 단위의 세밀한 재구성을 semantic-aware하게 수행했다.

기존 방식 → 문제 → 제안 → 개선 관계로 보면, 점군에서 직접 3D 방 모델을 만드는 대신 층별 2D face 문제로 바꾸고, semantic 지도로 face를 방에 할당해 기하와 방 semantic을 함께 확보한다.

## 5. 연구 방법론

### 연구 대상 / 데이터

- S3DIS(Stanford 3D Indoor Scene Dataset): Matterport 스캐너로 수집한 대규모 실내 장면 6개, 방 272개
- 각 점은 XYZ, RGB, 방 인스턴스 라벨, 13개 semantic 범주(천장, 바닥, 벽, 보, 기둥, 창, 문 / 테이블, 의자, 소파, 책장, 보드 / 잡동사니) 중 하나를 가진다.
- 개인 사무실, 회의실, 강당, 로비, 라운지, 복도, 계단, 복사실, 탕비실, 오픈 스페이스, 창고, 화장실 등 다양한 공간을 포함한다.
- 저자들은 S3DIS에 일부 오라벨·중복 점이 있어 semantic 라벨을 다시 예측해 사용했다(아래 "semantic 재라벨링").

### 시스템 구조

두 갈래로 진행된다.

```text
[갈래 1: 2D 공간 분할과 실내 face 인식]
Indoor Point Cloud (층별)
↓
Horizontal Slicing (두께 0.5 m, 여러 단면 융합, 이상치 제거)
↓
RANSAC 선형 요소 검출 (임계값 0.05 m)
↓
MeanShift로 선형 요소 정리 (kernel bandwidth 0.2)
↓
선형 요소 연장 → 2D 공간을 겹치지 않는 face로 분할 (half-edge 구조)
↓
MRF 이진 에너지 최소화 (Graph Cut, alpha-expansion) → face를 실내 / 실외로 분류
↓
외곽·내부 경계 ring 추적 → constrained Delaunay 삼각분할 → 평균 높이로 돌출
↓
층 단위(coarse) 모델

[갈래 2: room semantic map]
KPConv semantic segmentation → 천장 / 바닥 / 벽 / 창 / 문 / 잡동사니
↓
바닥 semantic map (천장+바닥 점, 해상도 0.05 m)
벽 semantic map (벽+창 점, 해상도 0.15 m)
↓
벽 지도에서 바닥 지도를 뺀 difference map
↓
수리 형태학으로 방 단위 분할 → room semantic map (방 면적 5 m² ~ 1,000 m²)

[결합]
room semantic map을 실내 face에 겹쳐 face별 방 할당
↓
같은 방 face 묶기 → 방 경계 추적 → 방 높이 결정 → 삼각분할·돌출
↓
방 단위(fine) 3D Room Models
```

### 단계별 방법

**2D 공간 분할**

- 층마다 두께 0.5 m로 수평 단면을 잘라 대표 2D 단면을 얻는다. 가구 가림과 유리(창·문·발코니)로 인한 누락을 줄이려고 여러 단면을 합친다. 평균 점 밀도의 3배 이상 벗어난 점은 제거한다.
- 평면도가 구간별 선형이라고 가정하고 RANSAC(0.05 m)으로 선형 요소를 찾는다. 엄격한 임계값 때문에 작은 요소가 과다하게 생기므로 MeanShift로 줄여 정확도와 간결성의 균형을 맞춘다.
- 선형 요소를 연장해 2D 공간을 공통 edge를 공유하는 face들로 나누고, half-edge 자료구조로 꼭짓점·edge·face 간 인접 관계를 상수 시간에 조회한다.

**실내 face 인식 (이진 에너지 최소화)**

- 전역 에너지 `E(l) = λ Σ 정합항 + Σ 문맥항`을 Markov Random Field로 정의하고, 각 face에 실내(1) 또는 실외(0) 라벨을 부여한다.
- 정합항: 단면 영역에 무작위 점을 뿌리고, 바닥 semantic map에서 각 점이 실내인지 확인한다. face 안의 실내 점 비율이 낮은데 실내 라벨이면 벌점을 준다.
- 문맥항: 인접한 두 face의 공통 edge를 선분으로 바꿔 벽 semantic map에 겹친다. 두 face의 라벨이 다를 때, 공통 edge가 벽일 확률이 낮을수록 벌점을 준다. 벽 사이가 아닌데 실내·실외가 갈리는 것을 막는다.
- 초기 라벨은 바닥 semantic map으로 정하고, Graph Cut(alpha-expansion)으로 최소화한다.
- 층 단위 모델은 실내 face의 경계 edge를 추적해 외곽 ring과 내부 ring을 만들고, constrained Delaunay 삼각분할로 지붕을 만들며, 경계 ring을 평균 건물 높이로 돌출해 벽을 만든다.

**Room semantic map**

- KPConv로 점을 6개 클래스(천장, 바닥, 벽, 창, 문, 잡동사니)로 분류한다.
- 천장·바닥 점을 0.05 m로 래스터화한 바닥 semantic map은 벽 두께 때문에 방 사이가 어느 정도 분리된다. 그러나 열린 문 때문에 대부분 방이 인접 복도로 새어 나가 방이 닫히지 않는다.
- 벽·창 점을 래스터화한 벽 semantic map은 닫힌 성질이 있어 이를 보완한다. 벽 지도에서 바닥 지도를 뺀 difference map에 수리 형태학을 적용하면 방 사이, 방과 복도 사이 경계가 모두 정확히 나뉜다.
- 5 m²보다 작은 조각은 인접한 큰 조각에 합치고, 1,000 m²를 넘는 조각은 나눈다. 길고 좁은 복도 처리에 효과적이라고 설명한다.

**방 단위 모델링**

- Room semantic map을 실내 face에 겹쳐 face별 방을 정한다. 연결되어 있고 같은 방 semantic을 가진 face가 하나의 방이 된다.
- 방마다 경계를 추적하고, 천장과 바닥의 높이 차로 방 높이를 정한다. 방 안 face들의 높이가 다르면 같은 높이끼리 나눠 따로 모델링한 뒤 합친다. 천장·바닥 점이 없으면 벽 높이로, 완전히 누락되면 가장 가까운 face 높이로 추정한다.
- 평면도를 삼각분할하고 방 높이로 돌출한 뒤, 모든 방 모델을 합친다.

**Semantic 재라벨링**

- S3DIS 원래 라벨에 오라벨·중복이 있어, 5개 고전 모델(PointNet, SPGraph, PointCNN, KPConv, RandLA-Net)을 Scene 5를 테스트로, 나머지 5개 장면을 학습으로 평가했다. KPConv가 13개 클래스 기준 mIoU 70.6%로 가장 높았다.
- 13개 클래스를 6개로 합친 뒤(보·기둥·보드·벽 → 벽, 테이블·의자·소파·책장·잡동사니 → 잡동사니) KPConv를 다시 학습했고, 이 모델로 S3DIS 전체 점의 라벨을 예측해 모델링에 사용했다.

### 파라미터

| 모듈 | 파라미터 | 권장값 |
|---|---|---|
| 수평 단면 | 두께 | 0.5 m |
| 선형 요소 추출 | RANSAC 임계값 | 0.05 m |
| 선형 요소 정리 | MeanShift kernel bandwidth | 0.2 |
| Room semantic map | 최소·최대 방 면적 | 5 m², 1,000 m² |
| 실내 face 인식 | 바닥 지도 해상도 / 벽 지도 해상도 / λ | 0.05 m / 0.15 m / 0.5~1.0 |

- 벽 지도 해상도: 0.05 m이면 두 방에서 두 번 스캔된 내벽이 두 겹으로 나타나 공통 edge가 벽일 확률이 낮게(예: 0.4) 계산된다. 이 경우 실내 face가 실외로 잘못 분류될 수 있다. 0.15 m로 낮추면 두 겹 구조가 사라진다.
- λ: 5나 10처럼 크면 실내 누락 영역 때문에 실내 face가 실외로, 0.01처럼 작으면 실외 face가 실내로 잘못 분류된다. 0.5~1.0이 누락·오포함의 균형이 좋았다.

### 사용 기술

- 수평 단면화, RANSAC, MeanShift
- Half-edge 자료구조
- Markov Random Field, Graph Cut(alpha-expansion)
- Constrained Delaunay 삼각분할
- KPConv(비교: PointNet, SPGraph, PointCNN, RandLA-Net)
- 수리 형태학 기반 영역 분할

### 평가 방법

- Semantic segmentation: 클래스별 IoU, mIoU(Scene 5 테스트)
- 실내·실외 face 라벨링: precision, recall, F1-score(정답 face는 room semantic map 기반 자동 판정 후 전부 수작업 검증)
- 방 모델 기하 정확도: 원본 점에서 가장 가까운 삼각 mesh까지 거리의 Min, Max, MAE
- 생성된 방 수와 원래 방 수 비교
- S3DIS 기준 mesh와의 비교: Min, Max, MAE, RMSE

## 6. 핵심 결과

**Semantic segmentation (Scene 5 테스트)**

- 13개 클래스 기준 mIoU: KPConv 70.6%, RandLA-Net 70.0%, PointCNN 65.4%, SPGraph 62.1%, PointNet 47.6%
- 6개 클래스로 합친 뒤 KPConv mIoU 76.1%. 클래스별로 천장 93.2%, 바닥 98.3%, 벽 84.1%, 창 44.6%, 문 49.5%, 잡동사니 86.6%

**실내·실외 face 라벨링**

| 장면 | 실내 Precision | 실내 Recall | 실내 F1 | 실외 F1 |
|---|---|---|---|---|
| Scene 1 | 95.87 | 97.48 | 96.67 | 92.45 |
| Scene 2 | 96.64 | 97.70 | 97.17 | 94.20 |
| Scene 3 | 97.27 | 97.46 | 97.37 | 97.57 |
| Scene 4 | 95.54 | 97.67 | 96.59 | 92.43 |
| Scene 5 | 99.32 | 99.32 | 99.32 | 98.74 |
| Scene 6 | 97.65 | 98.21 | 97.92 | 95.48 |

(단위: %)

- 실내 face F1은 모든 장면에서 96% 이상이었다.
- 오류는 주로 실내외 전이 지역인 외벽의 돌출·함입 부분과 작은 face에서 발생했다. 곡선형 형상을 선형 요소로 근사하면 공간 분할이 복잡해져 오류 가능성이 커지므로, 건물을 주요 방향으로 정렬하는 전략을 썼다.

**방 단위 모델 정확도**

| 장면 | Max (m) | MAE (m) | 생성 방 수 | 원래 방 수 |
|---|---|---|---|---|
| Scene 1 | 1.13 | 0.06 | 57 | 44 |
| Scene 2 | 1.20 | 0.11 | 40 | 40 |
| Scene 3 | 1.14 | 0.10 | 31 | 23 |
| Scene 4 | 1.34 | 0.09 | 48 | 49 |
| Scene 5 | 1.37 | 0.12 | 54 | 68 |
| Scene 6 | 1.71 | 0.11 | 52 | 48 |

(Min은 모든 장면에서 0.00 m)

- MAE는 약 0.1 m 수준이다. Max 오차가 모두 1 m를 넘는데, 대부분 누락 데이터 때문이다.
- 생성된 방 수가 원래보다 많은 경우(Scene 3, 6 등): 외벽의 과도한 돌출 부분을 별도 방으로 잘못 분류했다.
- 적은 경우(Scene 4, 5): 복도와 오픈 스페이스가 기둥으로만 구분되고 복도와 이어진 벽이 적어 과소분할되었다. S3DIS 원래 데이터에서는 복도가 여러 부분으로 수작업 분할되어 있는데, 벽이 없어 이 경계를 재현하기 어려웠다.
- 오류 원인은 세 가지로 정리된다: 외벽의 작은 돌출·함입을 선형 요소가 잡지 못함, 계단 공간의 심한 누락, 긴 복도의 오분할(복도 부분마다 높이가 다를 때 높이도 틀림).

**S3DIS 기준 mesh와의 비교**

- MAE 0.08~0.15 m, RMSE 0.15~0.21 m, Max 1.17~1.32 m
- 차이는 주로 돌출·함입 영역, 누락이 심한 계단, 자유형 천장에서 생겼다.

## 7. 결론 및 시사점

저자들은 점군과 semantic으로 방 단위 구조 모델을 재구성하는 프레임워크를 제시했다고 결론짓는다. 층별 외형의 일관성을 이용해 3D 문제를 2D 평면도 구성 문제로 바꾸고, 이진 에너지 최소화로 실내외를 구분하며, semantic으로 방 배치를 찾는다. 결과 모델은 방 수준뿐 아니라 부분 수준(내벽·외벽·천장·바닥) semantic도 가지며, 각 방 모델과 그 semantic 구성요소를 연결할 수 있다.

이 논문은 점군에서 구조, 방, semantic 정보를 함께 생성하는 과정이 상당 수준 자동화되고 있음을 보여준다. 다만 저자들이 말하는 "correct topology"는 mesh와 방 배치의 유효성을 가리키며, 문을 통한 방 간 연결 그래프(navigation topology)를 만든 것은 아니다. 실제로 문과 창은 방 모델에서 다루지 않았다.

- SLAM / 3D Reconstruction: 스캔 결과를 방 단위 구조 모델로 변환하는 후처리 단계의 대표 사례다.
- Indoor GIS / IndoorGML: 방 폴리곤은 IndoorGML CellSpace 생성의 입력이 될 수 있다. navigation network까지 가려면 문 검출과 연결 복원이 추가로 필요하다.
- BIM: 방과 벽 배치를 가진 모델은 Scan-to-BIM의 IfcSpace, IfcWall 생성과 연결된다.
- Digital Twin: 기존 건물의 as-is 공간 모델을 자동으로 구축하는 데 활용할 수 있다.

## 8. 연구의 한계

### 저자가 명시한 한계

- 인접한 방이 공유하는 내벽의 두께를 고려하지 않는다. 두 방에서 각각 스캔된 두 겹의 점을 따로 분석해 내벽 두께를 추정할 계획이다.
- 고정 구조 모델링에 집중해 창, 발코니, 문 같은 작은 돌출·함입 요소를 다루지 않았다. 레이아웃을 검출하고 미리 정의한 요소 모델을 맞추는 방식으로 해결할 계획이다.
- 가구 같은 이동 가능한 물체를 모델에 넣지 않았다. 위치를 인식해 CAD 모델로 대체할 계획이다.
- 평면도가 구간별 선형이라고 가정하므로, 돌출된 실내 모델은 구간별 평면 표면과 수직 벽을 전제한다.
- 벽이 적은 긴 복도와 오픈 스페이스를 정확히 분할하기 어렵고, 계단 등 누락이 심한 공간을 완전히 복원하지 못한다.

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 모델링에 쓴 semantic 라벨은 KPConv가 예측한 것인데, 이 KPConv는 Scene 5를 제외한 다섯 장면으로 학습되었다. 따라서 Scene 1~4, 6의 모델링은 학습에 쓴 장면을 다시 예측한 라벨에 기반한다. 새로운 건물에서는 semantic 정확도가 Scene 5 수준(mIoU 76.1%) 이하일 가능성이 크고, 그만큼 모델링 성능도 떨어질 수 있다.
- 실내 face 정답을 room semantic map 기반으로 자동 판정한 뒤 수작업 검증했다. 방법 자체가 쓰는 semantic 지도로 정답을 만든 셈이어서 평가가 방법에 유리하게 편향될 여지가 있다.
- 평가 대상 장면 수 표기가 본문 안에서 일관되지 않는다. 초록은 "6개 장면", 서론 끝부분은 "4개 장면", 층 단위 모델 평가는 "마지막 4개 장면"이라고 하고, 표는 6개 장면을 모두 보고한다.
- 생성된 방 수가 원래와 크게 다른 장면이 있다(Scene 1: 57 대 44, Scene 5: 54 대 68). 방 단위 precision·recall 같은 인스턴스 수준 지표가 없어 방 분할 정확도를 직접 판단하기 어렵다.
- 층 내부 천장 높이 변화는 face 단위로 처리하지만, 경사 천장이나 복층 공간은 수직 돌출 방식으로 표현하기 어렵다.

## 9. 비판적 읽기

### 연구 설계

- 강점: 3D 문제를 2D face 조립과 이진 에너지 최소화로 정식화해 최적화 가능한 형태로 만들었다. 파라미터 민감도를 분석하고 전역·국소 영역 최적화의 일관성을 확인했다. 코드를 공개했다.
- 약점: 방 분할은 수리 형태학 기반 room semantic map에 크게 의존하는데, 이 단계의 정확도를 따로 평가하지 않았다.

### 데이터

- 공개 데이터셋(S3DIS) 6개 장면, 방 272개를 사용해 재현성이 있다. 다만 모두 같은 데이터셋(대학 건물군)이다.

### Baseline / 비교군

- Semantic segmentation은 5개 모델과 비교했다.
- 모델링 결과는 S3DIS 기준 mesh(조밀한 mesh를 단순화한 것)와만 비교했다. 다른 실내 모델링 방법(Floor-SP, 기존 floorplan 기반 방법 등)과의 정량 비교는 없다.

### 평가 지표

- 점-mesh 거리(MAE, RMSE)는 기하 정확도 평가에 적절하다. 방 인스턴스 분할의 정확도, 방 간 인접 관계의 정확도를 평가할 지표는 없다.

### 데이터 신뢰성

- 저자들이 S3DIS 라벨의 오류를 발견하고 재라벨링한 점은 투명하다. 다만 재라벨링을 모델 예측으로 했기 때문에 위의 학습-평가 중첩 문제가 생긴다.

### 주장과 결과의 관계

- "accurate geometry, correct topology, rich semantics"라는 주장 중 기하 정확도는 수치로 뒷받침된다. topology와 semantic의 정확도는 정성적이며, 방 수 불일치 사례가 함께 보고되어 있다.
- "Manhattan·Atlanta 가정 없이"라는 주장은 맞지만, 대신 구간별 선형 평면도와 수직 벽을 가정한다는 점을 함께 봐야 한다.

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 낮음 | 중국 국가자연과학기금 지원. 저자들은 경쟁적 이해관계가 없다고 선언 |
| 선택 편향 | 중간 | S3DIS 단일 데이터셋. 모델링에 쓴 semantic 라벨 예측 모델의 학습 장면과 평가 장면이 겹침 |
| 확증 편향 | 중간 | 정답 face를 방법이 쓰는 room semantic map으로 자동 생성 후 검증. 다만 방 수 불일치와 오류 원인을 명시 |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 중간 | 미국 대학 건물 기반 데이터셋 |

## 11. 주요 전문 용어

### Floorplan Reconstruction

점군이나 영상에서 건물의 평면도(방, 벽 배치)를 자동으로 복원하는 작업이다.

### Horizontal Slicing

점군을 특정 높이에서 수평으로 잘라 2D 단면을 얻는 처리다. 벽 위치를 파악하는 데 쓰인다.

### Half-edge 자료구조

각 edge를 방향이 반대인 두 half-edge로 나눠 저장해, 꼭짓점·edge·face 사이의 인접 관계를 빠르게 조회하는 자료구조다.

### Energy Minimization / Graph Cut

각 요소의 라벨을 정할 때 데이터와의 일치도(정합항)와 이웃 간 일관성(문맥항)을 합친 비용 함수를 최소화하는 방식이다. Graph Cut은 이를 최대 유량·최소 절단 문제로 바꿔 푼다.

### Mathematical Morphology

팽창, 침식, 열기, 닫기 같은 연산으로 영상의 형태를 분석·분할하는 기법이다.

### S3DIS

Stanford Large-Scale 3D Indoor Spaces Dataset. 대학 건물 실내를 스캔하고 semantic 라벨을 붙인 대표적인 실내 점군 데이터셋이다.

### KPConv

Kernel Point Convolution. 점군에 직접 합성곱을 적용하는 딥러닝 기반 point cloud segmentation 방법이다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

- 수평 단면화, RANSAC, MeanShift
- Half-edge 자료구조, MRF + Graph Cut(alpha-expansion)
- Constrained Delaunay 삼각분할
- KPConv(비교: PointNet, SPGraph, PointCNN, RandLA-Net)
- 수리 형태학
- S3DIS 데이터셋

### 실무 구현 시 적용 가능한 기술

아래는 서비스 구현 시 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**Point Cloud**
- Open3D, PCL, PDAL, CloudCompare

**GIS / 기하 처리**
- GDAL/OGR, Shapely, CGAL(arrangement, half-edge)

**Spatial DB**
- PostgreSQL + PostGIS(방 폴리곤 저장과 공간 질의)

**표준 변환**
- IndoorGML CellSpace, IFC IfcSpace로 export

**Visualization**
- QGIS(2D 평면도 검수), Cesium(3D 방 모델)

## 13. 커리어 관점

### 공부해야 할 기술

- Point cloud 전처리와 단면 추출
- 2D 공간 분할(arrangement)과 폴리곤 연산
- Point cloud semantic segmentation
- Graph Cut 기반 에너지 최소화
- 수리 형태학 기반 영역 분할

### 실무 연결

- 공간 관점: 층 단위로 실내·실외 경계를 먼저 정하고, 그 안을 방 단위로 나눈 뒤, 방마다 높이를 부여하는 순서는 실내 공간 모델 구축의 기본 틀이다. 공장이라면 건물 외곽 → 구역 → 구역별 높이 순으로 공간을 먼저 만들고 설비를 얹을 수 있다.
- 스캔 데이터 기반 실내 공간정보 구축(실내 지도, 시설관리)
- Scan-to-BIM 자동화
- 실내 navigation graph 생성을 위한 방 폴리곤 자동 추출

### 기술 면접으로 연결될 수 있는 질문

- 점군에서 방 경계를 자동으로 추출하는 방법에는 어떤 것들이 있는가?
- 3D 모델링 문제를 2D 평면도 문제로 바꿨을 때의 장점과 한계는 무엇인가?
- 이진 에너지 최소화에서 데이터 항과 문맥 항은 각각 어떤 역할을 하는가?
- 열린 문 때문에 방 분할이 복도로 새어 나가는 문제를 어떻게 해결할 수 있는가?
- 방 폴리곤을 IndoorGML CellSpace나 IfcSpace로 바꿀 때 무엇을 더 해야 하는가?

## 14. 후속 연구

### 저자가 제안한 Future Work

- 두 겹으로 스캔된 내벽 점을 분석해 내벽 두께 추정
- 창, 발코니, 문 같은 작은 요소의 레이아웃을 검출하고, 미리 정의한 요소 모델을 맞추는 모델 기반 전략으로 반영
- 가구 등 이동 물체의 위치를 인식해 CAD 모델로 대체하고, 매우 복잡한 물체는 동일 물체 정합이나 mesh 단순화로 표현한 뒤 고정 구조 모델과 합쳐 완전한 장면 모델 구성

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- 방 모델에 문 위치를 결합해 IndoorGML navigation network까지 자동 생성
- 층간 연결(계단, 엘리베이터)을 포함한 다층 모델로 확장
- 벽이 적은 개방형 공간을 기능·객체 단서로 분할
- 3DGS나 SLAM 실시간 출력에 적용 가능한 증분형 방 모델링

## 15. 논문 읽기 가이드

**1순위 — Fig. 1 (전체 파이프라인)**

두 갈래(face 분할·인식, room semantic map)와 결합 과정을 먼저 파악한다.

**2순위 — 3.2절 (실내 face 인식)과 Fig. 3**

정합항과 문맥항이 바닥·벽 semantic map을 어떻게 쓰는지 이해한다.

**3순위 — 3.4절 (room semantic map)과 Fig. 5, 6**

바닥 지도만으로는 방이 복도로 새는 문제와, difference map으로 해결하는 방식을 확인한다.

**4순위 — 4.5절과 Table 5, Fig. 15**

방 모델 정확도, 방 수 불일치의 원인, 오류가 생기는 공간 유형을 확인한다.

## 16. 핵심 정리

- 3D 방 모델링을 층별 2D face 조립 문제로 바꾸면 이진 에너지 최소화로 풀 수 있는 형태가 된다.
- 바닥 semantic map은 실내·실외 판정에, 벽 semantic map은 인접 face 간 경계 판정에 쓰인다. 벽 지도에서 바닥 지도를 빼면 열린 문으로 새지 않는 room semantic map을 얻는다.
- 실내 face F1은 모든 장면에서 96% 이상, 방 모델 MAE는 약 0.1 m였다. 복도·오픈 스페이스·계단에서는 방 수가 맞지 않거나 오차가 컸다.
- 이 논문의 "topology"는 mesh와 방 배치의 유효성이다. 문을 통한 방 간 연결 그래프는 만들지 않으므로, navigation 모델로 쓰려면 문 검출과 연결 복원이 추가로 필요하다.

## 관련 글

- [[2021-semantics-guided-indoorgml-reconstruction|Semantics-guided IndoorGML Reconstruction]] — 점군에서 IndoorGML navigation network까지
- [[2019-point-cloud-to-indoorgml-navigation-graph|Point Cloud → IndoorGML Navigation Graph]] — 문 검출 기반 공간 분할
- [[2022-hydra-3d-scene-graph|Hydra]] — 로봇 분야의 실시간 room 분할
