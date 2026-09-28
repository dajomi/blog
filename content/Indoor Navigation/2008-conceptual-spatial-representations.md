---
title: "Conceptual Spatial Representations — Metric·Navigation·Topological·Conceptual 계층으로 실내 공간을 표현하는 로봇 지도 (RAS 2008)"
date: 2026-09-28
description: "Metric line map, navigation graph, 문으로 나뉜 topological area, OWL-DL 온톨로지 기반 conceptual map의 4계층으로 실내 공간을 표현하고, 레이저 장소 분류·비전 객체 인식·언어 대화를 결합해 '이 방은 거실이다' 같은 공간 개념을 추론하는 로봇 시스템 논문 리뷰"
category: "Indoor Navigation"
tags:
  - paper-review
  - conceptual-map
  - topological-map
  - spatial-representation
  - ontology
  - human-robot-interaction
aliases:
  - Conceptual Spatial Representations for Indoor Mobile Robots
  - Zender 2008
paper_title: "Conceptual spatial representations for indoor mobile robots"
authors:
  - Hendrik Zender
  - Óscar Martínez Mozos
  - Patric Jensfelt
  - Geert-Jan M. Kruijff
  - Wolfram Burgard
venue: "Robotics and Autonomous Systems, 56(6), 493–502"
year: 2008
paper_type: journal
doi: "10.1016/j.robot.2008.03.007"
url: "https://doi.org/10.1016/j.robot.2008.03.007"
verification: full-text
draft: true
---

> [!info] 검증 범위
> 서지정보는 출판사와 저자(KTH) 페이지에서, 초록·방법·수치는 원문 전문(ScienceDirect PDF)에서 확인했다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | Conceptual spatial representations for indoor mobile robots |
| 저자 | Hendrik Zender(DFKI), Óscar Martínez Mozos(Univ. Freiburg), Patric Jensfelt(KTH), Geert-Jan M. Kruijff(DFKI), Wolfram Burgard(Univ. Freiburg) |
| 연도 | 2008 |
| 저널/학회 | Robotics and Autonomous Systems, Vol. 56, Issue 6, pp. 493–502 |
| 연구 분야 | Spatial Representation, Conceptual Mapping, Human-Robot Interaction |
| 핵심 기술 | EKF Line SLAM, AdaBoost 장소 분류, SIFT 객체 인식, Navigation Graph, OWL-DL 온톨로지, 상황 대화 |
| DOI | [10.1016/j.robot.2008.03.007](https://doi.org/10.1016/j.robot.2008.03.007) |
| 원문 | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0921889008000304) |
| 연구비 | EU FP6 IST Cognitive Systems Integrated Project "CoSy" |
| 피인용 | 검색 데이터 기준 약 294~350회(브리핑 작성 시점) |

## 1. 연구 배경

이 논문은 단일 지도 하나로 모든 것을 해결하지 않고, 추상화 수준이 서로 다른 여러 공간 표현을 두는 접근을 제시한다.

```text
Metric representation
↓
Topological representation
↓
Conceptual representation
```

지도가 "좌표상 이곳"이라는 수준에서 "여기는 corridor", "저기는 office", "이 공간은 저 공간과 연결"이라는 수준으로 올라간다.

출발점은 가정용·노인 돌봄 로봇 같은 서비스 로봇이다. 이런 로봇은 훈련받은 운영자가 아니라 일반인과 상호작용해야 한다. 사람에게 가장 직관적인 소통 수단은 말이므로, 로봇이 사람과 대화하려면 사람과 같은 개념으로 사물과 현상을 가리켜야 한다. 이를 위해 로봇은 사람이 만든 환경의 공간적·기능적 속성을 사람처럼 이해해야 한다. 예를 들어 "거실"은 단순한 라벨이 아니라 특정 구조를 가지며 소파나 TV가 있는 장소를 뜻하는 의미 표현이다. 동시에 로봇은 안전하고 신뢰성 있게 이동할 수 있어야 한다.

공간 인지 연구도 근거로 쓰인다. 사람은 공간을 부분적으로 계층적인 방식으로 표현하며, 그 기본 단위는 경계가 어느 정도 분명한 topological region이다. 경계는 물리적일 수도, 지각적일 수도, 순전히 주관적일 수도 있다. 뚜렷한 경계가 없는 자연 환경에서도 사람은 두드러진 랜드마크를 묶어 공간을 topology 계층으로 나눈다. 또한 사람은 기본 수준 범주(basic-level category)로 사물을 부르며, 이 범주가 사물과 어떻게 상호작용하고 어떻게 언급하는지를 결정한다.

이 논문은 실내 공간을 metric에서 개념 수준까지 계층적으로 표현하려는 연구를 학술적으로 설명할 때 좋은 뿌리가 된다.

## 2. 연구 Gap

**기존 연구의 한계**

- Kuipers의 Spatial Semantic Hierarchy(SSH), Krieg-Brückner의 Route Graph 같은 인지 기반 다계층 지도는 topological map을 중심 추상화 계층으로 둔다. topology 개체를 범주화하는 추가 계층은 없다.
- Galindo et al.(공간·개념 두 계층을 anchoring으로 연결), Vasudevan et al.(객체 기반 확률 계층), Beeson et al.(HSSH) 같은 다계층 모델은 사용자 상호작용을 상대적으로 덜 강조한다.
- 박물관 안내 로봇(Rhino, Robox)은 정확한 metric 표현에 의존하고 대화가 제한적이다. 대화 능력이 있는 로봇(BIRON 등)은 개념적 공간 지식과 언어 의미가 상황 인식에 연결되는 정도가 약하다.

**본 연구가 해결하려는 Gap**

로봇이 타고난(사람과 유사한) 공간 조직 개념을 여러 저수준 센서 시스템과 결합해, 환경의 내부 표현을 스스로 구축하는 방법을 제시한다. 신뢰성 있는 로봇 제어와 사람과 유사한 개념화를 모두 충족하도록 추상화 수준이 다른 지도를 계층으로 둔다. 개념 지식은 센서로 획득한 지식, 대화로 들은 지식, 타고난 지식, 추론으로 얻은 지식을 융합해 만든다. 이를 통해 공간을 단순히 인스턴스로 표현하는 데 그치지 않고 범주화까지 할 수 있다.

## 3. 연구 질문

논문이 초점으로 밝힌 문제는 다음과 같다.

> 로봇이 공간 조직에 관한 타고난(사람과 유사할 수 있는) 개념을 가지고 있을 때, 이 개념을 여러 저수준 센서 시스템과 결합해 환경의 내부 표현을 어떻게 스스로 구축할 수 있는가?

이를 바탕으로 재구성하면 다음과 같다.

1. 로봇 navigation에 필요한 표현과 사람의 공간 개념화에 맞는 표현을 어떻게 하나의 계층 구조로 연결할 수 있는가?
2. 공간의 종류(방, 복도, 거실 등)를 기하 속성과 그 안의 객체로 어떻게 범주화할 수 있는가?
3. 언어 대화가 지도 획득과 공간 지식 공유에 어떻게 기여할 수 있는가?

## 4. 핵심 기여

- 기존 방식: metric 또는 topological 지도 중심. 인지 기반 모델도 topology 계층이 최상위
- 문제: 사람이 쓰는 공간 개념(방의 종류, 기능)과 연결되지 않아 대화와 기능 기반 추론이 어렵다.
- 제안 방법
  - 4계층 공간 표현: metric line map → navigation graph → topological map → conceptual map
  - 레이저 기반 장소 분류(방·복도·문)와 비전 기반 객체 인식을 하위 계층에 결합
  - OWL-DL 온톨로지와 Description Logic 추론기로 "방 + 소파 → 거실" 같은 개념 추론
  - 대화로 들은 지식(asserted knowledge)을 지도에 반영하고, 지도를 대화에 활용
- 개선점: 로봇이 "I am in a room"에서 "I am in the living room"으로 공간을 더 구체적으로 이해하고 사람과 공유할 수 있다.

## 5. 연구 방법론

### 연구 대상 / 데이터

- 로봇: ActivMedia PeopleBot
- 센서: SICK 레이저 거리 측정기(전방 180°), pan-tilt-zoom 카메라
- 대화: 블루투스 헤드셋 연결 음성 인식, 로봇 내장 스피커 TTS
- 장소 분류 실험: KTH CAS 건물. 6층 궤적으로 학습하고, 구조가 비슷한 7층에서 반대 방향의 두 궤적으로 평가
- 시나리오: 사용자가 로봇을 데리고 집 안을 안내하며 방과 물건을 알려주는 "home tour"

### 시스템 구조

세 하위 시스템이 공간 표현을 만들고 사용한다: 센서 입력을 해석하는 인지(perception) 하위 시스템, 상황 대화를 담당하는 소통(communication) 하위 시스템, 센서 기반 지도와 사람 수준 공간 표현을 잇는 다계층 개념 공간 지도 하위 시스템이다.

```text
[Conceptual Map]    OWL-DL 온톨로지(TBox) + 인스턴스(ABox)
                    area → room / corridor → living room, kitchen, office ...
                    hasObject 관계, DL 추론기
        ↑ area 인스턴스, 객체 인스턴스
[Topological Map]   문(doorway) 노드로 나뉜 navigation 노드 집합 = area
                    area 범주는 소속 노드 분류의 다수결
        ↑
[Navigation Graph]  로봇이 1 m 이동할 때마다 노드 생성, 이동 순서대로 연결
                    노드 분류: room / corridor / doorway
                    인식된 객체는 가장 가까운 노드에 연결
        ↑
[Metric Map]        EKF SLAM 기반 선분(line) 지도 — 벽 등 직선 구조
```

### 계층별 구성

**Metric map**

- SLAM 모듈이 레이저 스캔에서 선분을 추출하고 Extended Kalman Filter로 통합한다. 선분은 대부분 정적인 벽에 해당하므로 위치 추정의 기준이 된다.
- 선분 지도는 자유 공간이 아니라 선으로 표현되는 부분만 기술하므로 navigation을 온전히 지원하기에는 부족하다. 좌표계도 로봇 내부 기준이라 사람과 대화할 공통 기반이 되지 못한다.

**Navigation graph**

- 로봇이 가장 가까운 기존 노드에서 일정 거리(1 m) 이상 움직이면 새 노드를 떨어뜨리고, 생성 순서(로봇 궤적)대로 연결한다. 자유 공간과 그 연결(도달 가능성)을 모델링하며, 이미 방문한 영역의 계획과 자율 이동에 쓰인다.
- 여기서 공간에 semantic 정보가 붙는다. 노드마다 room, corridor, doorway 중 하나를 부여한다.
- 문(doorway)은 로봇이 문 폭의 개구부를 통과할 때 검출해 추가한다. 개구부의 폭과 방향을 함께 저장한다. 문 모델에 관한 가정은 "로봇이 통과하는 좁은 개구부"뿐이다. 여닫이나 미닫이 문짝, 문 주변 구조 같은 가정은 두지 않는다.
- 방과 복도는 그 위치에서의 레이저 관측으로 분류한다. 스캔과 그 다각형 근사에서 회전 불변 기하 특징(연속 빔 간 평균 거리, 스캔 영역의 둘레, 스캔 다각형을 근사한 타원의 장축 등)을 뽑고, 약한 가설을 AdaBoost로 강한 분류기로 만든다. 지도학습이지만 학습 환경과 다른 환경에도 잘 일반화된다.
- 노드는 1 m마다만 생기므로, 직전 N개 pose의 분류 결과를 단기 기억에 저장했다가 다수결로 노드를 분류한다. 저자들은 이 방식으로 노드 분류가 크게 개선되었다고 보고한다.

**Topological map**

- Navigation graph 노드를 area로 나눈다. area는 doorway 노드로 분리된, 서로 연결된 노드 집합이다.
- 하위 계층의 정확한 형상과 경계는 방과 복도라는 거친 범주 구분으로 추상화된다. area 범주는 소속 노드 분류 결과의 다수결로 정한다.
- Topological area와 인식된 객체는 conceptual map으로 넘어가 각 범주의 인스턴스가 된다.

**Conceptual map**

- 실내 사무 환경의 OWL-DL 온톨로지를 손으로 만들었다. 최상위 개념은 area와 object이고, area는 room과 corridor로 나뉜다. room의 하위 개념(거실, 부엌 등 기본 수준 범주)은 그 안에서 발견되는 객체(hasObject 관계)로 정의한다.
- 온톨로지(TBox)는 실행 중 바뀌지 않는 타고난 지식이고, 센서와 대화로 얻은 정보는 인스턴스(ABox)로 쌓인다.
- 지식 유형은 네 가지다.
  - 획득 지식(acquired): 지도 작성 중 얻은 area 인스턴스, room/corridor 분류, 인식된 객체와 hasObject 관계
  - 주입 지식(asserted): 안내 중 사용자가 "여기는 복도야", "이게 충전 스테이션이야"라고 말한 내용
  - 타고난 지식(innate): 사무 환경 상식 온톨로지
  - 추론 지식(inferred): DL 추론기가 위 지식을 결합해 얻은 지식. 예를 들어 "room으로 분류되고 소파가 있음" → "living room". 반면 "corridor에 충전 스테이션이 있음"에서는 더 구체적인 범주가 추론되지 않는다.
- 사람마다, 상황마다 같은 방을 다르게 부를 수 있으므로(부엌 vs 휴게실) 한 area에 여러 분류를 허용한다.

### 인지 모듈

- 사람 추적: 레이저로 사람을 검출하고 따라간다.
- 객체 인식 방법 1: 모든 학습 이미지의 SIFT 특징을 하나의 KD-tree에 넣고 투표로 후보 객체를 추린 뒤 표준 SIFT 매칭으로 검증한다. 320×240 저해상도 이미지라 TV나 화분 같은 큰 물체에 한정된다. 객체를 분할하지 않고 학습하므로 사실상 객체 인식이 아니라 장면 인식에 가깝다.
- 객체 인식 방법 2: 컵이나 책 같은 작은 물체를 위해 검출과 인식을 분리한다. receptive field cooccurrence histogram(RFCH) 기반 주의 메커니즘으로 후보 위치를 찾고, 줌으로 확대해 확인한다. 작은 물체를 먼 거리에서도 찾을 수 있지만, 탐색 시간이 데이터베이스 객체 수에 대략 비례해 느리다.

### 상황 대화

- 음성 인식 결과를 OpenCCG의 Combinatory Categorial Grammar 파서로 분석해 의미 표현(logical form)을 만든다.
- 앞선 대화 맥락과 연결(상호 참조 해결)하고, 과거·현재의 시각-공간 맥락과 계획된 미래 사건에 발화 내용을 grounding한다.
- 대화 행동은 information state 방식과 과업 지향 관점을 결합해 모델링한다.

### 사용 기술

- ActivMedia PeopleBot, SICK 레이저(180°), PTZ 카메라
- EKF 기반 line SLAM
- AdaBoost 기반 레이저 장소 분류
- SIFT, KD-tree, RFCH
- OWL-DL 온톨로지, Description Logic 추론기
- OpenCCG 파서, 음성 인식, TTS

### 평가 방법

- 장소 분류: 학습 층과 다른 층의 궤적에서 pose 단위 분류율
- 통합 시스템: home tour 시나리오 실험의 정성적 능력 평가(대화 응답, 개념 추론)

## 6. 핵심 결과

- 장소 분류: KTH CAS 건물 6층 궤적으로 학습하고 7층에서 반대 방향 두 궤적을 분류했을 때, 모든 pose의 분류율은 93.18%~96.8%였다.
- 사람과 마주 보는 상황의 문제 해결
  - 레이저가 전방 180°만 보므로, 국소 occupancy grid에서 ray tracing으로 후방 빔을 시뮬레이션했다. 장애물에 닿지 않는 빔은 양옆의 알려진 빔 값으로 보간했다.
  - 사용자가 시야를 많이 가리므로 모든 좌표를 분류하지 않고 navigation 노드만 다수결로 분류했다.
  - 카메라도 대부분 사용자만 보므로, 사용자가 "주변을 둘러봐"라고 지시하게 했다.
- 문 검출: 좁은 개구부를 찾는 방식은 문과 비슷한 폭의 틈이 많아 오검출이 있었다. 로봇이 실제로 통과한 개구부만 받아들여 오검출을 크게 줄였고, 남은 오검출은 확인 대화(clarification dialogue)로 처리했다.
- 개념 추론: 사용자가 반복해서 로봇에게 위치를 물었을 때, 처음에는 area가 room으로만 분류되어 "I am in a room"이라고 답했다. 소파와 TV를 인식한 뒤에는 온톨로지 추론으로 거실을 추론해 "I am in the living room"이라고 답했다.

## 7. 결론 및 시사점

저자들은 개념이 전형적인 사무 실내 환경의 공간적·기능적 속성을 나타내는 개념 표현 생성 방법을 통합적으로 제시했다고 결론짓는다. 표현은 추상화 수준이 다른 여러 지도로 이루어지며, 각 수준의 정보는 레이저, 카메라, 자연어 처리 시스템 같은 서로 다른 모달리티에서 온다. 통합 시스템 평가는 이 접근이 높은 수준의 사람-로봇 소통과 개념 표현을 제공함을 보여준다고 저자들은 평가한다.

저자들은 공간을 "인식한다"는 것의 의미도 짚는다. SLAM 관점에서 area는 대략 "둘러싸인 공간"이며, 관측된 선형 구조를 벽으로 보고 문을 area 사이 전이로 본다. 이는 적절한 추상화지만 area를 구분하기에는 부족하다. 사람은 공간을 기하뿐 아니라 기능으로도 범주화하고, 기능은 주로 그 안의 객체에서 나온다. 따라서 기능-기하 해석을 위해서는 topological area와 객체 지식을 통합해야 한다.

- Indoor Navigation / IndoorGML: metric → navigation graph → topological area → conceptual map 구조는 IndoorGML이 기하 표현, topology(NRG), 공간 semantic을 분리해 다루는 방식과 철학적으로 닮았다. 특히 "문 노드로 나뉜 연결 노드 집합 = area"라는 정의는 IndoorGML의 CellSpace와 문을 통한 Transition 개념과 가깝다.
- SLAM / Robotics: 이후 3D scene graph 연구(DSG, Kimera, Hydra)의 계층적 공간 표현으로 이어지는 개념적 선행 연구로 볼 수 있다. 로봇이 통과한 개구부로 문을 검출하는 발상은 이후 스캐너 궤적으로 문을 검출하는 연구(Flikweert et al. 2019)와 같다.
- Knowledge Graph / Ontology: 공간 유형을 그 안의 객체로 정의하는 OWL 온톨로지는 공간 knowledge graph 설계의 초기 사례다.
- Digital Twin: 공간의 기능적 속성을 모델에 명시해야 운영 분석이 가능하다는 점에서 건물 Digital Twin의 공간 분류 체계 설계와 연결된다.

## 8. 연구의 한계

### 저자가 명시한 한계

- 문 검출은 로봇이 지나간 곳에서만 가능하다. 복도를 걷다 사용자가 어떤 방을 언급할 때처럼 아직 가지 않은 공간을 추론하려면 멀리 있는 문도 검출할 수 있어야 한다.
- Area는 검출된 문으로만 나눈다. 홀에서 복도로의 전환처럼 형상 차이만으로 구분되는 경계나, 부엌 겸 거실을 식사·조리 영역으로 나누는 기능적 구분은 처리하지 못한다. 객체 배치와 장소 분류 확률의 변화를 추가 단서로 쓰는 방법을 연구 중이라고 밝힌다.
- 잘못 획득하거나 주입된 지식이 추론 지식의 되돌릴 수 없는 오류로 이어질 수 있으므로 비단조(non-monotonic) 추론이 필요하다. 대안으로, 단조 DL 추론기의 ABox에 공간 개념 지식을 계속 유지하지 않고 필요할 때만 가장 최근의 신뢰할 만한 지식을 넘기는 방식을 제안한다.
- 레이저가 전방 180°만 보고, 사용자가 시야를 가린다.
- 방법 1의 객체 인식은 저해상도라 큰 물체에 한정되고, 분할 없이 학습해 배경이 우세하면 장면 전체를 인식하게 된다. 방법 2는 분할된 학습 이미지가 필요해 새 객체를 등록하기 어렵고(TV 같은 큰 물체는 특히), 탐색 시간이 객체 수에 비례한다.

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 정량 평가는 장소 분류(한 건물의 두 층) 하나뿐이다. 문 검출률, 객체 인식률, 개념 추론 정확도, 대화 성공률은 수치로 제시되지 않는다.
- 온톨로지가 사무 환경을 대상으로 손으로 만들어졌다. 실험 시나리오는 가정(home tour, 거실)인데 온톨로지는 "사무 환경"으로 설명되어, 적용 범위가 다소 모호하다.
- 2D 레이저 기반이어서 다층 건물의 층간 연결은 다루지 않는다.
- Navigation graph가 로봇 궤적 순서로 연결되므로, 로봇이 가 보지 않은 연결은 그래프에 없다.

## 9. 비판적 읽기

### 연구 설계

- 강점: 공간 인지 이론에 근거해 계층 구조를 설계했고, 인지·대화·지도 하위 시스템을 실제 로봇에 통합했다. 통합이 각 모듈의 약점을 어떻게 보완하는지(통과한 개구부만 문으로 인정, 확인 대화로 오검출 처리)를 구체적으로 보였다.
- 약점: 시스템 통합과 능력 시연 중심이며, 통합 시스템 전체에 대한 정량 평가가 없다.
- 개선 방향: 여러 환경에서 area 분할 정확도와 개념 추론 정확도를 측정할 수 있다.

### 데이터

- 장소 분류는 한 건물의 두 층에서 평가했다. 학습 층과 평가 층이 "비슷한 구조"라고 명시되어 있어, 일반화 주장의 범위는 제한적이다.

### Baseline / 비교군

- 정량 비교군은 없다. 관련 연구와는 서술 수준에서 비교한다. 노드 다수결 분류가 "크게 개선되었다"는 주장도 비교 수치 없이 제시된다.

### 평가 지표

- 장소 분류율은 적절한 지표다. 연구 목표인 "사람과 유사한 개념화"와 "사람-로봇 소통"을 평가할 지표는 제시되지 않는다.

### 데이터 신뢰성

- 사용자 발화로 얻은 지식은 오류 가능성이 있으며, 저자들도 이것이 추론 오류로 이어질 수 있다고 지적한다.

### 주장과 결과의 관계

- "높은 수준의 사람-로봇 소통과 개념 표현을 제공한다"는 결론은 시나리오 시연에 근거한다. 정량적으로 검증된 명제로 읽으면 안 된다.

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 낮음 | EU FP6 CoSy 프로젝트 지원. 상업적 이해충돌 정보는 확인 가능한 정보 없음 |
| 선택 편향 | 중간 | 장소 분류를 저자 소속 기관(KTH) 건물의 비슷한 두 층에서 평가 |
| 확증 편향 | 중간 | 성공 시나리오 중심 서술. 다만 문 검출 오검출, 비단조 추론 필요성 등 한계를 명시 |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 중간 | 유럽 사무 건물 구조와 사무 환경 온톨로지에 기반 |

## 11. 주요 전문 용어

### Metric Map

좌표와 거리 기반으로 공간의 기하를 표현한 지도다. 이 논문에서는 벽 같은 직선 구조를 선분으로 표현한 line map이다.

### Navigation Graph

로봇이 일정 거리를 이동할 때마다 떨어뜨린 노드와 그 연결로 자유 공간의 도달 가능성을 표현한 그래프다.

### Topological Map

장소(area)와 그 연결로 공간을 표현한 지도다. 이 논문에서는 문 노드로 나뉜 navigation 노드 집합을 하나의 area로 본다.

### Conceptual Map

공간과 객체를 "거실", "복도", "소파" 같은 사람의 개념 범주로 표현하고, 범주 간 관계로 추론하는 지도다.

### OWL-DL / Description Logic

OWL-DL은 Description Logic에 기반한 온톨로지 언어다. 개념(TBox)과 인스턴스(ABox)를 구분해 표현하고, 추론기로 명시되지 않은 사실을 도출할 수 있다.

### Basic-level Category

사람이 사물을 부를 때 가장 자연스럽게 쓰는 범주 수준이다. "가구"나 "안락의자"보다 "의자"가 기본 수준 범주다.

### Situated Dialogue

로봇과 사람이 같은 물리 환경을 공유하면서 그 환경을 주제로 나누는 대화다. 예를 들어 "여기가 부엌이야"라고 알려주는 식이다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

- ActivMedia PeopleBot, SICK 레이저, PTZ 카메라
- EKF line SLAM
- AdaBoost 기반 장소 분류, 후방 빔 시뮬레이션(occupancy grid ray tracing)
- SIFT + KD-tree, RFCH 주의 메커니즘
- OWL-DL 온톨로지, DL 추론기
- OpenCCG 기반 대화 시스템

### 실무 구현 시 적용 가능한 기술

아래는 서비스 구현 시 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**Indoor 공간 모델**
- IndoorGML(CellSpace, NRG, 공간 유형 속성), IFC IfcSpace(공간 용도 속성)

**Ontology / Knowledge Graph**
- OWL, RDF, SPARQL, Neo4j

**Spatial DB / 경로**
- PostgreSQL + PostGIS + pgRouting

**AI**
- 장소 분류 모델, LLM 기반 자연어 공간 질의 인터페이스

## 13. 커리어 관점

### 공부해야 할 기술

- Metric, topological, semantic 지도의 차이와 결합 방식
- IndoorGML 구조(Primal/Dual space, NRG, Multi-layered space model)
- 온톨로지 설계와 DL 추론 기초
- 장소 분류와 객체 인식 기초

### 실무 연결

- 공간 관점: 실내를 먼저 area(방·복도)와 그 연결로 나누고, 각 area에 기능 범주를 부여한 뒤, 그 안에 객체를 배치하는 순서는 실내 공간 모델링의 기본 틀이다. 공장이라면 구역을 먼저 정의하고 그 안의 설비로 구역의 기능을 추론하는 식으로 응용할 수 있다.
- 실내 지도 서비스의 공간 유형 체계(방 용도 분류) 설계
- 시설관리 시스템의 공간 계층 모델링과 온톨로지 기반 공간 질의
- 자연어 기반 실내 길찾기 인터페이스

### 기술 면접으로 연결될 수 있는 질문

- Metric map과 topological map을 함께 쓰는 이유는 무엇인가?
- IndoorGML의 multi-layered space model과 로봇의 다계층 지도는 어떻게 대응되는가?
- 공간의 "기능적 속성"을 지도에 표현해야 하는 사례는 무엇인가?
- 온톨로지에서 TBox와 ABox의 차이는 무엇인가?
- 문 검출로 공간을 나누는 방식의 한계는 무엇이며, 개방형 공간은 어떻게 나눌 수 있는가?

## 14. 후속 연구

### 저자가 제안한 Future Work

- 객체의 존재와 배치, 레이저 장소 분류 확률의 변화를 추가 단서로 삼아 문 없이도 공간을 기능적·기하적 영역으로 분할
- 가 보지 않은 공간에 대해 추론할 수 있도록 멀리 있는 문 검출
- 비단조 추론 도입, 또는 필요할 때만 최근의 신뢰할 만한 지식을 개념 지도로 전달하는 방식
- 객체 인식에 top-down 정보 활용(거실에서는 커피 머신을 찾지 않는 식으로 탐색 대상 축소)

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- 개념 계층을 3D scene graph의 room 노드 라벨링으로 연결
- 언어 대화 대신 vision-language 모델로 공간 개념을 자동 부여
- 개념 지도를 IndoorGML semantic 속성과 온톨로지로 표준화해 교환

## 15. 논문 읽기 가이드

**1순위 — Fig. 7 (다계층 지도)과 5절**

네 계층이 무엇을 표현하고 어떻게 연결되는지 파악한다.

**2순위 — 5.5절 (Spatial knowledge processing)과 Fig. 9, 10**

획득·주입·타고난·추론 지식이 개념 지도에서 어떻게 결합되는지 이해한다.

**3순위 — 7절 (System integration)**

장소 분류 결과, 문 검출 개선, "I am in the living room" 추론 사례를 확인한다.

**4순위 — 7.4절과 8절**

문 검출과 area 분할의 한계, 비단조 추론 필요성을 확인한다.

## 16. 핵심 정리

- 하나의 지도로 모든 것을 해결하지 않고, metric → navigation graph → topological area → conceptual map의 4계층으로 공간을 표현한다.
- Area는 문 노드로 나뉜 연결 노드 집합이며, 그 범주(방·복도)는 소속 노드 분류의 다수결로 정한다.
- 공간의 기능은 그 안의 객체로 정의된다. "방 + 소파·TV → 거실"처럼 온톨로지 추론으로 공간 개념을 얻는다.
- 장소 분류는 다른 층에서도 93.18~96.8%의 분류율을 보였다. 통합 시스템 전체는 시나리오 시연으로만 평가되었다.
- 이 계층적 사고는 IndoorGML과 3D scene graph 모두의 개념적 뿌리로 읽을 수 있다.

## 관련 글

- [[2011-hybrid-metric-topological-navigation|Navigation in Hybrid Metric-Topological Maps]] — metric과 topology의 역할 분리
- [[2008-towards-semantic-maps-mobile-robots|Towards Semantic Maps for Mobile Robots]] — 기하 지도에 의미 결합
- [[2019-point-cloud-to-indoorgml-navigation-graph|Point Cloud → IndoorGML Navigation Graph]] — 궤적 기반 문 검출과 공간 분할
- [[2020-3d-dynamic-scene-graphs|3D Dynamic Scene Graphs]] — 계층적 공간 표현의 현대적 형태
