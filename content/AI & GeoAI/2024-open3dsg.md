---
title: "Open3DSG — 점군에서 Open-Vocabulary 객체와 Open-Set 관계를 예측하는 3D Scene Graph (CVPR 2024)"
date: 2026-09-28
description: "3D scene graph GNN backbone을 2D vision-language foundation model 특징 공간과 공동 임베딩하고, LLM으로 객체 간 관계를 생성해 라벨 없이 점군에서 open-vocabulary 3D scene graph를 예측하는 Open3DSG 논문 리뷰"
category: "AI & GeoAI"
tags:
  - paper-review
  - 3d-scene-graph
  - open-vocabulary
  - point-cloud
  - vision-language-model
  - knowledge-distillation
aliases:
  - Open3DSG
  - "Open3DSG: Open-Vocabulary 3D Scene Graphs from Point Clouds with Queryable Objects and Open-Set Relationships"
paper_title: "Open3DSG: Open-Vocabulary 3D Scene Graphs from Point Clouds with Queryable Objects and Open-Set Relationships"
authors:
  - Sebastian Koch
  - Narunas Vaskevicius
  - Mirco Colosi
  - Pedro Hermosilla
  - Timo Ropinski
venue: "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)"
year: 2024
paper_type: conference
doi: ""
url: "https://openaccess.thecvf.com/content/CVPR2024/html/Koch_Open3DSG_Open-Vocabulary_3D_Scene_Graphs_from_Point_Clouds_with_Queryable_CVPR_2024_paper.html"
verification: full-text
---

> [!info] 검증 범위
> 서지정보와 초록은 arXiv(2402.12259)와 CVF Open Access에서, 방법·수치는 arXiv 원문에서 확인했다. DOI는 이번 작업에서 확인하지 못해 CVF 공식 링크를 원문으로 적는다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | Open3DSG: Open-Vocabulary 3D Scene Graphs from Point Clouds with Queryable Objects and Open-Set Relationships |
| 저자 | Sebastian Koch, Narunas Vaskevicius, Mirco Colosi, Pedro Hermosilla, Timo Ropinski |
| 연도 | 2024 |
| 저널/학회 | IEEE/CVF CVPR 2024 |
| 연구 분야 | 3D Scene Graph Prediction, Open-vocabulary 3D Understanding |
| 핵심 기술 | GNN Backbone, 2D–3D Feature Distillation, OpenSeg, InstructBLIP, LLM |
| DOI | 확인하지 못함 |
| 원문 | [CVF Open Access](https://openaccess.thecvf.com/content/CVPR2024/html/Koch_Open3DSG_Open-Vocabulary_3D_Scene_Graphs_from_Point_Clouds_with_Queryable_CVPR_2024_paper.html), [arXiv:2402.12259](https://arxiv.org/abs/2402.12259) |
| 코드 | [boschresearch/Open3DSG](https://github.com/boschresearch/Open3DSG) |

## 1. 연구 배경

Open3DSG는 입력이 3D point cloud라는 점이 특징이다.

```text
Point Cloud
↓
Object Detection / Segmentation
↓
Object Classes
↓
LLM / VLM
↓
Relationships
↓
3D Scene Graph
```

기존 3D scene graph 예측은 라벨링된 데이터셋으로 고정된 객체 클래스와 관계 범주를 학습했다. Open3DSG는 미리 정의된 클래스에 한정되지 않는 open-vocabulary 객체와 open-set 관계를 만든다. 즉 "점군을 AI로 semantic하게 해석하고 관계까지 자동 추출한다"는 방향도 빠르게 발전하고 있다.

## 2. 연구 Gap

**기존 연구의 한계**

- 3D scene graph 예측이 라벨된 데이터셋에 의존하며, 알려진 고정 객체 클래스와 관계 범주만 다룬다.
- 드물거나 구체적인 객체와 관계를 표현하지 못한다.

**본 연구가 해결하려는 Gap**

라벨된 scene graph 데이터 없이 열린 세계(open world)에서 3D scene graph 예측을 학습한다. 명시적인 open-vocabulary 객체 클래스뿐 아니라 사전 정의된 라벨 집합에 한정되지 않는 open-set 관계까지 예측하는 첫 3D 점군 방법이다.

## 3. 연구 질문

논문의 목적을 바탕으로 재구성하면 다음과 같다.

1. 라벨된 scene graph 없이 2D foundation model의 지식을 3D 점군 scene graph로 옮길 수 있는가?
2. 객체 클래스를 open vocabulary에서 질의하고, 객체 간 관계를 자유 형식으로 예측할 수 있는가?
3. 이 방법이 드문(long-tail) 객체와 관계를 표현하는 데 유리한가?

## 4. 핵심 기여

- 기존 방식: 라벨 기반 closed-set 3D scene graph 예측
- 문제: 새로운 객체·관계를 표현하지 못하고, long-tail 범주에 약하다.
- 제안 방법
  - 3D scene graph 예측 backbone(GNN)의 특징을 강력한 2D vision-language foundation model의 특징 공간과 공동 임베딩(co-embed)
  - 객체 클래스는 open vocabulary 텍스트와의 유사도로 질의
  - 관계는 scene graph 특징과 질의된 객체 클래스를 문맥으로 받은 grounded LLM이 생성
- 개선점: zero-shot으로 점군에서 3D scene graph를 예측하고, 공간·지지·semantic·비교 관계 등 복잡한 객체 간 관계를 표현한다.

## 5. 연구 방법론

### 연구 대상 / 데이터

- 학습(distillation): ScanNet. 기록 프레임의 시야가 3DSSG/3RScan보다 넓어 선택했다고 설명한다.
- 평가: 3DSSG. 3D 장면에 정렬된 semantic scene graph 라벨을 제공하는 유일한 데이터셋이라는 이유다.

### 시스템 구조

```text
3D Point Cloud
↓
GNN Backbone (node–edge–node triplet 특징 갱신)
↓
2D VLM 특징 증류
  - 객체: OpenSeg
  - 관계: InstructBLIP
↓
객체 예측: open-vocabulary 텍스트 프롬프트와 2D–3D 앙상블 그래프 임베딩 간 cosine similarity (CLIP 텍스트 인코더)
↓
관계 예측: InstructBLIP(ViT encoder + Q-Former) → LLM에
          "Describe the relationship between [object1] and [object2]?" 형태로 질의
↓
Open-vocabulary 3D Scene Graph
```

### 사용 기술

- Graph Neural Network backbone
- 2D–3D feature distillation
- OpenSeg, CLIP 텍스트 인코더
- InstructBLIP, LLM
- ScanNet, 3DSSG

### 평가 방법

- 객체, predicate, subject–predicate–object triplet의 top-k recall(R@k)
- 클래스별 mean recall(mR@k), 빈도별(head/body/tail) 분석

## 6. 핵심 결과

**Closed-vocabulary 3DSSG 벤치마크**

- Open3DSG 객체 R@5 0.57, predicate R@3 0.63
- 같은 벤치마크에서 지도학습 방식 3DSSG는 객체 R@5 0.68, predicate R@3 0.89
- 라벨 없이 학습한 방법이 지도학습 방법에 근접하지만, predicate 예측에서는 격차가 크다.

**Open-vocabulary 대안 방법과의 비교 (객체 R@5 / predicate R@3)**

- 단순 CLIP 질의: 0.35 / 0.09
- OpenSeg + CLIP: 0.38 / 0.10
- OpenSeg + NegCLIP: 0.38 / 0.10
- BLIPv2 캡션 기반: 0.38 / 0.50

**Long-tail 성능**

- Tail 객체 R@5: Open3DSG 0.42, 지도학습 VL-SAT 0.31
- Tail predicate R@3: Open3DSG 0.57, VL-SAT 0.58

드문 객체 범주에서는 라벨 없는 open-vocabulary 방식이 지도학습 방식보다 유리한 결과를 보였다.

> [!note]
> Triplet(relationship) 수준 recall 비교는 원문 Table 1에서 직접 확인하는 것을 권한다. 본 글에서는 객체·predicate 수치만 옮겼다.

## 7. 결론 및 시사점

저자들은 Open3DSG가 임의의 객체 클래스와 공간·지지·semantic·비교 관계를 포함한 복잡한 객체 간 관계를 예측하는 데 효과적이라고 결론짓는다. 동시에 open-vocabulary 관계 예측은 여전히 어려운 문제라고 인정한다.

- GeoAI: 2D foundation model 지식을 3D 공간 데이터로 증류하는 방식은 라벨이 부족한 공간 데이터 AI의 일반적 전략으로 볼 수 있다.
- Indoor GIS: 점군에서 관계까지 자동 추출하는 흐름은 IndoorGML topology 자동 생성과 방향이 겹친다. 다만 관계가 자유 텍스트여서 표준 스키마로의 정규화가 필요하다.
- Digital Twin / BIM: 스캔 점군에서 객체와 관계를 자동 추출해 자산 관계 모델을 만드는 데 응용할 수 있다.

## 8. 연구의 한계

### 저자가 명시한 한계

- Open-vocabulary 관계 예측은 여전히 어려운 문제다.
- Open-vocabulary 방법의 평가 설정은 아직 해결되지 않은 문제다.
- 예측된 관계의 다양성이 낮고, LLM hallucination이 발생한다.

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 관계가 객체 간 관계 중심이며, room·place 같은 공간 단위 계층은 다루지 않는다.
- 자유 텍스트 관계는 표현력이 높지만, 경로 탐색 같은 기계적 처리에는 표준화된 관계 체계가 필요하다.
- 평가 데이터(3DSSG)가 closed-set 라벨이어서 open-set 관계의 품질을 온전히 측정하기 어렵다.

## 9. 비판적 읽기

### 연구 설계

- 강점: 지도학습 방법과 open-vocabulary 대안 방법 모두와 비교해 위치를 명확히 했다.
- 약점: Open-set 관계를 closed-set 벤치마크로 평가하는 구조적 한계가 있다(저자도 인정).

### 데이터

- 학습과 평가 데이터셋을 분리했다(ScanNet → 3DSSG). 일반화 측정에 유리하다.

### Baseline / 비교군

- 지도학습(3DSSG, VL-SAT)과 open-vocabulary 대안 4종을 비교했다.

### 평가 지표

- R@k와 빈도별 mR@k로 long-tail 효과를 보였다. 적절하다.

### 데이터 신뢰성

- LLM 생성 관계의 평가는 텍스트 매칭 방식에 따라 결과가 달라질 수 있다.

### 주장과 결과의 관계

- "첫 open-set 관계 예측 방법"이라는 주장과 달리, predicate 성능은 지도학습보다 크게 낮다. "가능성을 보였다" 수준으로 읽는 것이 적절하다.

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 확인 불가 | Bosch Research 소속 저자 포함. 이해충돌 정보는 확인 가능한 정보 없음 |
| 선택 편향 | 낮음 | 공개 데이터셋 사용 |
| 확증 편향 | 낮음 | 관계 예측의 어려움, 평가 한계, hallucination을 명시 |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 중간 | 실내 소규모 공간 스캔 데이터 중심 |

## 11. 주요 전문 용어

### Open-Set Relationship

미리 정해진 관계 범주 목록에 없는 관계도 자유 형식으로 표현하는 것이다.

### Knowledge Distillation

큰 모델(teacher)의 지식을 다른 모델(student)이 모방하도록 학습시키는 방법이다. 여기서는 2D VLM의 특징을 3D GNN이 따라 하도록 학습한다.

### Co-embedding

서로 다른 모달리티(3D 점군, 2D 이미지, 텍스트)의 특징을 같은 임베딩 공간에 두어 직접 비교할 수 있게 하는 것이다.

### InstructBLIP

이미지와 지시문을 함께 받아 텍스트를 생성하는 vision-language 모델이다. ViT 인코더와 Q-Former를 거쳐 LLM에 시각 정보를 전달한다.

### Long-tail

데이터에서 등장 빈도가 낮은 다수의 범주다. 지도학습 모델은 이런 범주에 약한 경향이 있다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

- GNN backbone
- OpenSeg, CLIP 텍스트 인코더, InstructBLIP, LLM
- ScanNet(학습), 3DSSG(평가)

### 실무 구현 시 적용 가능한 기술

아래는 서비스 구현 시 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**AI**
- PyTorch, PyTorch Geometric

**Point Cloud**
- Open3D, PDAL

**Graph / Knowledge**
- Neo4j, RDF/OWL 온톨로지(관계 정규화)

**표준 연계**
- IFC 관계(IfcRel*), IndoorGML topology로 매핑

## 13. 커리어 관점

### 공부해야 할 기술

- 2D–3D feature distillation
- Vision-language 모델 구조(CLIP, BLIP 계열)
- GNN 기반 scene graph 예측
- 관계 표현의 온톨로지 정규화

### 실무 연결

- 스캔 데이터 기반 시설 자산·관계 자동 인식
- 라벨이 부족한 공간 데이터에 foundation model 지식 이전
- 자연어 질의 기반 3D 공간 검색

### 기술 면접으로 연결될 수 있는 질문

- Closed-set과 open-vocabulary 인식의 차이와 각각의 장단점은 무엇인가?
- 2D 모델 지식을 3D 점군 모델로 옮기는 방법은 무엇인가?
- 자유 텍스트 관계를 표준 스키마로 정규화하려면 무엇이 필요한가?
- LLM 기반 관계 예측의 hallucination을 어떻게 평가·억제할 수 있는가?

## 14. 후속 연구

### 저자가 제안한 Future Work

- 관계 예측 성능의 추가 개선
- Open-vocabulary 방법에 맞는 평가 체계 마련(저자가 미해결 문제로 언급)

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- Open-set 관계를 IndoorGML·IFC 관계 체계로 매핑하는 정규화 계층
- 객체 그래프에 room·place 계층 추가
- 3DGS 기반 장면에서의 open-vocabulary scene graph

## 15. 논문 읽기 가이드

**1순위 — Method Overview Figure**

GNN backbone과 2D VLM 증류, 객체·관계 예측 경로를 파악한다.

**2순위 — Relationship Prediction**

InstructBLIP과 LLM으로 관계를 생성하는 방식을 이해한다.

**3순위 — Table 1, Table 2**

지도학습 대비 성능과 long-tail 결과를 확인한다.

**4순위 — Limitations**

관계 다양성, hallucination, 평가 설정 문제를 확인한다.

## 16. 핵심 정리

- Open3DSG는 라벨된 scene graph 없이 점군에서 open-vocabulary 객체와 open-set 관계를 예측한다.
- 2D foundation model 특징을 3D GNN에 증류하고, 관계는 LLM으로 생성한다.
- 지도학습 대비 전체 성능은 낮지만, 드문 객체 범주에서는 유리하다.
- 점군 → semantic → 관계 추출은 이미 자동화되고 있으며, 남은 과제는 관계의 정확성과 표준화다.

## 관련 글

- [[2024-conceptgraphs|ConceptGraphs]] — RGB-D 기반 open-vocabulary scene graph
- [[2021-scenegraphfusion|SceneGraphFusion]] — closed-set 증분 scene graph
- [[2021-semantics-guided-indoorgml-reconstruction|Semantics-guided IndoorGML Reconstruction]] — 점군 해석을 표준 topology로 연결
