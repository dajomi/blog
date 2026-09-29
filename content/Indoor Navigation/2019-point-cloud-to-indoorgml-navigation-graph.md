---
title: "실내 점군에서 IndoorGML용 Navigation Graph 자동 추출 — 3D MAT 기반 문 검출 (ISPRS Annals 2019)"
date: 2026-09-28
description: "동적 레이저 스캐닝 점군에서 보행 가능 표면, 문, 방·복도, 경사로·계단을 자동으로 검출해 IndoorGML 구조를 지향하는 navigation graph를 생성한 Flikweert et al. 논문 리뷰"
category: "Indoor Navigation"
tags:
  - paper-review
  - indoorgml
  - navigation-graph
  - point-cloud
  - door-detection
  - mobile-laser-scanning
aliases:
  - Automatic Extraction of a Navigation Graph Intended for IndoorGML from an Indoor Point Cloud
  - Flikweert 2019
paper_title: "Automatic extraction of a navigation graph intended for IndoorGML from an indoor point cloud"
authors:
  - P. Flikweert
  - R. Peters
  - L. Díaz-Vilariño
  - R. Voûte
  - B. Staats
venue: "ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, IV-2/W5, 271–278"
year: 2019
paper_type: conference
doi: "10.5194/isprs-annals-IV-2-W5-271-2019"
url: "https://isprs-annals.copernicus.org/articles/IV-2-W5/271/2019/"
verification: full-text
---

> [!info] 검증 범위
> 서지정보, 초록, 원문 전문은 Copernicus(ISPRS Annals) 공식 페이지에서 확인했다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | Automatic Extraction of a Navigation Graph Intended for IndoorGML from an Indoor Point Cloud |
| 저자 | P. Flikweert, R. Peters, L. Díaz-Vilariño, R. Voûte, B. Staats |
| 연도 | 2019 |
| 저널/학회 | ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, IV-2/W5, pp. 271–278 |
| 연구 분야 | Indoor Navigation, IndoorGML, Point Cloud Processing |
| 핵심 기술 | Mobile Laser Scanning, 3D Medial Axis Transform, Scanner Trajectory, Region Growing |
| DOI | [10.5194/isprs-annals-IV-2-W5-271-2019](https://doi.org/10.5194/isprs-annals-IV-2-W5-271-2019) |
| 원문 | [ISPRS Annals (Open Access)](https://isprs-annals.copernicus.org/articles/IV-2-W5/271/2019/) |
| 피인용 | Crossref 기준 약 4회(브리핑 작성 시점) |

## 1. 연구 배경

제목 그대로, 실내 점군에서 IndoorGML용 navigation graph를 자동으로 추출하는 연구다.

저자들은 공공에 개방된 건물일수록 실내 환경이 복잡하고 사람이 많아진다는 점에서 출발한다. 그에 따라 사람들이 어디에 있는지, 어떻게 이동하는지, 어떻게 도달할 수 있는지를 알아야 할 필요가 커진다. 그런데 도면은 최신 상태가 아닐 수 있어 지도와 경로의 근거로 신뢰하기 어렵다. 그래서 이 연구는 건물을 동적 레이저 스캐닝(dynamic laser scanning)해 얻은 점군을 입력으로 쓴다.

논문이 다루는 문제는 "도면에 의존할 수 없으므로, 점군에서 빠르고 자동으로 IndoorGML 구조의 navigation graph를 만들겠다"는 것이다. 즉 "IndoorGML 전문가가 따로 모델링하지 말고 스캔 결과에서 자동으로 만들자"는 문제가 2019년에 이미 정확히 연구되었다.

## 2. 연구 Gap

**기존 연구의 한계**

- 실내 navigation 모델은 주로 도면 기반으로 만들어지는데, 도면이 오래되었거나 실제와 다를 수 있다.
- IndoorGML 모델을 사람이 직접 구축하면 시간과 비용이 많이 든다.

**본 연구가 해결하려는 Gap**

도면 없이 모바일 레이저 스캐너 점군과 스캐너 이동 궤적만으로, 보행 가능 표면의 유형을 유지한 채 IndoorGML 구조의 navigation graph를 빠르고 자동으로 생성한다. 특히 공간을 연결하고 경로상 논리적 단계가 되는 문(door) 검출에 초점을 둔다.

## 3. 연구 질문

논문의 목적을 바탕으로 재구성하면 다음과 같다.

1. 도면 없이 실내 점군만으로 IndoorGML 구조를 따르는 navigation graph를 자동 생성할 수 있는가?
2. 3D Medial Axis Transform과 스캐너 궤적 정보를 결합해 문을 검출할 수 있는가?
3. 방·복도 구분과 경사로·계단 검출을 같은 파이프라인에 통합할 수 있는가?

## 4. 핵심 기여

- 기존 방식: 도면 기반 또는 수작업 IndoorGML 모델링
- 문제: 도면이 최신이 아니고, 수작업 비용이 크다.
- 제안 방법: 보행 가능 표면 검출 → 3D MAT와 스캐너 궤적을 결합한 문 검출 → 문을 경계로 한 공간 분할 → 경사로·계단 검출 → navigation graph
- 개선점: 도면 없이 점군에서 공간 연결 그래프를 자동 생성하며, 첫 결과에서 걸어서 통과한 문을 모두 검출했다.

## 5. 연구 방법론

### 연구 대상 / 데이터

- 대학 학부 건물 일부를 ZEB-REVO 모바일 레이저 스캐너로 수집한 점군
- 대상 영역: 복도와 몇 개의 방, 인접한 방으로 이어지는 계단, 여러 층을 잇는 대형 계단이 가운데 있는 넓은 홀
- 총 점 개수와 공간 크기는 논문에 제시되지 않았다.

### 시스템 구조

```text
Indoor Point Cloud (dynamic laser scanning) + Scanner Trajectory
↓
Walkable Surface Detection
  - 점군과 궤적을 복셀화
  - region growing(8-이웃 연결)으로 수평면, 계단, 경사로, 기타 요소 분류
  - Staats et al.(2018)의 선행 연구 기반
↓
Door Detection (3D MAT + 스캐너 궤적)
  - 3D Medial Axis Transform sheet 중 벽 내부에 형성된 sheet만 필터링
    (분리 각도 θ > 0.8π rad, 반지름 < 0.4 m, 법선 z성분 < 0.2, 점 1000개 초과)
  - 궤적 양쪽에 벽 sheet가 있고 방위각 쌍이 180°에 가까운 위치를 문으로 판단
↓
Room / Corridor Identification
  - 문틀 내부 복셀을 제거한 뒤 region growing → 바닥이 방 단위로 분리
↓
Slope / Stair Detection
  - 보행 표면 분류 단계에서 검출, 위·아래 끝점에 노드 배치
↓
Navigation Graph (Connectivity Node-Relation Graph)
↓
IndoorGML 구조로 저장 가능
```

### 사용 기술

- ZEB-REVO 모바일 레이저 스캐너
- 복셀화, region growing
- 3D Medial Axis Transform
- 스캐너 이동 궤적 정보 활용
- IndoorGML Node-Relation Graph(NRG) 개념

### 평가 방법

- 검출된 문 수, 오검출 수
- 공간 분리 성공 여부
- Precision, recall, F-score 같은 정량 지표는 보고되지 않았다.

## 6. 핵심 결과

- 대상 영역의 문은 총 13개이며, 스캔 중 실제로 통과한 문은 그중 7개다.
- 걸어서 통과한 7개 문은 오검출 없이 모두 검출되었다.
- 검출된 7개 문 중 1개는 실내 공간을 두 개로 분리하지 못했다. 즉 7개 중 6개 문에서 공간 분리에 성공했다.
- 방문한 모든 영역에 개별 식별자가 부여되어 connectivity graph가 생성되었다.

## 7. 결론 및 시사점

저자들은 3D MAT와 모바일 스캐너 궤적의 정보를 결합한 문 검출이 좋은 첫 결과를 보였다고 평가한다. 방·복도 식별과 경사로·계단 검출을 거쳐 IndoorGML 구조로 저장할 수 있는 navigation graph를 얻었다.

다만 논문에서 생성한 것은 IndoorGML Connectivity NRG를 지향하는 그래프이며, 실제 IndoorGML 형식으로 내보내거나 표준 적합성을 검증한 과정은 서술되지 않았다. 저자들은 이 결과를 IndoorGML Connectivity 및 Accessibility NRG의 입력으로 쓰는 작업을 진행 중이라고 밝힌다.

- Indoor GIS / IndoorGML: "사람이 IndoorGML을 작성하는 대신 스캔 결과에서 자동 생성한다"는 방향의 초기 peer-reviewed 연구다. prior art 관점에서 매우 중요하다.
- SLAM: 모바일 스캐너 궤적 자체를 공간 해석의 단서로 사용한다는 점이 특징이다. SLAM 궤적은 지도 작성의 부산물이 아니라 공간 구조 추론의 입력이 될 수 있다.
- Digital Twin: 도면이 없거나 낡은 기존 건물의 navigation 모델을 빠르게 구축하는 데 활용할 수 있다.

## 8. 연구의 한계

### 저자가 명시한 한계

- 걸어서 통과한 문만 검출할 수 있다. 통과하지 않은 6개 문은 검출되지 않았다.
- Sheet 필터링 파라미터는 스캔한 실내 환경의 유형에 따라 달라질 수 있다.
- 결과 그래프는 각 공간에 노드가 하나뿐이어서 복도나 넓은 공간의 경로가 실제 이동 경로를 잘 대표하지 못한다.
- 한쪽 면만 스캔된 벽은 검출할 수 없다.

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 단일 건물 일부에서의 첫 결과로 표본이 작다.
- 정량 지표(precision, recall)가 없어 다른 방법과 비교하기 어렵다.
- 실제 IndoorGML 파일 생성과 표준 검증이 포함되지 않아, 제목의 "intended for IndoorGML"이 의미하는 수준을 정확히 이해해야 한다.

## 9. 비판적 읽기

### 연구 설계

- 강점: 스캐너 궤적을 문 검출 단서로 쓰는 발상이 명확하고, 전체 파이프라인을 끝까지 연결했다.
- 약점: 검증이 단일 사례의 정성 평가 위주다.
- 개선 방향: 여러 건물에서 precision/recall을 측정할 필요가 있다.

### 데이터

- 대학 건물 일부 한 곳의 데이터다. 대표성이 제한적이다.

### Baseline / 비교군

- 다른 문 검출 방법과의 비교가 없다.

### 평가 지표

- 문 검출 수와 공간 분리 성공 여부만 보고했다. 연구 목표(navigation graph 생성)를 평가하려면 그래프의 정확도나 경로 품질 지표가 필요하다.

### 데이터 신뢰성

- 모바일 레이저 스캐너 데이터로 기하 품질은 양호할 것으로 보인다. 궤적에 의존하는 방법 특성상 스캔 경로 설계가 결과를 좌우한다.

### 주장과 결과의 관계

- "좋은 첫 결과"라는 저자의 표현은 적절히 절제되어 있다. 다만 통과한 문 100% 검출이라는 결과를 일반적인 문 검출 성능으로 확대 해석하면 안 된다.

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 확인 불가 | 확인 가능한 정보 없음 |
| 선택 편향 | 중간 | 단일 건물 일부만 대상으로 했고, 평가 대상 문이 걸어서 통과한 문으로 한정됨 |
| 확증 편향 | 낮음 | 검출하지 못한 문과 실패 사례(공간 미분리)를 함께 보고 |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 중간 | 유럽 대학 건물 한 곳. 다른 건축 양식에서는 파라미터 조정이 필요할 수 있음 |

## 11. 주요 전문 용어

### IndoorGML

OGC가 제정한 실내 공간정보 표준이다. 실내 공간을 셀(CellSpace)로 나누고, 셀 간 연결관계를 그래프(State–Transition)로 표현해 실내 navigation을 지원한다.

### Node-Relation Graph (NRG)

IndoorGML에서 공간 셀을 노드로, 공간 간 인접·연결·접근 관계를 edge로 표현하는 그래프다. Connectivity NRG는 문 등을 통해 실제로 이동 가능한 연결을 나타낸다.

### Medial Axis Transform (MAT)

형상 내부에서 경계까지의 거리가 같은 점들의 골격(medial axis)과 그 거리로 형상을 표현하는 방법이다. 3D에서는 sheet 형태로 나타나며, 벽 두께 안에 생기는 sheet를 이용해 벽을 찾을 수 있다.

### Mobile / Dynamic Laser Scanning

사람이 들고 다니거나 차량·로봇에 탑재한 레이저 스캐너로 이동하면서 점군을 수집하는 방식이다. 스캐너의 이동 궤적도 함께 기록된다.

### Region Growing

씨앗 점에서 시작해 조건(연결성, 평면성 등)을 만족하는 이웃을 반복적으로 붙여 영역을 확장하는 분할 방법이다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

- ZEB-REVO 모바일 레이저 스캐너, 스캐너 궤적
- 복셀화, region growing
- 3D Medial Axis Transform
- IndoorGML NRG 개념(실제 파일 export는 미포함)

### 실무 구현 시 적용 가능한 기술

아래는 서비스 구현 시 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**Point Cloud**
- PDAL, Open3D, CloudCompare

**Spatial DB / 경로**
- PostgreSQL + PostGIS + pgRouting (navigation graph 저장·경로 탐색)

**표준**
- IndoorGML 1.1 / 2.0 인코딩, IndoorGML 검증 도구

**Visualization**
- QGIS, Cesium

## 13. 커리어 관점

### 공부해야 할 기술

- IndoorGML 구조(CellSpace, State, Transition, NRG, Multi-layered space)
- Point cloud 복셀화와 분할
- 모바일 레이저 스캐닝과 SLAM 궤적의 의미
- 그래프 기반 경로 탐색

### 실무 연결

- 실내 공간정보 구축 사업에서 스캔 데이터 기반 navigation network 자동화
- 공공시설 재난 대피 경로 모델링
- 도면이 없는 기존 건물의 실내 지도 제작

### 기술 면접으로 연결될 수 있는 질문

- IndoorGML에서 CellSpace와 State, Transition의 관계는 무엇인가?
- 점군에서 문을 검출하는 것이 navigation graph 생성에 중요한 이유는 무엇인가?
- 스캐너 궤적을 공간 해석에 활용할 때의 장점과 한계는 무엇인가?
- 공간마다 노드를 하나만 두면 어떤 경로 문제가 생기고, subspacing은 이를 어떻게 해결하는가?

## 14. 후속 연구

### 저자가 제안한 Future Work

- 대각선 연결을 막도록 벽 sheet 복셀 주변에 buffer를 두어 8-분리 보장
- 복도와 넓은 공간을 하위 공간으로 나누는 subspacing으로 경로 현실성 향상
- IndoorGML Connectivity 및 Accessibility NRG의 정식 생성(진행 중이라고 언급)

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- 딥러닝 기반 문 검출로 통과하지 않은 문까지 검출
- 결과 그래프를 실제 IndoorGML 문서로 export하고 표준 적합성 검증
- SLAM 실시간 출력에 적용하는 증분형 navigation graph 생성

## 15. 논문 읽기 가이드

**1순위 — 방법론 개요 Figure**

보행 표면 → 문 검출 → 공간 분할 → 그래프 생성 흐름을 파악한다.

**2순위 — 3D MAT 기반 문 검출**

벽 sheet 필터링 조건과 궤적 기반 판정 방식을 이해한다.

**3순위 — 결과**

13개 문 중 7개 통과, 7개 검출, 1개 공간 미분리 결과를 확인한다.

**4순위 — Discussion / Future Work**

통과하지 않은 문 문제, subspacing 필요성, IndoorGML NRG 생성 계획을 확인한다.

## 16. 핵심 정리

- 도면 대신 모바일 레이저 스캔 점군과 스캐너 궤적으로 실내 navigation graph를 자동 생성한다.
- 문은 공간을 연결하는 핵심 요소이며, 3D MAT와 궤적 정보를 결합해 검출한다.
- 걸어서 통과한 7개 문을 모두 검출했지만, 통과하지 않은 문은 검출하지 못하고 정량 지표도 제한적이다.
- "IndoorGML을 사람이 작성하지 않고 스캔 결과에서 자동 생성한다"는 문제는 2019년에 이미 연구된 prior art다.

## 관련 글

- [[2021-semantics-guided-indoorgml-reconstruction|Semantics-guided IndoorGML Reconstruction]] — semantic 해석을 결합한 발전된 버전
- [[2022-hydra-3d-scene-graph|Hydra]] — 로봇 분야의 실시간 room·topology 추출
- [[2011-hybrid-metric-topological-navigation|Navigation in Hybrid Metric-Topological Maps]] — topology 기반 navigation의 역할
