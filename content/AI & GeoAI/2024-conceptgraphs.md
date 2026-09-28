---
title: "ConceptGraphs — 2D Foundation Model로 만드는 Open-Vocabulary 3D Scene Graph와 LLM 기반 Planning (ICRA 2024)"
date: 2026-09-28
description: "SAM, CLIP, LLaVA, GPT-4 같은 2D foundation model의 출력을 다중 시점 연관으로 3D에 융합해 open-vocabulary 객체와 공간 관계를 가진 그래프를 만들고, 언어 기반 planning에 활용하는 ConceptGraphs 논문 리뷰"
category: "AI & GeoAI"
tags:
  - paper-review
  - 3d-scene-graph
  - open-vocabulary
  - foundation-model
  - llm
  - robot-planning
aliases:
  - ConceptGraphs
  - "ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning"
paper_title: "ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning"
authors:
  - Qiao Gu
  - Alihusein Kuwajerwala
  - Sacha Morin
  - Krishna Murthy Jatavallabhula
  - Bipasha Sen
  - Aditya Agarwal
  - Corban Rivera
  - William Paul
  - Kirsty Ellis
  - Rama Chellappa
  - Chuang Gan
  - Celso Miguel de Melo
  - Joshua B. Tenenbaum
  - Antonio Torralba
  - Florian Shkurti
  - Liam Paull
venue: "IEEE International Conference on Robotics and Automation (ICRA)"
year: 2024
paper_type: conference
doi: "10.1109/ICRA57147.2024.10610243"
url: "https://arxiv.org/abs/2309.16650"
verification: full-text
draft: true
---

> [!info] 검증 범위
> 서지정보와 초록은 arXiv와 IEEE Xplore에서, 방법·수치는 arXiv 원문(2309.16650)에서 확인했다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning |
| 저자 | Qiao Gu, Alihusein Kuwajerwala, Sacha Morin, Krishna Murthy Jatavallabhula, Bipasha Sen, Aditya Agarwal, Corban Rivera, William Paul, Kirsty Ellis, Rama Chellappa, Chuang Gan, Celso Miguel de Melo, Joshua B. Tenenbaum, Antonio Torralba, Florian Shkurti, Liam Paull |
| 연도 | 2024 (arXiv 공개 2023) |
| 저널/학회 | IEEE ICRA 2024 |
| 연구 분야 | Open-vocabulary 3D Perception, 3D Scene Graph, Robot Task Planning |
| 핵심 기술 | SAM, CLIP, DINO, LLaVA, GPT-4, Multi-view Association |
| DOI | [10.1109/ICRA57147.2024.10610243](https://doi.org/10.1109/ICRA57147.2024.10610243) |
| 원문 | [arXiv:2309.16650](https://arxiv.org/abs/2309.16650) |
| 프로젝트 | [concept-graphs.github.io](https://concept-graphs.github.io/) |
| 피인용 | OpenAlex 기반 집계 약 95회(브리핑 작성 시점) |

## 1. 연구 배경

ConceptGraphs는 비교적 최신 연구지만 이미 영향력이 커지고 있다. "사람이 이해할 수 있는 공간 표현을 바탕으로 한 의사결정"에 가까운 연구다.

저자들은 로봇이 다양한 과업을 수행하려면 semantic하게 풍부하면서도 과업 중심의 인지와 planning에 효율적인 compact한 3D 표현이 필요하다고 본다. 최근에는 대형 vision-language 모델의 특징을 3D 표현에 담으려는 시도가 있었다.

## 2. 연구 Gap

**기존 연구의 한계**

기존 접근은 점마다 특징 벡터를 저장하는 per-point feature map을 만드는 경향이 있었다. 이 방식에는 두 가지 문제가 있다.

- 큰 환경으로 잘 확장되지 않는다.
- Planning에 유용한 개체 간 semantic 공간 관계를 담지 못한다.

논문이 기존 per-point semantic map의 문제로 지적하는 핵심은 **점마다 semantic feature가 있다고 해서 개체 사이의 semantic spatial relationship이 표현되는 것은 아니다**라는 점이다.

```text
Semantic 3DGS / per-point map
→ "이건 Door다"

Graph
→ "이 Door는 Room A와 Corridor B를 연결한다"
```

**본 연구가 해결하려는 Gap**

Open-vocabulary 객체를 노드로, 공간 관계를 edge로 가지는 그래프 구조 3D 표현을 만든다. 대규모 3D 데이터를 수집하거나 모델을 finetuning하지 않고도 새로운 semantic 클래스로 일반화한다.

## 3. 연구 질문

논문의 목적을 바탕으로 재구성하면 다음과 같다.

1. 2D foundation model의 출력을 3D로 융합해 open-vocabulary 객체 그래프를 만들 수 있는가?
2. 추가 3D 학습 없이 새로운 semantic 클래스로 일반화할 수 있는가?
3. 이 그래프가 언어로 지정된 복잡한 planning 과업에 유용한가?

## 4. 핵심 기여

- 기존 방식: per-point feature를 저장하는 dense open-vocabulary map
- 문제: 대규모 환경에서 확장성이 낮고, 개체 간 관계가 없다.
- 제안 방법: 2D foundation model로 객체를 분할·기술하고, 다중 시점 연관으로 3D 객체로 융합한 뒤, LLM으로 객체 간 공간 관계를 추론해 graph를 만든다.
- 개선점: compact한 그래프 표현으로 새로운 클래스에 일반화하고, 추상적인 언어 프롬프트로 지정된 planning 과업을 수행한다.

## 5. 연구 방법론

### 연구 대상 / 데이터

- Replica 데이터셋(실내 장면)
- REAL Lab: 다양한 객체를 배치한 실내 장면
- AI2Thor 시뮬레이션 환경
- 실제 로봇: Clearpath Jackal UGV(VLP-16 LiDAR, RealSense D435i 카메라), Boston Dynamics Spot Arm

### 시스템 구조

```text
Posed RGB-D Images
↓
2D Foundation Models
  - Class-agnostic 2D segmentation (SAM)
  - Visual feature (CLIP, DINO)
↓
Instance Segmentation
↓
3D Object Fusion (기하·semantic 유사도 기반 multi-view association)
↓
Language / Vision Embedding
  - Node captioning (LLaVA)
↓
Object Relationships (GPT-4로 공간 관계 추론)
↓
3D Scene Graph
↓
LLM / Task Planning
```

탐지기 기반 변형(ConceptGraphs-Detector, CG-D)은 Grounding DINO와 RAM을 사용한다.

### 사용 기술

- Segment Anything(SAM)
- CLIP, DINO
- LLaVA(노드 캡셔닝)
- GPT-4(gpt-4-0613, 관계 추론과 planning)
- Grounding DINO, RAM(CG-D 변형)
- Multi-view association 기반 3D 객체 융합

### 평가 방법

- Node precision, edge precision: Amazon Mechanical Turk 사람 평가
- 유효 객체 수, 중복 검출 수
- Semantic segmentation: mAcc, F-mIoU
- 객체 검색: Recall@1, @2, @3(서술형, affordance, 부정형 질의)

## 6. 핵심 결과

**Scene graph 정확도 (Replica, 사람 평가)**

- ConceptGraphs 평균 node precision 0.71, edge precision 0.88
- ConceptGraphs-Detector 평균 node precision 0.61, edge precision 0.91
- 장면별 유효 객체 43~60개, 중복 0~5개

**Open-vocabulary semantic segmentation (Replica)**

| 방법 | mAcc | F-mIoU |
|---|---|---|
| ConceptGraphs | 40.63 | 35.95 |
| ConceptGraphs-Detector | 38.72 | 35.82 |
| OpenSeg | 41.19 | 53.74 |
| LSeg | 33.39 | 51.54 |
| CLIPSeg | 28.21 | 39.84 |
| ConceptFusion + SAM | 31.53 | 38.70 |
| ConceptFusion | 24.16 | 31.31 |
| MaskCLIP | 4.53 | 0.94 |

ConceptGraphs는 mAcc에서 상위권이지만 F-mIoU는 OpenSeg, LSeg보다 낮다. 이 논문의 초점은 segmentation 성능 자체보다 compact한 객체 그래프 표현에 있다.

**LLM 기반 객체 검색 (Replica, R@1)**

- 서술형 질의 0.61, affordance 질의 0.57, 부정형 질의 0.80
- REAL Lab에서는 세 유형 모두 R@1 1.00

실제 로봇(Jackal, Spot)에서 언어 질의 기반 객체 탐색과 조작 과업도 시연했다.

## 7. 결론 및 시사점

저자들은 추상적인 언어 프롬프트로 지정되고 공간·semantic 개념에 대한 복잡한 추론이 필요한 여러 planning 과업을 통해 이 표현의 유용성을 보였다.

- GeoAI / Spatial AI: Foundation model을 공간 표현 구축에 조합하는 설계의 대표 사례다.
- Indoor GIS / IndoorGML: "점 단위 의미"와 "개체 간 관계"를 구분하는 이 논문의 문제의식은 semantic map과 IndoorGML topology의 차이를 설명하는 데 그대로 쓸 수 있다.
- Digital Twin: 자연어로 공간을 질의하는 인터페이스와 연결된다.

## 8. 연구의 한계

### 저자가 명시한 한계

- LLaVA 같은 대형 vision-language 모델의 한계로 노드 캡션에 오류가 생긴다. 예를 들어 LLaVA-7B는 작은 물체 상당수를 칫솔이나 가위로 잘못 분류한다.
- 작거나 얇은 객체를 놓치거나 중복 검출하는 경우가 있다.
- 여러 번의 LVLM과 LLM 추론에 드는 계산·경제적 비용이 클 수 있다.

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 관계가 주로 객체 간 관계(예: 위에 있음)이며, room·place 수준의 공간 계층이나 navigation topology는 중심이 아니다.
- 입력으로 카메라 pose가 주어진(posed) RGB-D를 가정한다. SLAM 오차가 그래프 품질에 미치는 영향은 별도 검토가 필요하다.
- Node·edge precision이 사람 평가에 의존하므로 평가 일관성에 한계가 있다.
- 상용 LLM(GPT-4)을 쓰므로 버전 변화에 따른 재현성 문제가 있다.

## 9. 비판적 읽기

### 연구 설계

- 강점: 그래프 품질, segmentation, 객체 검색, 실제 로봇 과업까지 여러 층위에서 평가했다.
- 약점: 그래프 품질 평가가 사람 평가(AMT)에 의존한다.

### 데이터

- Replica는 합성에 가까운 고품질 실내 데이터다. 실제 환경 일반화는 로봇 시연 위주로 보였다.

### Baseline / 비교군

- Segmentation에서는 여러 open-vocabulary 방법과 비교했다. Scene graph 자체의 비교 대상은 제한적이다.

### 평가 지표

- R@k 기반 객체 검색은 언어 질의 응용에 적절하다. Edge precision은 관계 종류 다양성을 충분히 반영하지 못할 수 있다.

### 데이터 신뢰성

- LLM 출력은 확률적이므로 반복 실행 시 결과 변동을 확인할 필요가 있다.

### 주장과 결과의 관계

- "새로운 클래스로 일반화한다"는 주장은 open-vocabulary 설정의 구조적 장점에 근거한다. 정량적으로는 segmentation F-mIoU가 일부 baseline보다 낮다는 점도 함께 봐야 한다.

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 확인 불가 | 확인 가능한 정보 없음 |
| 선택 편향 | 중간 | Replica와 연구실 구성 장면 중심 |
| 확증 편향 | 낮음 | LLaVA 오분류, 누락·중복 등 실패 사례를 보고 |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 중간 | 가정·연구실형 실내 환경 중심 |

## 11. 주요 전문 용어

### Open-Vocabulary

학습 때 정해진 클래스 목록에 한정되지 않고, 텍스트로 표현된 임의의 개념을 인식하거나 질의할 수 있는 성질이다.

### Foundation Model

대규모 데이터로 사전학습되어 여러 하위 과업에 범용으로 쓰이는 모델이다. 예를 들어 SAM, CLIP, GPT-4가 있다.

### SAM (Segment Anything Model)

클래스와 무관하게 이미지의 객체 영역을 분할하는 범용 segmentation 모델이다.

### CLIP

이미지와 텍스트를 같은 임베딩 공간에 두도록 학습한 모델이다. 텍스트 질의로 이미지 영역을 찾는 데 쓰인다.

### Multi-view Association

여러 시점에서 검출된 2D 객체가 같은 3D 객체인지 판단해 하나로 묶는 과정이다.

### Per-point Feature Map

3D 지도의 각 점에 semantic 특징 벡터를 저장하는 표현이다. 풍부하지만 메모리가 크고, 개체 간 관계를 담지 않는다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

- SAM, CLIP, DINO, LLaVA, GPT-4, Grounding DINO, RAM
- Replica, AI2Thor
- Clearpath Jackal, Boston Dynamics Spot

### 실무 구현 시 적용 가능한 기술

아래는 서비스 구현 시 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**AI**
- PyTorch, 오픈소스 vision-language 모델

**Graph 저장·질의**
- Neo4j, Knowledge Graph(RDF/OWL)

**Spatial DB**
- PostgreSQL + PostGIS

**Backend**
- FastAPI(자연어 공간 질의 API)

## 13. 커리어 관점

### 공부해야 할 기술

- Vision-language 모델(CLIP, SAM) 활용법
- 2D 검출 결과를 3D로 투영·융합하는 카메라 기하
- LLM 기반 planning과 프롬프트 설계
- Scene graph와 knowledge graph 모델링

### 실무 연결

- 자연어 기반 실내 공간·자산 검색 서비스
- 로봇의 언어 명령 기반 탐색·조작
- Digital Twin에 LLM 질의 인터페이스 결합

### 기술 면접으로 연결될 수 있는 질문

- Per-point semantic map과 scene graph의 차이는 무엇인가?
- Open-vocabulary 인식이 필요한 이유와 한계는 무엇인가?
- LLM을 공간 추론에 쓸 때 hallucination을 어떻게 통제할 수 있는가?
- "이건 Door다"와 "이 Door는 A와 B를 연결한다"를 표현하려면 각각 어떤 데이터 구조가 필요한가?

## 14. 후속 연구

### 저자가 제안한 Future Work

- 시간적 변화(temporal dynamics)를 모델에 통합
- 덜 구조화되고 더 어려운 환경에서의 성능 평가
- Instruction-finetuned LLaVA 변형 등 더 성능 좋은 vision-language 모델 사용

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- 객체 그래프에 room·place 계층을 추가해 navigation topology와 결합
- LLM 추론 결과를 IndoorGML 같은 표준 모델로 검증·정규화
- 3DGS 기반 장면 표현과 open-vocabulary 그래프의 결합

## 15. 논문 읽기 가이드

**1순위 — Pipeline Figure**

2D foundation model → 3D 융합 → 캡셔닝 → 관계 추론 흐름을 파악한다.

**2순위 — Object Association과 Fusion**

다중 시점 객체를 하나로 묶는 기준을 이해한다.

**3순위 — 실험 결과**

Node·edge precision, segmentation, 객체 검색 결과를 확인한다.

**4순위 — Limitations**

LVLM 오류, 비용, 누락·중복 문제를 확인한다.

## 16. 핵심 정리

- 점마다 semantic feature가 있다고 해서 개체 간 공간 관계가 표현되는 것은 아니다.
- ConceptGraphs는 2D foundation model을 조합해 open-vocabulary 객체와 관계를 가진 compact한 3D 그래프를 만든다.
- 추가 3D 학습 없이 새로운 개념으로 일반화하고, LLM 기반 planning에 활용된다.
- Foundation model 시대의 공간 표현은 "의미 인식"과 "관계 구조"를 분리해서 설계해야 한다.

## 관련 글

- [[2021-scenegraphfusion|SceneGraphFusion]] — closed-set 증분 scene graph
- [[2024-open3dsg|Open3DSG]] — 점군 기반 open-vocabulary scene graph
- [[2021-kimera|Kimera]] — room·place 계층을 가진 scene graph
