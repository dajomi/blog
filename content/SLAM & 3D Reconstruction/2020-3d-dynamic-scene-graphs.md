---
title: "3D Dynamic Scene Graphs — 객체·장소·방·사람을 계층 그래프로 표현하는 Actionable Spatial Perception (RSS 2020)"
date: 2026-09-28
description: "Visual-inertial 데이터로부터 mesh, 객체·에이전트, 장소·구조물, 방, 건물의 5계층 3D Dynamic Scene Graph를 자동 구축하는 Spatial Perception Engine(SPIN)을 제안한 논문 리뷰"
category: "SLAM & 3D Reconstruction"
tags:
  - paper-review
  - 3d-scene-graph
  - spatial-perception
  - visual-inertial-slam
  - topological-map
aliases:
  - 3D Dynamic Scene Graphs
  - DSG
  - "3D Dynamic Scene Graphs: Actionable Spatial Perception with Places, Objects, and Humans"
paper_title: "3D Dynamic Scene Graphs: Actionable Spatial Perception with Places, Objects, and Humans"
authors:
  - Antoni Rosinol
  - Arjun Gupta
  - Marcus Abate
  - Jingnan Shi
  - Luca Carlone
venue: "Robotics: Science and Systems (RSS) XVI"
year: 2020
paper_type: conference
doi: "10.15607/RSS.2020.XVI.079"
url: "https://arxiv.org/abs/2002.06289"
verification: full-text
---

> [!info] 검증 범위
> 서지정보는 RSS 공식 프로그램 페이지와 RSS 온라인 proceedings에서, 초록·방법·수치는 arXiv 원문(2002.06289)에서 확인했다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | 3D Dynamic Scene Graphs: Actionable Spatial Perception with Places, Objects, and Humans |
| 저자 | Antoni Rosinol, Arjun Gupta, Marcus Abate, Jingnan Shi, Luca Carlone |
| 연도 | 2020 |
| 저널/학회 | Robotics: Science and Systems (RSS) 2020 |
| 연구 분야 | Spatial Perception, 3D Scene Graph, Visual-Inertial SLAM |
| 핵심 기술 | Kimera-VIO, ESDF 기반 Places 추출, Room Segmentation, Human Mesh Tracking |
| DOI | [10.15607/RSS.2020.XVI.079](https://doi.org/10.15607/RSS.2020.XVI.079) |
| 원문 | [arXiv:2002.06289](https://arxiv.org/abs/2002.06289) |
| 피인용 | 한 검색 인덱스 기준 약 150회(브리핑 작성 시점). 데이터베이스마다 차이가 있다. |

## 1. 연구 배경

이 논문은 단순한 semantic segmentation 수준을 넘어선다. SLAM 결과에서 공간을 자동으로 이해하고, semantic·topological abstraction을 거쳐 의사결정에 쓰는 흐름의 상당 부분을 이미 구현한다.

저자들은 "actionable spatial perception"을 위한 통합 표현으로 3D Dynamic Scene Graph(DSG)를 제안한다. Scene graph는 장면의 개체(객체, 벽, 방)를 노드로, 개체 간 관계(포함, 인접)를 edge로 표현하는 방향 그래프다. DSG는 이 개념을 움직이는 에이전트(사람, 로봇)가 있는 동적 장면으로 확장한다. 또한 planning과 decision-making을 지원하는 정보(시공간 관계, 여러 추상화 수준의 topology)를 포함한다.

저자들은 이를 명시적으로 planning과 decision-making을 위한 actionable spatial representation이라고 정의한다.

## 2. 연구 Gap

**기존 연구의 한계**

- 기존 로봇 지도는 metric map, semantic map, 객체 지도 등으로 파편화되어 있다. 여러 추상화 수준과 동적 에이전트를 하나의 표현으로 통합하지 못했다.
- 기존 scene graph 연구는 주로 이미지 단위이거나 정적 장면에 한정되었다.

**본 연구가 해결하려는 Gap**

Visual-inertial 데이터에서 metric-semantic mesh부터 객체, 사람, 장소, 방, 건물까지 계층적 그래프를 완전 자동으로 구축하는 첫 end-to-end 시스템(SPIN)을 제시한다. 저자들은 visual-inertial SLAM과 dense human mesh tracking을 조화시킨 첫 연구라고 설명한다.

## 3. 연구 질문

논문의 기여를 바탕으로 재구성하면 다음과 같다.

1. 동적 장면의 metric, semantic, topological 정보를 하나의 계층 그래프로 통합 표현할 수 있는가?
2. 이 그래프를 visual-inertial 센서 데이터로부터 사람 개입 없이 자동 구축할 수 있는가?
3. 사람이 많은(crowded) 환경에서도 이 구축 과정이 견고하게 동작하는가?

## 4. 핵심 기여

저자가 제시한 기여는 세 가지다.

- 표현: 3D Dynamic Scene Graph라는 통합 표현
- 시스템: DSG를 visual-inertial 데이터에서 구축하는 첫 end-to-end 완전 자동 Spatial PerceptIon eNgine(SPIN)
- 검증: 사진 수준의 Unity 기반 시뮬레이터에서 SPIN의 견고성과 표현력을 평가

기존 방식 → 문제 → 제안 → 개선 관계로 정리하면 다음과 같다.

- 기존 방식: metric-semantic map 또는 객체 지도 단독 사용
- 문제: 장소·방·건물 같은 상위 개념과 사람의 움직임이 빠져 있어 planning에 필요한 구조적 정보가 없다.
- 제안: 객체·사람·로봇 노드를 견고하게 추정하고, 장소·구조물·방과 그 관계를 계층적으로 자동 추출한다.
- 개선: 로봇이 "사람이 어느 방에 있는가", "이 방은 어느 방과 연결되는가" 같은 질의를 할 수 있는 표현을 얻는다.

## 5. 연구 방법론

### 연구 대상 / 데이터

- 사진 수준의 Unity 기반 시뮬레이터, 65m × 65m 규모 환경, panoptic semantic segmentation 제공
- 공개 데이터셋 uHumans
  - uH_01: 사람 12명
  - uH_02: 사람 24명
  - uH_03: 사람 60명
- VIO 비교용 EuRoC 시퀀스

### 시스템 구조

DSG의 5개 계층(단층 실내 환경 기준)은 다음과 같다.

```text
Layer 5  Building           건물 노드 하나
Layer 4  Rooms              방, 복도, 홀과 인접 관계
Layer 3  Places & Structures 자유 공간 위치(places)와 벽·바닥·천장 등 구조물
Layer 2  Objects & Agents    정적 객체와 동적 에이전트(사람, 로봇)
Layer 1  Metric-Semantic Mesh semantic 라벨이 붙은 3D mesh
```

관계 예시는 다음과 같다.

```text
object ∈ room
room ↔ room
place ↔ place
agent ∈ room
```

SPIN의 처리 흐름은 다음과 같다.

```text
Visual-Inertial Data
↓
Kimera-VIO (IMU preintegration, fixed-lag smoothing)
  + 사람이 많은 장면용 IMU-aware optical flow, 2-point RANSAC
↓
Kimera-RPGO (pose graph optimization)
↓
Metric-Semantic Mesh (사람 영역은 dynamic masking으로 제외)
↓
Objects & Agents
  - 형상을 모르는 객체: Euclidean clustering
  - 형상을 아는 객체: TEASER++로 CAD 모델 정합
  - 사람: Graph-CNN(Kolotouros et al.)으로 SMPL mesh 추정 + pose graph 추적
↓
Places (ESDF 기반 topological graph)
↓
Rooms (천장 아래 0.3m 높이의 2D ESDF 단면으로 방 분할, 다수결로 place→room 할당)
↓
Building
↓
3D Dynamic Scene Graph
```

### 사용 기술

- Kimera-VIO, Kimera-RPGO
- Metric-semantic mesh 재구성
- Euclidean clustering, TEASER++ 기반 CAD 정합
- Graph-CNN 기반 human mesh(SMPL) 추정, zero-velocity prior를 둔 pose graph 추적
- ESDF 기반 places 추출, 2D ESDF 단면 기반 room 분할

### 평가 방법

- VIO 궤적 오차(cm)
- Mesh 정확도(RMSE, m)
- 사람·객체 위치 오차(m)
- Room parsing precision / recall

## 6. 핵심 결과

**VIO 궤적 오차 (cm)**

| 시퀀스 | 5-point | 2-point | DVIO |
|---|---|---|---|
| uH_01 | 92 | 78 | 59 |
| uH_02 | 145 | 79 | 78 |
| uH_03 | 160 | 111 | 88 |

사람이 많아질수록 기본 5-point 방식의 오차가 커지며, 제안한 동적 장면 대응(DVIO)이 가장 낮은 오차를 보였다.

**Mesh 정확도 (RMSE, m)** — dynamic masking(DM) 적용 여부 비교

| 시퀀스 | GT pose, DM 없음 | GT pose, DM 적용 | DVIO, DM 없음 | DVIO, DM 적용 |
|---|---|---|---|---|
| uH_01 | 0.089 | 0.060 | 0.227 | 0.227 |
| uH_02 | 0.133 | 0.061 | 0.347 | 0.301 |
| uH_03 | 0.192 | 0.061 | 0.351 | 0.335 |

**사람·객체 위치 오차 (m)**

| 시퀀스 | 사람: 단일 이미지 | 사람: 필터링 | 사람: 추적 | 형상 모르는 객체 | 형상 아는 객체 |
|---|---|---|---|---|---|
| uH_01 | 1.07 | 0.88 | 0.65 | 1.31 | 0.20 |
| uH_02 | 1.09 | 0.78 | 0.61 | 1.70 | 0.35 |
| uH_03 | 1.20 | 0.97 | 0.63 | 1.51 | 0.38 |

**Room parsing (uH_01)**

- 평균 precision 99.89%, 평균 recall 99.84%

## 7. 결론 및 시사점

저자들은 DSG가 planning과 decision-making, 사람-로봇 상호작용, 장기 자율성, 장면 예측에 큰 영향을 줄 수 있다고 본다.

이 논문은 SLAM에서 공간을 자동으로 이해하고 semantic·topological abstraction을 거쳐 의사결정으로 가는 흐름을 이미 상당 부분 구현했다. 3DGS나 IndoorGML과 결합하는 연구를 구상할 때 가장 먼저 확인해야 하는 선행연구다.

- SLAM / 3D Reconstruction: SLAM 결과를 "지도"에서 "공간 이해"로 끌어올리는 spatial perception 연구 흐름의 출발점이다.
- Indoor GIS / IndoorGML: Room–Place–Object 계층과 인접 관계는 IndoorGML의 CellSpace–State–Transition 구조와 개념적으로 매우 가깝다. 다만 데이터 모델과 표준화 목적은 다르다.
- Digital Twin: 사람과 로봇 같은 동적 에이전트까지 공간 구조 안에 넣는다는 점에서 운영형 Digital Twin의 공간 모델 설계에 참고가 된다.

## 8. 연구의 한계

### 저자가 명시한 한계

저자는 Discussion에서 향후 과제 형태로 다음을 언급한다.

- 제시한 여러 질의 기능은 아직 해결되지 않은 연구 문제를 포함한다.
- 재질이나 affordance 같은 노드 속성의 추론은 향후 과제다.
- DSG를 증분적·실시간으로 추정하는 것은 향후 과제다(이 논문의 구축은 실시간이 아니다).

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 평가가 사진 수준 시뮬레이터 중심이다. 실제 건물 데이터에서의 성능은 이 논문만으로 판단하기 어렵다.
- 방 분할이 천장 아래 수평 2D 단면에 기반하므로 단층·직교형 공간에 유리하다. 개방형 평면이나 복층 공간에서는 한계가 예상된다.
- Room parsing 결과가 한 시퀀스(uH_01)에 대해서만 제시되었다.
- 방 노드에 "사무실", "회의실" 같은 기능 라벨이 자동으로 붙는지는 별도 확인이 필요하다.

## 9. 비판적 읽기

### 연구 설계

- 강점: 표현 정의 → 구축 엔진 → 시뮬레이션 검증으로 이어지는 구성이 명확하다.
- 약점: 실제 환경 실험이 부족하다.
- 개선 방향: 실제 건물 데이터에서 계층별 정확도를 평가해야 한다.

### 데이터

- 강점: 사람 수를 12/24/60명으로 늘려 동적 환경 난이도를 체계적으로 조절했다.
- 약점: 단일 시뮬레이션 환경이다.

### Baseline / 비교군

- VIO는 5-point, 2-point 방식과 비교했다. DSG 전체를 다른 시스템과 비교하지는 않았다(비교 대상 시스템이 거의 없던 시점이다).

### 평가 지표

- 계층별 지표(궤적, mesh, 위치, room)가 제시되어 있다. "DSG가 planning에 얼마나 도움이 되는가"를 보여주는 과업 수준 지표는 없다.

### 데이터 신뢰성

- 시뮬레이터는 ground truth가 정확하다는 장점이 있다. 반면 실제 센서 잡음과 조명 변화는 반영이 제한된다.

### 주장과 결과의 관계

- "planning과 decision-making에 큰 영향을 줄 수 있다"는 주장은 전망에 가깝다. 이 논문의 결과로 직접 검증된 것은 아니다.

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 확인 불가 | 확인 가능한 정보 없음 |
| 선택 편향 | 중간 | 저자가 만든 시뮬레이션 환경에서 평가 |
| 확증 편향 | 중간 | Room parsing 결과가 단일 시퀀스에 대해서만 제시됨 |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 확인 불가 | 확인 가능한 정보 없음 |

## 11. 주요 전문 용어

### 3D Scene Graph

3D 장면의 개체를 노드로, 개체 간 관계를 edge로 표현한 그래프다. 여러 추상화 수준(객체, 방, 건물)을 계층으로 가질 수 있다.

### Dynamic Scene Graph (DSG)

Scene graph에 움직이는 에이전트(사람, 로봇)와 시공간 관계를 추가한 표현이다.

### ESDF (Euclidean Signed Distance Field)

공간의 각 지점에서 가장 가까운 장애물까지의 거리를 저장한 필드다. 자유 공간의 구조를 파악하고 places를 추출하는 데 쓰인다.

### Places

로봇이 이동할 수 있는 자유 공간을 대표하는 점들과 그 연결로 이루어진 topological graph다.

### Visual-Inertial Odometry (VIO)

카메라 영상과 IMU(가속도계, 자이로) 데이터를 함께 사용해 센서의 움직임을 추정하는 기법이다.

### SMPL

사람의 자세와 체형을 소수의 파라미터로 표현하는 대표적인 인체 mesh 모델이다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

- Kimera-VIO, Kimera-RPGO
- Metric-semantic mesh, dynamic masking
- Euclidean clustering, TEASER++
- Graph-CNN 기반 SMPL 추정
- ESDF 기반 places 및 room 분할
- Unity 기반 시뮬레이터

### 실무 구현 시 적용 가능한 기술

아래는 논문 구조를 서비스로 구현할 때 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**Robotics**
- ROS 2, Kimera / Hydra 오픈소스

**Graph 저장·질의**
- Neo4j 같은 그래프 DB
- PostgreSQL + PostGIS (공간 질의), pgRouting (경로 탐색)

**표준 변환**
- IndoorGML (CellSpace, State, Transition)으로 room·place 그래프 내보내기

**Visualization**
- Unity, Unreal Engine, Cesium

## 13. 커리어 관점

### 공부해야 할 기술

- Visual-inertial SLAM의 원리
- ESDF와 topological map 추출
- 그래프 자료구조와 그래프 알고리즘
- IndoorGML의 공간 모델(CellSpace, NRG)과 scene graph의 비교

### 실무 연결

- 실내 로봇·드론의 공간 이해 모듈
- 스마트 빌딩에서 재실자 위치와 공간 구조를 결합한 서비스
- 실내 Digital Twin의 공간 계층 모델 설계

### 기술 면접으로 연결될 수 있는 질문

- Metric map, semantic map, topological map, scene graph의 차이는 무엇인가?
- 3D scene graph와 IndoorGML은 어떤 점에서 비슷하고 어떤 점에서 다른가?
- ESDF에서 방을 분할하는 방법의 한계는 무엇인가?
- 사람이 많은 환경에서 VIO가 어려운 이유와 대응 방법은 무엇인가?

## 14. 후속 연구

### 저자가 제안한 Future Work

- 재질, affordance 같은 노드 속성을 데이터에서 추론
- Scene graph를 증분적·실시간으로 추정
- 여러 로봇이 수집한 데이터로 DSG를 추정하는 분산 SPIN
- 실외 환경과 새로운 노드 유형으로 확장

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- DSG의 room·place 계층을 IndoorGML 호환 navigation model로 자동 변환
- 실제 건물(복층, 개방형 평면)에서의 room 분할 성능 검증
- 3DGS 기반 지도를 하위 계층으로 사용하는 scene graph

## 15. 논문 읽기 가이드

**1순위 — DSG 계층 Figure**

5개 계층과 노드·edge 정의를 먼저 이해한다.

**2순위 — SPIN 구성**

VIO, mesh, 사람·객체 추정, places·rooms 추출이 어떻게 연결되는지 확인한다.

**3순위 — 실험 결과 표**

동적 환경에서 VIO와 mesh 성능이 어떻게 달라지는지 확인한다.

**4순위 — Discussion (질의와 응용)**

DSG로 어떤 질의가 가능한지, 무엇이 아직 연구 과제인지 확인한다.

## 16. 핵심 정리

- 3D scene graph는 metric에서 building까지 여러 추상화 계층을 하나의 그래프로 통합한다.
- DSG는 사람과 로봇 같은 동적 에이전트까지 공간 구조 안에 포함한다.
- Places(자유 공간 topology)와 rooms를 센서 데이터에서 자동 추출할 수 있음을 보였다.
- "SLAM → 공간 자동 이해 → semantic/topological abstraction → 의사결정" 흐름을 이미 상당 부분 구현한 핵심 선행연구다.

## 관련 글

- [[2021-kimera|Kimera]] — DSG 구축 파이프라인을 실제 데이터와 path planning까지 확장
- [[2022-hydra-3d-scene-graph|Hydra]] — scene graph의 실시간·증분 구축
- [[2008-conceptual-spatial-representations|Conceptual Spatial Representations]] — 계층적 공간 표현의 선행 사고
