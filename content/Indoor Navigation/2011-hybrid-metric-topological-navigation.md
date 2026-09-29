---
title: "Navigation in Hybrid Metric-Topological Maps — 국소 Occupancy Grid와 전역 Topological Graph의 역할 분리 (ICRA 2011)"
date: 2026-09-28
description: "Graph SLAM의 pose graph 위에 navigation graph와 국소 occupancy grid를 겹쳐, 전역 occupancy grid를 만들지 않고도 전역 metric 지도 수준의 경로를 얻는 하이브리드 navigation 시스템 논문 리뷰"
category: "Indoor Navigation"
tags:
  - paper-review
  - topological-map
  - metric-map
  - path-planning
  - graph-slam
  - mobile-robot
aliases:
  - Navigation in Hybrid Metric-Topological Maps
  - Konolige 2011
paper_title: "Navigation in hybrid metric-topological maps"
authors:
  - Kurt Konolige
  - Eitan Marder-Eppstein
  - Bhaskara Marthi
venue: "IEEE International Conference on Robotics and Automation (ICRA), pp. 3041–3047"
year: 2011
paper_type: conference
doi: "10.1109/ICRA.2011.5980074"
url: "https://ieeexplore.ieee.org/document/5980074/"
verification: full-text
---

> [!info] 검증 범위
> 서지정보는 Crossref에서, 초록·방법·수치는 원문 전문(IEEE Xplore PDF)에서 확인했다.

## 논문 정보

| 항목 | 내용 |
|---|---|
| 제목 | Navigation in Hybrid Metric–Topological Maps |
| 저자 | Kurt Konolige, Eitan Marder-Eppstein, Bhaskara Marthi (Willow Garage) |
| 연도 | 2011 |
| 저널/학회 | IEEE ICRA 2011, pp. 3041–3047 |
| 연구 분야 | Robot Navigation, Hybrid Map Representation, Graph SLAM |
| 핵심 기술 | Pose Graph, Navigation Graph, Local Occupancy Grid, Dijkstra, A*, ROS Navigation Stack |
| DOI | [10.1109/ICRA.2011.5980074](https://doi.org/10.1109/ICRA.2011.5980074) |
| 원문 | [IEEE Xplore](https://ieeexplore.ieee.org/document/5980074/) |
| 피인용 | 검색 source에 따라 약 118~150회(브리핑 작성 시점), Crossref 기준 97회(2026-09 확인) |
| 코드 | ROS의 일부로 오픈소스 공개(원문 기준) |

## 1. 연구 배경

이 논문은 metric map과 topological graph를 분리해서 함께 사용한다.

```text
Metric Map
+
Topological Graph
```

대부분의 SLAM 시스템은 작업 공간 전체의 전역 metric map을 만든다. 저자들은 전역 metric map이 작은 영역에서는 편리하지만 규모가 커지면 세 가지 비효율이 생긴다고 지적한다.

- 큰 metric map에서의 경로 계획은 빠르게 다루기 어려워진다.
- 큰 루프를 닫을 때 전역 일관성을 유지하는 비용이 최악의 경우 지도 크기의 세제곱으로 늘어난다(EKF와 제약 기반 지도 모두).
- 주차 건물 같은 다층 구조를 표현하려면 2D roadmap이 아니라 3D 공간 전체를 다뤄야 해 표현이 더 커진다.

여러 연구자는 navigation 목적이라면 전역적으로 일관된 metric map이 꼭 필요하지 않다고 봐 왔다. 넓은 공간에서는 대략적인 metric 정보가 있는 topological 연결로 계획이 충분하고, 국소 metric 정보는 정밀한 위치 추정과 장애물 회피에 쓰면 된다. 이 생각은 submap을 쓰는 SLAM 연구로 이어졌다. 그런데 저자들은 지도를 만드는 가장 큰 이유인 navigation 자체에 대해서는 연구가 의외로 적었다고 본다.

이 역할 분리는 실내 공간 표준 IndoorGML이 존재하는 이유와 가장 가까운 로봇 연구 사례 중 하나로 볼 수 있다. IndoorGML도 정밀 기하와 별도로 공간 간 연결관계(topology)를 navigation의 핵심 표현으로 둔다.

## 2. 연구 Gap

**기존 연구의 한계**

- 전역 metric map은 계획 비용, 루프 폐합 시 일관성 유지 비용, 다층 구조 표현 비용이 규모에 따라 크게 늘어난다.
- Topological mapping 계열은 지각적으로 인식 가능한 장소 사이를 벽 따라가기 같은 행동 기반 방식으로 이동하는 경우가 많았다.
- 가장 가까운 하이브리드 연구인 Thrun(1998)은 전역 occupancy grid를 먼저 만든 뒤 Voronoi 다이어그램으로 roadmap을 추상화했다. topological 경로는 grid 경로보다 몇 퍼센트 더 길었다. Zivkovic et al.(2006)은 graph-cut clustering 기반의 비슷한 시스템을 제시했지만, 계산 시간과 경로 길이가 Thrun의 방식보다 컸다.
- Submap 기반 SLAM은 주로 지도 작성의 확장성 문제에 집중했고, navigation 설계는 상대적으로 덜 다뤄졌다.

**본 연구가 해결하려는 Gap**

전역 occupancy grid를 한 번도 만들지 않고, graph SLAM의 pose graph로부터 navigation graph와 국소 grid를 구성한다. 전역 계획은 graph에서, 실제 이동은 국소 grid에서 수행해 전역 metric map 수준의 경로 품질을 유지하면서 규모 확장성을 확보한다.

## 3. 연구 질문

논문의 목적과 실험 구성을 바탕으로 재구성하면 다음과 같다.

1. 전역 occupancy grid 없이 pose graph와 국소 grid만으로 실용적인 navigation 시스템을 만들 수 있는가?
2. 이 하이브리드 방식의 경로가 전역 metric map 기반 경로만큼 짧은가?
3. 국소 grid 크기와 navigation graph 밀도는 경로 품질에 어떤 영향을 주는가?
4. Graph 기반 계획은 metric 계획보다 얼마나 빠른가?

## 4. 핵심 기여

저자들이 제시한 주된 기여는 국소 grid 구조를 위치 추정과 navigation에 쓰는 설계, 그리고 pose graph 구조로부터 topological map과 planner를 만든 것이다. navigation graph는 pose graph와 관련되지만 두 가지 추가 요건을 만족해야 한다.

- 일관성: 두 노드 사이에 유효한 metric 경로가 있을 때에만 두 노드를 연결한다.
- 효율성: 실제 실행 경로가 전역 metric map의 경로만큼 짧아야 한다.

기존 방식 → 문제 → 제안 → 개선 관계로 정리하면 다음과 같다.

- 기존 방식: 전역 occupancy grid를 만든 뒤 계획(또는 grid에서 roadmap 추출)
- 문제: 대규모 환경에서 grid 재구성이 병목이 되고, 지도 변화에 대응하기 어렵다.
- 제안 방법: pose graph 노드에 저장된 센서 데이터로 크기가 제한된 국소 grid만 만든다. navigation graph edge는 해당 grid 안에서 A*로 실제 통과 가능성을 확인해 생성한다.
- 개선점: 전역 grid 없이도 경로 길이가 전역 metric 계획과 거의 같고, 계획이 훨씬 빠르며, 지도를 국소적·증분적으로 갱신할 수 있다.

## 5. 연구 방법론

### 연구 대상 / 데이터

- 센서: 2D 레이저 거리 측정기(laser range finder) 스캔
- 시뮬레이션: 사무실 환경
- 실제 로봇: Willow Garage PR2, 저자들의 사무실 환경

### 시스템 구조

지도는 세 계층으로 구성된다.

```text
Pose Graph  G = {N, E, S, C, P}
  N: 시간이 지나도 고정된 id를 가진 노드(로봇 pose)
  S: 노드별 센서 데이터(해당 노드 좌표계 기준 2D 레이저 스캔)
  E: 노드 pose 간 soft constraint
  C: 제약(두 좌표계 변환의 Gaussian)
  P: 전역 최적화된 노드 pose
↓
Navigation Graph  R = {G, O, E, C, S}
  O: 국소 occupancy grid 집합(각 grid는 중심 노드에 고정)
  C_o: grid에 포함된 노드, S_o: grid를 구성하는 데 쓰인 노드
  E: (n1, n2, o, c) — grid o 안에서 n1→n2 이동 가능, 비용 c(경로 길이)
↓
Local Occupancy Grids (navigation과 위치 추정에 사용)
```

위치 추정은 전역 pose가 아니라 `(n, p)` 형태다. n은 pose graph의 노드, p는 그 노드 좌표계에서의 SE(2) pose다.

SLAM 부분(논문의 초점은 아님)은 다음과 같다.

- Wheel odometry로 얻은 상대 pose와 새 레이저 스캔을 그래프 국소 이웃과 scan matching해 위치를 갱신한다.
- 위치가 기준 노드에서 일정 거리 이상 벗어나면 새 노드를 추가한다.
- 새 노드에는 세 종류 제약이 붙는다: wheel odometry 제약, 인접 노드와의 scan matching 제약, 그래프상 멀지만 최적화 pose가 가까운 노드와의 multiresolution scan matching 기반 loop closure 제약.
- Scan matching은 Karto SLAM 패키지의 오픈소스 matcher를 사용한다.
- Sparse pose adjustment로 그래프를 1초에 한 번 최적화한다. 매우 큰 그래프도 보통 수십 ms가 걸린다.

국소 grid와 navigation graph 구성은 다음과 같다.

- Grid는 표준 ray tracing으로 계산한다. 한 셀을 지나는 광선 수를 m, 그 셀에서 끝나는 광선 수를 n이라 할 때 `m > 2`이고 `n/m < 0.1`이면 free로 표시한다.
- 한 변이 r인 정사각형 grid는, 노드가 같은 중심의 한 변 αr 정사각형 안에 있으면 그 노드를 cover한다고 정의한다(α = 0.6). 모든 노드가 최소 하나의 grid에 cover되도록 필요할 때 새 grid를 추가한다.
- Grid 안에서 로봇 반경만큼 장애물을 팽창시킨 뒤 A*로 일정 거리 이내 노드 쌍 간 경로를 계산해 edge를 만든다. 그래서 navigation graph 구조는 로봇 형상에 따라 달라진다.
- Pose graph의 edge는 SLAM 제약이고, navigation graph의 edge는 grid 안의 이동 가능성이다. 두 그래프의 구조는 서로 다르다.

### Navigation 계획과 실행

```text
1. 로봇 근처 start node 선택 + 로봇→start node metric 경로
2. 목표 근처 goal node 선택 + goal node→목표 metric 경로
3. start ~ goal 사이 topological 경로 계획 (Dijkstra)
4. 현재 grid 안에 있는 마지막 waypoint까지 metric navigation 수행
5. 더 가까운 다른 grid 중심으로 넘어가면 4를 반복
```

- Start/goal node 선택: 로봇(또는 목표)에 중심이 가장 가까운 grid를 pose graph 상의 manifold 거리로 고른다. 그 grid에서 Dijkstra로 navigation function(potential)을 계산해 potential이 가장 낮은 노드를 고른다.
- Topological 계획: navigation graph에서 Dijkstra로 waypoint 목록을 만든다. waypoint를 모두 따라가면 경로가 graph 구조를 따라 우회하게 되므로, 현재 grid 안에서 유효한 경로가 있는 마지막 waypoint만 metric navigation에 전달한다. grid가 클수록 최적에 가깝고, 작을수록 메모리가 적게 든다.
- Metric navigation: ROS navigation stack을 사용한다. 센서의 장애물 정보를 3D voxel grid로 추적하고 2D로 투영한다. configuration space에서 A*로 계획하고 Dynamic Window Approach로 경로를 추종한다.
- 막힌 edge 처리: 지도에 없는 장애물로 waypoint에 도달할 수 없으면, 현재 topological 경로의 인접 waypoint 쌍마다 metric 경로를 확인해 통과 불가능한 link를 찾는다. 이 link를 blocked 목록에 넣고 대체 경로를 다시 계획한다.

### 지도 갱신

- Pose graph mapper는 새 노드, 새 edge, 기존 노드의 새 스캔, 노드 pose 변경을 증분적으로 방송한다.
- 정확한 방법은 영향받은 모든 grid를 다시 만드는 것이다. 하지만 최적화로 변화가 그래프 전체에 퍼지므로, 몇 초마다 변경을 반영하면 노드 수백 개 이상의 그래프에서는 불가능해진다.
- 그래서 변경 지점 주변 grid만 즉시 다시 계산하고, 나머지는 로봇이 그 영역에 들어갈 때 필요에 따라 다시 계산하는 opportunistic 전략을 쓴다. loop closure 직후에는 먼 영역의 연결 정보가 일시적으로 틀릴 수 있다.
- 막힌 경로는 모두 일시적이라고 가정한다. 사용자 지정 timeout과 함께 blocked 목록에 넣었다가 시간이 지나면 복원한다. 저자들은 이 전략이 명백히 최적이 아니고 영구적인 막힘에는 특히 나쁘지만, 실제로는 잘 동작했다고 밝힌다.

### 사용 기술

- Graph SLAM(pose graph), Karto scan matcher, sparse pose adjustment
- 2D laser range finder
- Ray tracing 기반 occupancy grid
- A*(grid 내 edge 생성, metric 계획), Dijkstra(topological 계획, navigation function)
- ROS navigation stack, Dynamic Window Approach
- PR2 로봇

### 평가 방법

- 경로 최적성: 전체 환경의 ground truth occupancy grid를 쓰는 ROS navigation stack(fully metric)의 주행 거리를 최적 기준으로 두고 비교
- Grid 크기와 graph 밀도 영향: 동적 장애물 시나리오의 정성 분석
- 계획 효율: metric planner와 graph planner의 경로 길이, 계획 시간 비교
- 실제 로봇 시험: PR2 주행 거리 비교

## 6. 핵심 결과

**시뮬레이션 최적성 (20개 목표점 순회, edge 최대 노드 간격 3m)**

| 방식 | 총 주행 거리 |
|---|---|
| 전역 Metric Map | 723.15 m |
| 20 m grid | 721.16 m |
| 15 m grid | 713.35 m |
| 10 m grid | 715.36 m |
| Graph 경로를 그대로 따라감(20 m grid) | 727.51 m |

- 세 grid 크기 모두 최적 경로 길이의 1% 이내였다.
- 5 m grid는 모든 waypoint에 도달하지 못했다. 저자들은 grid 크기가 waypoint를 따라갈 만큼만 크면, 경로 최적성은 grid 크기보다 navigation graph 밀도에 더 좌우된다고 관찰했다.
- Graph waypoint를 전부 정확히 밟게 해도 총 거리가 최적과 큰 차이가 없었다. 저자들은 실험 환경의 graph가 grid 크기와 관계없이 거의 최적 경로를 만들 만큼 조밀했다고 해석한다.

**Graph 밀도와 grid 크기**

- Navigation graph가 두 출입구 사이 공간의 중앙에만 지나가는 넓은 방에 동적 장애물을 두었다. 10 m grid는 장애물을 우회할 metric 정보가 부족해 통과하지 못했다. 15 m는 겨우 가능했고, 20 m는 충분히 우회했다.
- 조밀한 graph는 필요한 grid 크기를 줄이지만, 많은 노드 간 연결을 계산해야 해 유지 비용이 크다. 큰 grid는 edge 계산이 저렴한 대신 metric 계획 비용이 늘어난다.

**Metric vs Graph 계획 (사무 환경, 경로 17개)**

- Metric planner: 58 m × 45 m grid, 해상도 0.025 m/cell
- Graph planner: 노드 374개, 국소 grid 10 m, 해상도 0.025 m/cell
- 계획 시간: metric planner는 경로당 약 0.036~0.164초, graph planner는 약 0.0001~0.025초였다. 격차는 계획 거리가 길수록 커졌다.
- 경로 길이: 대부분 거의 같았다. 한 경우(metric 46.64 m, graph 38.12 m)는 metric planner가 비용 함수 때문에 장애물을 멀리 돌아갔고, graph planner는 좁은 통로를 통과해 더 짧았다.

**실제 로봇 (PR2, 사무 환경, waypoint 5개)**

| 방식 | 총 주행 거리 |
|---|---|
| 전역 Metric Map | 62.77 m |
| 10 m grid | 74.90 m |

- 저자들은 작은 10 m grid로도 metric planner와 비교할 만한 계획을 만들었다고 평가한다. 실험 중 동적 장애물로 edge가 막혔을 때 대체 link로 우회 경로를 만들었다.

## 7. 결론 및 시사점

저자들은 하이브리드 metric-topological navigation 시스템이 전역 metric map과 비슷한 성능을 낸다고 결론짓는다. 국소 metric grid로 국소 계획을 개선하고 전역 grid 계산을 피하므로, 시스템을 증분적으로 만들고 갱신할 수 있다.

두 지도의 질문은 다르다.

```text
Metric Map       "정확히 어디를 지나갈까?"
Topological Map  "어떤 공간들을 거쳐갈까?"
```

이 구조를 최신 공간 표현으로 치환하면 다음과 같이 해석할 수 있다.

```text
3DGS / Visual Map
→ Metric / perceptual localization

IndoorGML
→ Topological navigation
```

즉 정밀한 위치 추정은 3DGS 같은 metric·visual 표현이, 공간 간 경로 계획은 IndoorGML 같은 topology 표현이 담당하는 구조와 철학적으로 상당히 비슷하다.

다만 이 논문의 topology는 IndoorGML과 성격이 다르다. 이 논문의 노드는 방이나 복도 같은 의미 있는 공간이 아니라 "로봇이 레이저 스캔을 찍은 위치"다(저자들도 지각적으로 의미 있는 장소가 아니라고 명시한다). edge도 "특정 로봇이 이 grid 안에서 이 두 pose 사이를 갈 수 있다"는 로봇 형상 의존적 이동 가능성이다. IndoorGML의 CellSpace와 Transition은 사람이 이해하는 공간 단위와 그 연결을 표현한다.

- Indoor Navigation: "정밀 이동은 metric, 경로 계획은 topology"라는 역할 분리는 실내 길찾기 시스템 설계의 기본 원칙으로 쓸 수 있다.
- IndoorGML: navigation graph가 담당하는 역할을 로봇 관점에서 설명해 준다. semantic 공간 단위가 없는 로봇 topology와 표준 공간 topology를 연결하는 문제가 남는다.
- SLAM: 전역 지도를 만들지 않고 pose graph 위에서 직접 navigation한다는 설계는 대규모 SLAM 지도 활용의 한 방향을 보여 준다.
- Digital Twin: 대규모 시설에서 정밀 형상 데이터와 연결 그래프를 분리하고, 변화는 국소적으로 갱신한다는 설계 근거가 된다.

## 8. 연구의 한계

### 저자가 명시한 한계

- 지도 갱신 알고리즘은 단순한 수준이며 개선 여지가 크다. loop closure 이후 먼 영역의 연결 정보가 일시적으로 틀릴 수 있다.
- 막힌 경로를 모두 일시적인 것으로 가정하는 전략은 명백히 최적이 아니며, 영구적인 막힘에는 특히 나쁘다.
- 5 m grid는 너무 작아 모든 waypoint에 도달하지 못했다. graph가 희소한 곳에서는 작은 grid로 장애물을 우회하지 못한다.

### 추가적으로 고려할 한계

아래는 분석자의 의견이다.

- 실제 로봇 실험에서 10 m grid의 주행 거리(74.90 m)는 metric map(62.77 m)보다 약 19% 길다. 저자는 "comparable"하다고 평가하지만, 시뮬레이션의 1% 이내 결과와 비교하면 실제 환경에서는 격차가 훨씬 크게 나타났다. 원인 분석은 제시되지 않는다.
- 실제 로봇 실험은 waypoint 5개 규모로 작다.
- 계획 시간 비교는 "계획" 시간만 측정했다. navigation graph와 국소 grid를 만들고 유지하는 비용은 같은 표에서 비교되지 않는다.
- 노드가 의미 없는 스캔 위치이므로, "회의실로 가라" 같은 의미 기반 목표를 처리하려면 별도의 semantic 계층이 필요하다.
- 2D 레이저와 2D grid 기반이다. 도입부에서 다층 구조 표현을 동기로 들었지만, 실험은 단층 환경에서만 이루어졌다.

## 9. 비판적 읽기

### 연구 설계

- 강점: 전체 환경의 ground truth grid를 쓰는 metric planner라는 명확한 최적 기준과 비교했다. 시뮬레이션 결과를 실제 로봇에서 다시 확인했다.
- 약점: graph 밀도와 grid 크기의 관계는 한 장면의 정성적 예시로만 제시했다.
- 개선 방향: graph 밀도와 grid 크기를 체계적으로 바꾸며 성공률과 경로 길이를 측정할 수 있다.

### 데이터

- 시뮬레이션 사무 환경 하나와 실제 사무 환경 하나를 사용했다. 환경 유형의 다양성은 제한적이다.

### Baseline / 비교군

- 강점: 같은 ROS navigation stack 기반의 fully metric 방식을 기준으로 삼아 공정한 비교가 가능하다.
- 약점: 선행 하이브리드 방법(Thrun 1998, Zivkovic 2006)과의 직접 실험 비교는 없다. 관련 연구 서술로만 비교한다.

### 평가 지표

- 주행 거리와 계획 시간은 목표(경로 품질 유지 + 효율)를 평가하기에 적절하다. 성공률, 동적 장애물 대응 시간 같은 지표는 없다.

### 데이터 신뢰성

- 시뮬레이션의 최적 기준은 ground truth grid로 신뢰할 수 있다. 실제 실험은 반복 횟수가 명시되지 않았다.

### 주장과 결과의 관계

- "전역 metric map과 비슷한 성능"이라는 결론은 시뮬레이션에서는 잘 뒷받침된다. 실제 로봇 결과(약 19% 더 긴 경로)에 대해서는 과도한 일반화일 수 있다.
- 계획 시간이 "거리에 따라 격차가 커진다"는 해석은 표의 경향과 대체로 맞지만, 17개 경로로 얻은 추세이므로 더 큰 환경에서의 결론은 추정이다.

## 10. 편향 점검

| 편향 유형 | 수준 | 근거 |
|---|---|---|
| 연구비·이해충돌 | 중간 | 저자 전원이 Willow Garage 소속이며, PR2와 ROS 모두 같은 회사의 제품·플랫폼이다(분석자 판단) |
| 선택 편향 | 중간 | 시뮬레이션·실제 모두 사무 환경 하나 |
| 확증 편향 | 중간 | 실제 로봇 결과의 큰 경로 차이를 "comparable"로 평가 |
| 출판 편향 | 확인 불가 | 확인 가능한 정보 없음 |
| 지역적 편향 | 확인 불가 | 확인 가능한 정보 없음 |

## 11. 주요 전문 용어

### Pose Graph

로봇의 과거 pose를 노드로, pose 간 상대 변환 제약(odometry, scan matching, loop closure)을 edge로 표현한 그래프다. Graph SLAM은 이 그래프를 최적화해 일관된 궤적을 얻는다.

### Occupancy Grid

공간을 격자로 나누고 각 칸이 장애물로 점유되었는지를 표시한 metric map이다. 이 논문은 전역 grid 대신 크기가 제한된 국소 grid만 만든다.

### Navigation Graph

Pose graph 노드 위에 "실제로 이동 가능한 연결"만 edge로 둔 그래프다. edge는 국소 grid 안에서 A*로 확인한 경로이며 비용은 경로 길이다.

### Navigation Function

grid의 각 지점에 목표(또는 로봇)까지의 거리와 장애물 정보를 반영한 potential 값을 부여한 함수다. Dijkstra로 계산하며, potential이 낮은 방향으로 가면 목표에 도달한다.

### Dynamic Window Approach (DWA)

로봇이 현재 속도에서 짧은 시간 안에 낼 수 있는 속도 후보를 시뮬레이션해, 전역 경로를 따르면서 장애물을 피하는 명령을 고르는 국소 제어 기법이다.

### Configuration Space

로봇을 점으로 보고 장애물을 로봇 반경만큼 팽창시킨 공간이다. 이 공간에서 경로를 찾으면 로봇의 크기가 자동으로 반영된다.

## 12. 실무 기술 연결

### 논문에서 실제 사용한 기술

- Graph SLAM, Karto scan matcher, sparse pose adjustment
- 2D laser range finder, ray tracing 기반 occupancy grid
- A*, Dijkstra
- ROS navigation stack, Dynamic Window Approach
- Willow Garage PR2

### 실무 구현 시 적용 가능한 기술

아래는 서비스 구현 시 활용할 수 있는 예시이며, 논문에서 사용한 기술이 아니다.

**Robotics**
- ROS 2 Navigation2 (costmap, global/local planner)
- slam_toolbox (pose graph 기반 2D SLAM)

**Indoor 공간 모델**
- IndoorGML NRG, pgRouting (공간 단위 topology 경로 탐색)

**Spatial DB**
- PostgreSQL + PostGIS (국소 grid 영역과 graph 저장)

**Visualization**
- RViz, Cesium, Unity

## 13. 커리어 관점

### 공부해야 할 기술

- Graph SLAM과 pose graph optimization
- Occupancy grid, costmap, configuration space
- 그래프 탐색(Dijkstra, A*)과 계층적 경로 계획
- ROS navigation stack 구조(global planner, local planner)
- IndoorGML NRG와 로봇 navigation graph의 차이

### 실무 연결

- 공간 관점: 대형 공장, 물류센터, 공공시설처럼 넓은 실내 공간을 "구역 연결 그래프 + 구역별 정밀 지도"로 나눠 관리하는 설계
- 그 위에서 AMR·서비스 로봇의 navigation 스택 이해와 튜닝
- 실내 길찾기 서비스에서 공간 그래프와 정밀 지도의 이중 구조 설계

### 기술 면접으로 연결될 수 있는 질문

- Metric map과 topological map의 역할 차이는 무엇인가?
- 대규모 환경에서 단일 전역 occupancy grid만 쓰면 어떤 문제가 생기는가?
- Pose graph와 navigation graph는 왜 구조가 다른가?
- Topological 경로의 waypoint를 모두 따라가면 왜 경로가 길어지고, 이 논문은 이를 어떻게 피했는가?
- 로봇의 navigation graph 노드와 IndoorGML의 CellSpace 노드는 어떻게 다른가?

## 14. 후속 연구

### 저자가 제안한 Future Work

- 지도 갱신 시 그래프 거리가 멀어질수록 노드 간 상대 변위가 줄어든다는 점을 보여, 국소 갱신만으로 충분함을 입증
- 국소 metric map을 3D 구조로 유지. 각 grid의 영역이 제한되어 있으므로 온라인으로 만들고, 당장 필요하지 않을 때는 캐시로 보관할 수 있다고 본다.

### 추가 연구 아이디어

아래는 분석자의 제안이다.

- 스캔 위치 노드 대신 방·복도 같은 의미 있는 공간 단위를 노드로 쓰는 navigation graph(IndoorGML CellSpace와의 결합)
- 3DGS 기반 visual localization과 IndoorGML topology를 결합한 하이브리드 navigation
- 영구적인 공간 변화(가벽, 문 폐쇄)를 일시적 장애물과 구분해 topology를 갱신하는 연구

## 15. 논문 읽기 가이드

**1순위 — Figure 1, Figure 3**

Pose graph, navigation graph, 국소 grid가 어떻게 겹쳐 있는지 먼저 파악한다. 두 그래프 구조가 다른 이유가 핵심이다.

**2순위 — Section III-B, IV (Navigation Graph와 계획·실행)**

Edge 생성 방식과 "현재 grid의 마지막 waypoint만 넘긴다"는 실행 전략을 이해한다.

**3순위 — Section VI (Table I, II, III)**

시뮬레이션 최적성, 계획 시간, 실제 로봇 결과를 확인한다. 시뮬레이션과 실제 결과의 차이에 주의한다.

**4순위 — Section V와 Conclusion**

지도 갱신 전략의 한계와 3D 국소 지도로의 확장 방향을 확인한다.

## 16. 핵심 정리

- 정밀 이동은 국소 metric grid("정확히 어디를 지나갈까"), 전역 계획은 topological graph("어떤 공간들을 거쳐갈까")가 담당한다.
- 전역 occupancy grid를 만들지 않고, pose graph 위에 이동 가능성 기반 navigation graph와 국소 grid를 겹쳐 쓴다.
- 시뮬레이션에서는 전역 metric 계획 대비 경로 길이 1% 이내, 계획 시간은 크게 단축되었다. 실제 로봇에서는 경로가 약 19% 길었다.
- 이 논문의 topology 노드는 의미 있는 공간이 아니라 스캔 위치다. 의미 있는 공간 단위의 topology(IndoorGML)와 연결하는 것은 별도의 과제다.

## 관련 글

- [[2008-conceptual-spatial-representations|Conceptual Spatial Representations]] — metric·topological·conceptual 계층
- [[2019-point-cloud-to-indoorgml-navigation-graph|Point Cloud → IndoorGML Navigation Graph]] — 의미 있는 공간 단위의 navigation graph 자동 생성
- [[2022-hydra-3d-scene-graph|Hydra]] — places topological map의 실시간 자동 추출
- [[2026-indoorgml-constrained-3dgs-navigation|IndoorGML-Constrained 3DGS Navigation]] — IndoorGML topology로 3DGS 장면 간 이동 제어
