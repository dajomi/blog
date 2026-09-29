---
title: "SceneGraphFusion — RGB-D 시퀀스에서 3D Scene Graph를 실시간·증분적으로 예측하는 GNN (CVPR 2021)"
date: 2026-09-28
description: "RGB-D 시퀀스를 받으면서 기하 분할과 feature-wise attention GNN으로 객체, 클래스, 객체 간 관계를 포함한 3D scene graph를 증분적으로 예측하는 SceneGraphFusion 논문 리뷰"
category: "AI & GeoAI"
tags:
  - paper-review
  - 3d-scene-graph
  - graph-neural-network
  - rgb-d
  - incremental-mapping
aliases:
  - SceneGraphFusion
  - "SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences"
paper_title: "SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences"
authors:
  - Shun-Cheng Wu
  - Johanna Wald
  - Keisuke Tateno
  - Nassir Navab
  - Federico Tombari
venue: "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)"
year: 2021
paper_type: conference
doi: ""
url: "https://openaccess.thecvf.com/content/CVPR2021/papers/Wu_SceneGraphFusion_Incremental_3D_Scene_Graph_Prediction_From_RGB-D_Sequences_CVPR_2021_paper.pdf"
verification: full-text
---

> [!info] 검증 범위
> 서지정보는 CVF Open Access와 저자 페이지에서, 방법·수치는 arXiv 원문(2103.14898)에서 확인했다. DOI는 이번 작업에서 확인하지 못해 CVF 공식 링크를 원문으로 적는다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences |
| 저자 | Shun-Cheng Wu, Johanna Wald, Keisuke Tateno, Nassir Navab, Federico Tombari |
| 연도 | 2021 |
| 저널/학회 | IEEE/CVF CVPR 2021 |
| 연구 분야 | 3D Scene Understanding, 3D Scene Graph Prediction |
| 핵심 기술 | Incremental Geometric Segmentation, Graph Neural Network, Feature-wise Attention |
| DOI | 확인하지 못함 |
| 원문 | [CVF Open Access](https://openaccess.thecvf.com/content/CVPR2021/papers/Wu_SceneGraphFusion_Incremental_3D_Scene_Graph_Prediction_From_RGB-D_Sequences_CVPR_2021_paper.pdf), [arXiv:2103.14898](https://arxiv.org/abs/2103.14898) |
| 프로젝트 | [shunchengwu.github.io/SceneGraphFusion](https://shunchengwu.github.io/SceneGraphFusion) |

## 1. 연구 배경

GIS 관점에서는 공간의 semantic과 topology를 IndoorGML로 표현하는 것이 자연스럽다. 그러나 Robotics와 Computer Vision 연구자들은 같은 문제를 3D Scene Graph로 해결하는 경우가 많다.

```text
GIS:           semantic / topology → IndoorGML
Robotics / CV: semantic / topology → 3D Scene Graph
```

SceneGraphFusion은 이 흐름에서 RGB-D 시퀀스를 받으면서 실시간으로 3D 객체, 객체 클래스, 관계를 예측해 3D scene graph를 증분적으로 구축하는 연구다.

```text
3D Objects
+
Object Classes
+
Relationships
↓
3D Scene Graph
```

즉 IndoorGML 같은 고정 스키마 없이도 다음과 같은 symbolic structure를 생성한다.

```text
chair ─ inside → office
table ─ inside → office
door  ─ connects → corridor
```

## 2. 연구 Gap

**기존 연구의 한계**

- 기존 3D scene graph 예측(3DSSG 등)은 완성된 3D 장면 전체를 오프라인으로 처리했다.
- 증분적으로 쌓이는 3D 데이터는 불완전하고, 이웃 관계가 없거나 계속 바뀐다. 기존 GNN은 이런 조건을 다루기 어려웠다.

**본 연구가 해결하려는 Gap**

기하 분할과 새로운 GNN을 결합해 장면을 재구성하는 동시에 전역적으로 일관된 semantic 모델(scene graph)을 증분적으로 구축한다. 불완전한 3D 데이터를 다루기 위해 feature-wise attention을 도입한다.

## 3. 연구 질문

논문의 기여를 바탕으로 재구성하면 다음과 같다.

1. RGB-D 시퀀스가 들어오는 동안 3D scene graph를 실시간·증분적으로 예측할 수 있는가?
2. 이웃 관계가 불완전하거나 변하는 증분 데이터에서 GNN이 안정적으로 동작하게 할 수 있는가?
3. 증분 방식이 오프라인 방식과 비교해 경쟁력 있는 정확도를 내는가?

## 4. 핵심 기여

- 기존 방식: 완성된 3D 장면 전체를 입력으로 하는 오프라인 scene graph 예측
- 문제: 로봇·혼합현실처럼 실시간이 필요한 응용에 쓸 수 없다.
- 제안 방법
  - 증분 기하 분할로 segment 생성
  - Segment 간 거리 기반 이웃 그래프 구성
  - Feature-wise attention(FAT)을 갖춘 GNN으로 객체와 관계 예측
  - 같은 객체 인스턴스에 속한 segment를 잇는 "same part" 관계 도입(panoptic segmentation과 유사한 인스턴스 식별)
- 개선점: 3D scene graph 예측 벤치마크에서 경쟁력 있는 성능, 3D semantic·instance segmentation 벤치마크에서 기존 방법과 대등한 성능을 35Hz로 달성

## 5. 연구 방법론

### 연구 대상 / 데이터

- 3RScan / 3DSSG
  - 전체 평가: 객체 클래스 160개, predicate(관계) 26개
  - 기하 segment 평가: NYUv2 기반 20개 클래스, predicate 8개
- ScanNet: panoptic / semantic segmentation 벤치마크

### 시스템 구조

```text
RGB-D Sequence
↓
Incremental Geometric Segmentation
↓
Segment Neighbor Graph (거리 0.5m 기준 인접)
↓
GNN (message passing 2층 + Feature-wise Attention)
↓
Object Class + Relationship (predicate) + "same part"
↓
Incremental 3D Scene Graph (전역적으로 일관)
```

### 사용 기술

- 증분 기하 분할
- Graph Neural Network(message passing)
- Feature-wise Attention(FAT)
- "Same part" 관계로 인스턴스 식별

### 평가 방법

- 관계·객체·predicate recall(R@1, R@3, R@50, R@100)
- Panoptic Quality(PQ), Segmentation Quality(SQ), Recognition Quality(RQ)
- mAP, IoU
- 처리 속도

## 6. 핵심 결과

- 3DSSG(정답 인스턴스 사용)에서 관계 예측 R@50 0.85, R@100 0.87을 기록했다. 비교 기준인 3DSSG는 각각 0.39, 0.45였다.
- 기하 segment 기반 전체 장면 평가에서 관계 R@1은 FAT 적용 시 0.55, attention 없이 0.41이었다. Feature-wise attention의 효과를 보여준다.
- ScanNet semantic segmentation에서 mAP 63.7을 기록했다.
- 약 35Hz로 동작한다고 보고했다. 원문의 처리 시간 분해(분할과 그래프 예측 단계)는 원문에서 함께 확인하는 것이 좋다.

## 7. 결론 및 시사점

저자들은 제안 방법이 3D scene graph 예측 벤치마크에서 경쟁력 있는 성능을 보이고, 3D semantic·instance segmentation 벤치마크에서 기존 방법과 대등하면서 35Hz로 동작해 로봇과 혼합현실 응용에 쓸 수 있다고 결론짓는다.

- GeoAI / Spatial AI: 객체 간 관계를 학습으로 예측하는 대표 연구다. 고정 스키마 없이 관계 구조를 만든다는 점에서 IndoorGML 같은 표준 모델과 접근이 다르다.
- Indoor GIS: "inside", "connects" 같은 관계는 IndoorGML topology와 개념적으로 겹친다. 두 표현 간 변환이 연구 과제가 될 수 있다.
- Digital Twin: 실시간으로 갱신되는 객체·관계 그래프는 운영형 Digital Twin의 장면 모델로 활용할 수 있다.

## 8. 연구의 한계

### 저자가 명시한 한계

- 방법이 의존하는 장면 기하가 누락되면 PanopticFusion 대비 panoptic RQ 점수가 낮아진다.
- 증분 semantic scene graph를 SLAM 프레임워크의 카메라 pose 추정이나 loop closure 검출에 활용하는 것은 향후 과제로 남겼다.

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 3DSSG의 고정 클래스·predicate 집합에 한정된 closed-set 예측이다.
- 관계는 주로 객체 간 관계이며, room이나 place 같은 공간 단위 계층은 다루지 않는다.
- 3RScan은 소규모 실내 공간 스캔 위주여서 건물 규모로의 확장은 별도 검증이 필요하다.

## 9. 비판적 읽기

### 연구 설계

- 강점: 증분 방식이면서 오프라인 방법과 같은 벤치마크로 비교했다.
- 약점: 정답 인스턴스를 쓰는 설정과 기하 segment를 쓰는 설정의 성능 차이가 크므로, 실제 사용 조건에 가까운 설정의 결과를 중심으로 읽어야 한다.

### 데이터

- 공개 벤치마크(3RScan/3DSSG, ScanNet)로 재현성이 있다.

### Baseline / 비교군

- 3DSSG(오프라인 scene graph), SemanticFusion, ProgressiveFusion, FusionAware(증분 semantic SLAM), PanopticFusion과 비교했다. attention 변형(GAT, SDPA)과의 비교도 포함한다.

### 평가 지표

- Recall@k는 scene graph 예측의 표준 지표다. PQ, mAP로 segmentation 성능도 함께 평가했다.

### 데이터 신뢰성

- 3DSSG 관계 라벨의 품질과 불균형에 결과가 영향을 받을 수 있다.

### 주장과 결과의 관계

- "대등한 성능"은 segmentation 벤치마크에 대한 주장이다. scene graph 성능은 "경쟁력 있는" 수준이라는 표현을 구분해서 읽어야 한다.

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 확인 불가 | Google 소속 저자 포함. 이해충돌 정보는 확인 가능한 정보 없음 |
| 선택 편향 | 낮음 | 공개 벤치마크 사용 |
| 확증 편향 | 낮음 | PanopticFusion 대비 약점을 보고 |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 중간 | 실내 소규모 공간 스캔 데이터 중심 |

## 11. 주요 전문 용어

### 3D Scene Graph Prediction

3D 장면에서 객체(노드)와 객체 간 관계(edge, predicate)를 예측해 그래프로 표현하는 작업이다.

### Graph Neural Network (GNN)

노드와 edge의 특징을 이웃 간 message passing으로 갱신하며 학습하는 신경망이다.

### Feature-wise Attention

특징 벡터의 각 차원별로 이웃 정보의 가중치를 다르게 주는 attention이다. 이웃이 불완전하거나 변하는 증분 데이터에서 안정적인 학습을 돕는다.

### Predicate

Scene graph에서 두 객체 사이 관계의 종류다. 예를 들어 "standing on", "attached to", "same part" 등이 있다.

### Panoptic Segmentation

모든 픽셀(점)에 클래스 라벨을 주면서, 셀 수 있는 객체는 인스턴스별로도 구분하는 segmentation이다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

- 증분 기하 분할
- GNN + Feature-wise Attention
- 3RScan/3DSSG, ScanNet 데이터셋

### 실무 구현 시 적용 가능한 기술

아래는 서비스 구현 시 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**AI**
- PyTorch, PyTorch Geometric

**Graph 저장·질의**
- Neo4j, RDF/OWL 기반 Knowledge Graph

**Spatial DB**
- PostgreSQL + PostGIS

**표준 연계**
- Scene graph 관계를 IndoorGML 또는 IFC 관계로 매핑하는 변환 계층

## 13. 커리어 관점

### 공부해야 할 기술

- GNN 기초(message passing, attention)
- 3D scene graph 데이터셋(3RScan/3DSSG) 구조
- 증분 mapping과 SLAM 연동 개념
- Knowledge graph와 scene graph의 차이

### 실무 연결

- 실내 공간의 객체·관계 자동 인식(시설 자산 인벤토리)
- 혼합현실(MR) 응용의 실시간 장면 이해
- Digital Twin의 객체 관계 모델 자동 구축

### 기술 면접으로 연결될 수 있는 질문

- 3D scene graph와 IndoorGML은 어떤 문제를 각각 어떻게 푸는가?
- 증분 방식 scene graph 예측이 오프라인 방식보다 어려운 이유는 무엇인가?
- GNN에서 attention을 쓰는 이유는 무엇인가?
- Scene graph를 knowledge graph로 저장하려면 어떤 모델링이 필요한가?

## 14. 후속 연구

### 저자가 제안한 Future Work

- 증분 semantic scene graph를 SLAM의 카메라 pose 추정과 loop closure 검출에 활용

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- 객체 관계에 room·place 계층을 추가해 navigation 가능한 공간 그래프로 확장
- Open-vocabulary 객체·관계로 확장(후속 연구 Open3DSG 방향)
- Scene graph ↔ IndoorGML 자동 변환

## 15. 논문 읽기 가이드

**1순위 — 시스템 개요 Figure**

증분 분할 → 이웃 그래프 → GNN 예측 흐름을 파악한다.

**2순위 — Feature-wise Attention과 "same part" 관계**

핵심 기술 기여를 이해한다.

**3순위 — 3DSSG와 ScanNet 결과 표**

오프라인 방법과의 비교, attention 효과, 속도를 확인한다.

**4순위 — Conclusion**

SLAM 연동 향후 과제를 확인한다.

## 16. 핵심 정리

- Robotics/CV는 공간의 semantic과 관계를 IndoorGML이 아닌 3D scene graph로 표현하는 경우가 많다.
- SceneGraphFusion은 RGB-D 시퀀스에서 객체·관계 그래프를 증분적으로 예측한다.
- Feature-wise attention은 불완전하고 변하는 증분 데이터에서 GNN 성능을 높인다.
- 고정 스키마 없이도 "inside", "connects" 같은 symbolic 공간 구조를 자동 생성할 수 있다.

## 관련 글

- [[2024-conceptgraphs|ConceptGraphs]] — foundation model 기반 open-vocabulary scene graph
- [[2024-open3dsg|Open3DSG]] — 점군에서 open-set 관계까지 예측
- [[2017-semanticfusion|SemanticFusion]] — 증분 semantic mapping의 선행 연구
