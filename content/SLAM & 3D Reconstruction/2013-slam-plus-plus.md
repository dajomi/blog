---
title: "SLAM++ — 객체 단위로 지도를 구성하는 Object-level SLAM (CVPR 2013)"
date: 2026-09-28
description: "깊이 카메라 기반 실시간 3D 객체 인식으로 카메라-객체 제약을 만들고, 객체 pose graph를 최적화해 점 대신 객체로 이루어진 SLAM 지도를 구축하는 SLAM++ 논문 리뷰"
category: "SLAM & 3D Reconstruction"
tags:
  - paper-review
  - slam
  - object-level-slam
  - rgb-d
  - pose-graph
aliases:
  - SLAM++
  - "SLAM++: Simultaneous Localisation and Mapping at the Level of Objects"
paper_title: "SLAM++: Simultaneous Localisation and Mapping at the Level of Objects"
authors:
  - Renato F. Salas-Moreno
  - Richard A. Newcombe
  - Hauke Strasdat
  - Paul H. J. Kelly
  - Andrew J. Davison
venue: "IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 1352–1359"
year: 2013
paper_type: conference
doi: "10.1109/CVPR.2013.178"
url: "https://openaccess.thecvf.com/content_cvpr_2013/html/Salas-Moreno_SLAM_Simultaneous_Localisation_2013_CVPR_paper.html"
verification: full-text
---

> [!info] 검증 범위
> 서지정보는 Crossref에서, 초록·방법·수치는 CVF Open Access 원문에서 확인했다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | SLAM++: Simultaneous Localisation and Mapping at the Level of Objects |
| 저자 | Renato F. Salas-Moreno, Richard A. Newcombe, Hauke Strasdat, Paul H. J. Kelly, Andrew J. Davison |
| 연도 | 2013 |
| 저널/학회 | IEEE CVPR 2013, pp. 1352–1359 |
| 연구 분야 | Object-level SLAM, 3D Object Recognition |
| 핵심 기술 | Depth Camera, Point Pair Features, Pose Graph Optimization |
| DOI | [10.1109/CVPR.2013.178](https://doi.org/10.1109/CVPR.2013.178) |
| 원문 | [CVF Open Access](https://openaccess.thecvf.com/content_cvpr_2013/html/Salas-Moreno_SLAM_Simultaneous_Localisation_2013_CVPR_paper.html) |
| 피인용 | 검색 기준 875회(브리핑 작성 시점), Crossref 기준 738회(2026-09 확인) |

## 1. 연구 배경

기존 SLAM 지도는 점(map point), 선, 면, 복셀 같은 저수준 기하 요소의 집합이다.

```text
기존 SLAM:
Map Point
Map Point
Map Point
...
```

SLAM++는 여기서 벗어나 `Chair / Table / Monitor ...`처럼 객체 수준 표현(object-level representation)을 SLAM 지도에 직접 넣으려는 대표 연구다.

저자들은 실내 장면이 반복적으로 등장하는 도메인 특화 객체와 구조로 이루어져 있다는 사전 지식에 주목한다. 이 지식을 SLAM 루프 안에서 적극 활용하는 "object oriented" 3D SLAM 패러다임을 제안한다.

## 2. 연구 Gap

**기존 연구의 한계**

- Dense surface reconstruction 기반 SLAM(KinectFusion 등)은 장면을 정밀하게 복원하지만, 표현이 방대하고 객체라는 의미 단위를 갖지 않는다.
- 점 단위 지도는 "무엇이 어디에 있는가"라는 로봇 상호작용에 필요한 기술(description)을 제공하지 못한다.

**본 연구가 해결하려는 Gap**

실시간 3D 객체 인식을 SLAM 루프에 넣어, 객체를 지도의 기본 단위로 삼는다. dense SLAM의 기술력과 예측력을 유지하면서 표현을 크게 압축한다.

## 3. 연구 질문

논문의 목적을 바탕으로 재구성하면 다음과 같다.

1. 사전에 알려진 반복 객체를 실시간으로 인식해 SLAM의 지도 단위로 사용할 수 있는가?
2. 객체 단위 지도가 dense 지도 대비 표현을 얼마나 압축하면서도 loop closure, relocalisation 같은 SLAM 기능을 유지하는가?

## 4. 핵심 기여

- 기존 방식: 점·면·복셀 중심의 dense 또는 sparse SLAM
- 문제: 표현이 크고, 객체 단위의 의미가 없다.
- 제안 방법: 깊이 카메라로 실시간 3D 객체 인식 → 카메라-객체 제약 생성 → 객체 graph를 pose-graph optimization으로 정제
- 개선점: dense surface reconstruction 수준의 기술·예측력을 유지하면서 표현을 크게 압축한다. 실시간 증분 매핑, loop closure 검출, relocalisation, 이동된 객체 식별을 시연했다.

## 5. 연구 방법론

### 연구 대상 / 데이터

- 센서: 손으로 들고 다니는 깊이 카메라(hand-held depth camera)
- 하드웨어: 게이밍 노트북, GPGPU 병렬 구현
- 실험 환경: 약 15×10×3m 크기의 대형 공용실에서 34개 객체 매핑, 약 10×6×3m 크기의 두 번째 방에서 35개 객체 매핑
- 대형 공용실 매핑에 약 10분 소요
- 시연된 객체 종류는 최대 5종

### 시스템 구조

```text
Depth Camera Frame
↓
Real-time 3D Object Recognition (Point Pair Features, GPU)
↓
Camera–Object 6DoF Constraints
↓
Object Pose Graph (카메라 pose + 객체 pose 노드)
  + 선택적 구조 prior (예: ground plane)
↓
Pose Graph Optimization (Levenberg–Marquardt, sparse Cholesky)
↓
Object-level Map
  - loop closure
  - relocalisation
  - 이동된 객체 식별
```

### 사용 기술

- Point Pair Features (PPF, Drost et al. 방식) — 두 개의 방향성 점 사이 상대 위치와 법선으로 만든 4차원 기술자. 160K개 PPF 처리에 일반적으로 5ms 미만
- GPU 병렬 객체 인식
- SE(3) pose graph, Levenberg–Marquardt 최적화, sparse Cholesky solver
- 사전 정의된 객체 CAD/스캔 모델 데이터베이스

### 평가 방법

- 프레임레이트
- 추적된 카메라 pose 수, 객체 수, graph edge 수
- 지도 메모리 크기와 KinectFusion 대비 압축률
- Loop closure, relocalisation, 이동 객체 식별의 정성적 시연

## 6. 핵심 결과

| 항목 | 값 |
|---|---|
| 프레임레이트 | 20 fps (실시간) |
| 추적된 카메라 pose | 132 |
| 객체 수 | 35 |
| Graph edge 수 | 338 |
| 객체 graph 메모리 | 350 KB |
| 동등한 KinectFusion 표현 | 1.4 GB |
| 대략적 압축률 | 약 1/70 |

- 객체 수준 표현으로 dense 표현 대비 메모리를 크게 줄였다.
- 실시간 증분 매핑, loop closure 검출, relocalisation, 이동된 객체 식별을 시연했다.
- 로봇 상호작용에 적합한 장면 기술(scene description)을 생성했다.

## 7. 결론 및 시사점

SLAM++는 SLAM 지도의 기본 단위를 "점"에서 "객체"로 올렸다. 지도 표현의 추상화 수준을 다음과 같이 구분할 때 가운데 단계를 대표한다.

```text
Point-level map
↓
Object-level semantic map
↓
Spatial / topological semantic map
```

- SLAM / 3D Reconstruction: 객체 중심 SLAM 연구의 기준점이다.
- Indoor Navigation: 객체 수준 지도만으로는 공간 간 연결관계가 표현되지 않는다. room, place, topology로 한 단계 더 추상화해야 한다.
- Digital Twin / BIM: 반복되는 표준 객체(가구, 설비)를 모델로 치환한다는 발상은 스캔 데이터를 객체 기반 모델로 변환하는 Scan-to-BIM과 구조적으로 닮았다.

## 8. 연구의 한계

### 저자가 명시한 한계

- 반복되는 동일 요소가 많은 공공 건물 내부 같은 환경에 특히 적합하다.
- 객체를 사전에 정의해야 한다.

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 데이터베이스에 없는 객체는 지도에 표현되지 않는다. 벽, 바닥 같은 구조 요소도 객체 모델 없이는 다루기 어렵다.
- 실험 객체 종류가 최대 5종 수준으로 제한적이다.
- 객체 인식의 정량 정확도(precision/recall)보다 시스템 동작 시연 위주의 평가다.

## 9. 비판적 읽기

### 연구 설계

- 강점: 실시간 시스템을 실제 환경에서 end-to-end로 시연했다.
- 약점: 방법 간 정량 비교 실험보다 시연 중심이다.
- 개선 방향: 객체 인식 정확도와 궤적 정확도의 정량 평가를 추가할 수 있다.

### 데이터

- 두 개의 실내 공간, 30여 개 객체로 규모가 제한적이다. 반복 객체가 많은 환경이 선택되었다.

### Baseline / 비교군

- 메모리 측면에서 KinectFusion과 비교했다. 궤적 정확도 등에서 다른 SLAM과의 비교는 제한적이다.

### 평가 지표

- 압축률과 프레임레이트는 "효율"을 보여주기에 적절하다. "정확도"를 보여주는 지표는 부족하다.

### 데이터 신뢰성

- 사전 모델이 있는 객체만 다루므로 인식 성능이 우호적인 조건에서 측정되었을 수 있다.

### 주장과 결과의 관계

- "dense SLAM의 기술·예측력을 유지한다"는 주장은 정성적 시연에 근거하는 비중이 크므로 일반화에는 주의가 필요하다.

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 확인 불가 | 확인 가능한 정보 없음 |
| 선택 편향 | 중간 | 반복 객체가 많은, 방법에 유리한 환경을 실험 공간으로 사용 |
| 확증 편향 | 중간 | 성공 사례 시연 중심(분석자 판단) |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 확인 불가 | 확인 가능한 정보 없음 |

## 11. 주요 전문 용어

### Object-level SLAM

지도의 기본 단위를 점·면이 아닌 인식된 객체로 삼는 SLAM이다. 각 객체의 종류와 6DoF pose를 지도에 저장한다.

### Point Pair Feature (PPF)

두 개의 방향성 점(위치 + 법선) 사이의 거리와 각도로 만든 기술자다. 3D 모델과 관측 점군을 매칭해 객체 pose를 추정할 때 쓰인다.

### Pose Graph Optimization

카메라나 객체의 pose를 노드, 관측으로 얻은 상대 제약을 edge로 두고, 전체 오차가 최소가 되도록 pose를 동시에 조정하는 최적화다.

### Relocalisation

추적을 잃은 뒤 기존 지도와 현재 관측을 대조해 카메라 위치를 다시 찾는 기능이다.

### KinectFusion

깊이 카메라 데이터를 TSDF 볼륨에 융합해 실시간으로 dense 표면을 복원하는 대표 시스템이다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

- Hand-held depth camera
- GPU 기반 Point Pair Feature 객체 인식
- SE(3) pose graph, Levenberg–Marquardt, sparse Cholesky solver

### 실무 구현 시 적용 가능한 기술

아래는 논문 구조를 현재 기술로 구현할 때 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**객체 인식 / pose 추정**
- 딥러닝 기반 6DoF pose estimation 모델
- Open3D, PCL (점군 정합)

**최적화**
- g2o, GTSAM, Ceres Solver

**데이터 관리**
- PostgreSQL + PostGIS (객체 위치·종류 저장)

**Visualization**
- Unity, Unreal Engine

## 13. 커리어 관점

### 공부해야 할 기술

- Pose graph와 비선형 최소제곱 최적화
- 3D 객체 인식과 점군 정합(ICP, PPF)
- SLAM 지도 표현 방식의 종류(점, 면, 복셀, 객체)

### 실무 연결

- 공장·물류 환경처럼 반복 설비가 많은 공간에서 설비 단위 지도를 만드는 작업
- 스캔 데이터에서 표준 객체를 인식해 라이브러리 모델로 치환하는 Scan-to-BIM 자동화
- 로봇 manipulation을 위한 객체 지도

### 기술 면접으로 연결될 수 있는 질문

- 점 기반 지도와 객체 기반 지도의 장단점은 무엇인가?
- Pose graph optimization에서 노드와 edge는 각각 무엇을 의미하는가?
- 객체 수준 지도가 메모리를 절약하는 원리는 무엇인가?
- 사전 정의된 객체 모델이 없는 환경에서는 어떻게 대응할 수 있는가?

## 14. 후속 연구

### 저자가 제안한 Future Work

- 형상 변이가 작은(low-dimensional shape variability) 객체로 확장
- 장기적으로는 스스로 객체 클래스를 분할·정의하는 시스템

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- 객체 지도에 room, place 계층을 추가해 공간 관계까지 표현
- Open-vocabulary 인식으로 사전 정의 객체 제약 완화
- 설비 객체 지도와 IoT 센서 데이터를 결합한 Digital Twin 구성

## 15. 논문 읽기 가이드

**1순위 — Figure 1과 시스템 개요**

객체 단위 지도가 어떻게 보이는지, 전체 파이프라인이 어떻게 구성되는지 파악한다.

**2순위 — 객체 인식과 graph 최적화 방법**

PPF 기반 인식과 카메라-객체 제약 구성 방식을 확인한다.

**3순위 — 시스템 통계 표**

압축률, 프레임레이트, graph 규모를 확인한다.

**4순위 — Conclusion**

사전 정의 객체의 한계와 향후 방향을 확인한다.

## 16. 핵심 정리

- SLAM 지도의 기본 단위를 점에서 객체로 올린 대표 연구다.
- 반복 객체라는 도메인 사전 지식을 SLAM 루프 안에서 활용한다.
- 객체 graph는 동등한 dense 표현 대비 약 1/70 크기로 압축된다.
- Point-level → Object-level → Spatial/topological 계층 중 가운데 단계를 이해하는 데 핵심이 되는 논문이다.

## 관련 글

- [[2017-semanticfusion|SemanticFusion]] — dense 지도에 semantic 라벨 융합
- [[2020-3d-dynamic-scene-graphs|3D Dynamic Scene Graphs]] — 객체 위에 place, room 계층 추가
