---
title: "IndoorGML 기반 다중 3DGS 장면 간 실내 Navigation — TU Delft 석사논문 (2026)"
date: 2026-09-28
description: "방별로 독립 생성한 3D Gaussian Splatting 장면을 공통 좌표계로 정렬하고, IndoorGML의 Cell–Node–Edge topology를 PostGIS에 저장해 방 사이 이동을 제어하는 웹 viewer를 구현한 TU Delft 석사논문 리뷰"
category: "Indoor Navigation"
tags:
  - paper-review
  - indoorgml
  - 3d-gaussian-splatting
  - postgis
  - web-viewer
  - master-thesis
aliases:
  - IndoorGML-Constrained Navigation Across Multiple 3DGS Scenes
  - Teo 2026
paper_title: "IndoorGML-Constrained Navigation Across Multiple 3D Gaussian Splatting Scenes for Indoor Environments"
authors:
  - Mingjie Teo
venue: "TU Delft, MSc Geomatics (석사학위논문)"
year: 2026
paper_type: thesis
doi: ""
url: ""
verification: unverified
draft: true
---

> [!warning] 검증 범위
> TU Delft Geomatics의 2025년 9월 착수 논문 목록에서 저자(Teo Mingjie), 지도교수(Edward Verbree, Martijn Meijers), 연구 주제(IndoorGML을 topology 기반으로 사용해 여러 3DGS 실내 장면 사이를 이동하는 viewer)를 확인했다. 이 목록에 적힌 제목은 착수 당시 가제인 "A Topology-Aware Multi-3DGS Viewer"다.
>
> 최종 제목, 2026년 6월 제출 여부, TU Delft Repository의 원문 링크는 이번 작업에서 확인하지 못했다. 본문의 방법론 설명은 기존 브리핑에 근거하며, 원문 확인 전까지 사실로 단정하지 않는다.
>
> 이 연구는 peer-reviewed 논문이 아니라 석사학위논문이다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | IndoorGML-Constrained Navigation Across Multiple 3D Gaussian Splatting Scenes for Indoor Environments (브리핑 기준, 원문 미확인) |
| 착수 시 가제 | A Topology-Aware Multi-3DGS Viewer |
| 저자 | Mingjie Teo |
| 지도교수 | Edward Verbree, Martijn Meijers |
| 연도 | 2026 (브리핑 기준 2026년 6월 제출) |
| 저널/학회 | TU Delft MSc Geomatics 석사학위논문 |
| 연구 분야 | Indoor Navigation, 3D Gaussian Splatting, IndoorGML |
| 핵심 기술 | 3DGS, SfM, Umeyama Transformation, IndoorGML, PostGIS, Web Viewer |
| DOI | 없음 (학위논문) |
| 원문 | 확인하지 못함. [TU Delft Geomatics 논문 목록(2025년 9월 착수)](https://geomatics.bk.tudelft.nl/geo2022/theses/2025sep/) |

## 1. 연구 배경

TU Delft Geomatics 석사논문이며, 브리핑 기준으로 2026년 6월에 제출되었다. 발표 시점상 인용 수가 많을 수 없으므로 "고인용 검증 논문"은 아니다. 그러나 3DGS와 IndoorGML의 결합 가능성을 확인하려면 반드시 살펴봐야 하는 prior art다.

3D Gaussian Splatting(3DGS)은 여러 영상으로 장면의 외관과 기하를 표현하고 새로운 시점에서 빠르게 렌더링하는 장면 표현 기법이다. 실내 전체를 하나의 3DGS로 만들기보다 방 단위로 여러 장면을 만드는 경우가 많다. 그러면 여러 장면 사이를 어떻게 연결하고 이동을 제어할지가 문제가 된다.

TU Delft Geomatics 논문 목록의 연구 개요는 IndoorGML을 topology 기반으로 삼아 공간 변환으로 장면을 연결하고, topology 규칙을 강제하는 웹 기반 시각화를 구현한다고 설명한다.

## 2. 연구 Gap

**기존 연구의 한계**

(브리핑과 연구 개요 기반 해석) 3DGS 장면은 방마다 독립 좌표계를 가지며, 장면 사이의 공간 관계(어느 방이 어느 방과 연결되는가)를 표현하지 않는다.

**본 연구가 해결하려는 Gap**

여러 3DGS 장면을 공통 metric 좌표계로 정렬하고, IndoorGML topology로 방 사이 이동을 제어해 3DGS viewer 안에서 방과 방을 연결한다.

## 3. 연구 질문

브리핑과 연구 개요를 바탕으로 재구성하면 다음과 같다. 원문의 명시적 연구 질문은 확인이 필요하다.

1. 방별로 독립 생성한 여러 3DGS 장면을 하나의 공통 좌표계로 정렬할 수 있는가?
2. IndoorGML topology를 이용해 3DGS viewer에서 방 사이 이동을 제어할 수 있는가?

## 4. 핵심 기여

- 기존 방식: 단일 3DGS 장면, 또는 서로 연결되지 않은 여러 장면
- 문제: 장면 간 공간 관계가 없어 실내 전체를 연속적으로 탐색하기 어렵다.
- 제안 방법(브리핑 기준): 방별 3DGS → similarity transformation으로 공통 metric 좌표 정렬 → IndoorGML Cell–Node–Edge topology를 PostGIS에 저장 → 웹 viewer에서 topology 기반 navigation 제어
- 의미: "3DGS reference map에 IndoorGML을 붙일 수 있는가"라는 질문에 대해 "가능하며, 실제 prototype이 있다"는 답을 주는 연구다.

## 5. 연구 방법론

> [!warning] 전문 확인 필요
> 아래 구조는 기존 브리핑의 설명이다. 원문을 확인하지 못했다.

### 연구 대상 / 데이터

- 방별로 촬영해 만든 여러 개의 실내 3DGS 장면
- 대상 건물과 데이터 규모는 전문 확인이 필요하다.

### 시스템 구조

```text
Room별 3DGS
↓
SfM coordinate frame
↓
Umeyama Transformation
↓
공통 Metric Coordinate System
↓
IndoorGML
  Cell
  Node
  Edge
↓
PostGIS
↓
Web Viewer
↓
Room 사이 topology 기반 Navigation
```

방별로 독립적인 3DGS scene을 만들고, similarity transformation으로 공통 metric 좌표에 정렬한 다음, IndoorGML의 Cell–Node–Edge topology를 PostGIS에 넣어 방 사이 navigation을 제어한다.

### 사용 기술

브리핑 기준이며 원문 확인이 필요하다.

- 3D Gaussian Splatting
- SfM 좌표계
- Umeyama 알고리즘(similarity transformation 추정)
- IndoorGML
- PostGIS
- Web viewer

### 평가 방법

전문 확인이 필요하다.

## 6. 핵심 결과

> [!note]
> 원문을 확인하지 못해 결과와 수치를 기재하지 않는다. 브리핑은 이 연구가 prototype을 구현했다고 설명한다.

## 7. 결론 및 시사점

이 연구가 다루는 주요 문제는 여러 3DGS 장면을 IndoorGML topology로 연결하고 viewer 안의 이동을 제약하는 것이다.

```text
여러 개의 3DGS Scene
↓
IndoorGML topology
↓
Viewer 내 navigation constraint
```

즉 3DGS viewer에서 방 사이를 어떻게 연결할 것인가가 주요 문제다. 이와 구분되는 방향도 있다. 실제 사용자 카메라의 3DGS visual localization 결과(6DoF pose)를 IndoorGML Cell에 grounding해, 현재 semantic space와 topology 문맥을 판단하고 routing에 쓰는 방향이다. 이는 실제 위치추정 결과를 symbolic spatial model로 grounding하는 문제이며, viewer 내 이동 제약과는 성격이 다르다.

- Indoor GIS / IndoorGML: 최신 장면 표현(3DGS)과 OGC 표준 topology를 결합한 사례다.
- 3D GIS: 3DGS 장면을 공간 DB(PostGIS)와 연결해 관리하는 구조를 보여준다.
- Digital Twin: 사진 수준 시각화(3DGS)와 구조적 공간 모델(IndoorGML)을 분리해 결합하는 설계 사례다.

## 8. 연구의 한계

### 저자가 명시한 한계

원문을 확인하지 못했다.

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 석사학위논문으로 동료 심사를 거친 학술지·학회 논문과 검증 수준이 다르다.
- IndoorGML topology를 자동 생성하는지, 수작업으로 구축하는지에 따라 실무 적용 비용이 크게 달라진다. 원문 확인이 필요하다.
- Viewer 내 이동 제약이 중심이며, 실제 사용자의 위치 추정과 연결되는지는 확인이 필요하다.

## 9. 비판적 읽기

원문을 확인하지 못해 연구 설계, 데이터, baseline, 평가 지표, 데이터 신뢰성, 주장과 결과의 관계에 대한 평가는 보류한다. 원문 확인 시 다음을 우선 점검한다.

- IndoorGML 데이터의 생성 방식(수동/자동)
- 장면 정렬 정확도의 정량 평가 여부
- 사용자 평가 또는 성능 평가(렌더링 속도, 전환 지연 등) 여부
- 대상 건물 수와 규모

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 확인 불가 | 확인 가능한 정보 없음 |
| 선택 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 확증 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 확인 불가 | 확인 가능한 정보 없음 |

## 11. 주요 전문 용어

### 3D Gaussian Splatting (3DGS)

장면을 수많은 3D Gaussian(위치, 크기, 방향, 색, 불투명도)으로 표현하고, 이를 화면에 투영(splatting)해 빠르게 렌더링하는 장면 표현 기법이다.

### SfM (Structure from Motion)

여러 장의 사진에서 카메라 위치와 장면의 3D 점을 동시에 추정하는 기법이다. 3DGS 학습의 초기 카메라 pose와 점군을 제공한다(예: COLMAP).

### Umeyama Transformation

두 점 집합 사이의 최적 similarity transformation(회전, 이동, 축척)을 최소제곱으로 구하는 알고리즘이다. 서로 다른 좌표계의 장면을 정렬하는 데 쓰인다.

### Similarity Transformation

회전, 평행이동, 균일 축척으로 이루어진 좌표 변환이다. SfM 결과는 축척이 임의적이므로 metric 좌표로 맞출 때 필요하다.

### IndoorGML Cell / Node / Edge

IndoorGML에서 실내 공간 단위는 Cell(CellSpace)로, 그 쌍대 그래프의 노드(State)와 연결(Transition)로 navigation을 표현한다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

브리핑 기준이며 원문 확인이 필요하다.

- 3DGS, SfM, Umeyama transformation
- IndoorGML
- PostGIS
- Web viewer

### 실무 구현 시 적용 가능한 기술

아래는 서비스 구현 시 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**3DGS**
- COLMAP, gsplat, 웹 기반 3DGS 렌더러

**Spatial DB / 경로**
- PostgreSQL + PostGIS + pgRouting

**Backend**
- FastAPI, Spring Boot

**Visualization**
- Three.js 기반 viewer, Cesium

## 13. 커리어 관점

### 공부해야 할 기술

- 3DGS 원리와 학습 파이프라인(SfM → 학습 → 렌더링)
- 좌표계 정렬(similarity transformation, Umeyama)
- IndoorGML 데이터 모델
- PostGIS 기반 공간 데이터 관리와 웹 서비스 연동

### 실무 연결

- 실내 가상 투어, 부동산·시설 3D viewer에 공간 topology를 결합하는 서비스
- 3D 시각화와 공간 DB를 분리·연결하는 Digital Twin 아키텍처
- 실내 길찾기와 사진 수준 3D 시각화의 결합

### 기술 면접으로 연결될 수 있는 질문

- 3DGS와 point cloud, mesh의 차이는 무엇인가?
- 여러 SfM 결과를 하나의 좌표계로 합칠 때 축척 문제는 어떻게 해결하는가?
- 3D 시각화 데이터와 IndoorGML topology를 분리해 관리하는 장점은 무엇인가?
- PostGIS에 실내 navigation graph를 저장하고 경로를 찾는 방법은 무엇인가?

## 14. 후속 연구

### 저자가 제안한 Future Work

원문을 확인하지 못했다.

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- 3DGS visual localization으로 얻은 실제 사용자 pose를 IndoorGML Cell에 grounding
- 3DGS 장면에서 IndoorGML topology를 자동 생성·갱신
- 방 전환 시 렌더링 연속성과 사용자 경험 평가

## 15. 논문 읽기 가이드

**1순위 — 시스템 아키텍처**

3DGS 장면, 좌표 정렬, IndoorGML, PostGIS, viewer의 관계를 파악한다.

**2순위 — 좌표 정렬 방법**

Umeyama transformation으로 여러 장면을 metric 좌표로 맞추는 과정을 확인한다.

**3순위 — IndoorGML 구축과 저장**

Topology를 어떻게 만들고(수동/자동) PostGIS에 어떻게 저장하는지 확인한다.

**4순위 — 평가와 한계**

Prototype의 성능과 한계를 확인한다.

## 16. 핵심 정리

- 방별 3DGS 장면을 공통 좌표계로 정렬하고 IndoorGML topology로 연결하는 prototype 연구다(브리핑 기준).
- "3DGS + IndoorGML 결합" 자체는 이미 시도되었으므로, 그것만으로는 새로운 연구 질문이 되기 어렵다.
- 이 연구의 중심은 viewer 내 이동 제약이며, 실제 위치추정 결과를 IndoorGML 공간에 grounding하는 문제와는 구분된다.
- 석사학위논문이며 원문 확인 전이므로 세부 내용은 검증이 필요하다.

## 관련 글

- [[2011-hybrid-metric-topological-navigation|Navigation in Hybrid Metric-Topological Maps]] — metric과 topology의 역할 분리
- [[2021-semantics-guided-indoorgml-reconstruction|Semantics-guided IndoorGML Reconstruction]] — 3D 데이터에서 IndoorGML 자동 생성
