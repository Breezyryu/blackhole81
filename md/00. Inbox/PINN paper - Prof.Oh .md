# PINN

## Abstract
- Neural network > time depenent features > nonlinear degradation 특성
- Surrogate neural network
    - distinct time dependent features
    - physic > supervised 역할
    - domain shift learning strategy > NN interpolation, extrapolation

## Introduction
    배터리 수명 예측과 SOH(State of Health) 추정을 위한 머신러닝 연구는 크게 세 가지 접근 방식으로 발전해왔다:

    1. 전통적 머신러닝 기법
        - 가우시안 프로세스 회귀(GPR)와 지원 벡터 머신(SVM)이 제한된 데이터로 SOH 추정에 널리 활용됨
        - GPR은 확률적 접근으로 예측의 불확실성을 정량화하고 신뢰 구간을 제공
        - SVM은 고차원 공간에서 최적의 결정 경계를 찾아 복잡한 비선형 관계를 모델링
        - 제한된 데이터셋에서도 효과적인 성능을 보이지만, 물리적 메커니즘의 이해에는 한계가 있음

    2. 딥러닝 기반 접근법
        - RNN 계열(LSTM, GRU)이 배터리 열화 모델링의 주류를 이루며, 시계열 패턴 포착에 효과적
        - CNN과 RNN의 결합으로 공간적-시간적 특징을 동시에 학습
            * CNN: 배터리 데이터의 지역적 패턴과 구조적 특징 추출
            * RNN: 시계열 데이터의 순차적 패턴과 장기 의존성 모델링
        - 순수 데이터 기반 접근의 한계:
            * 물리적 메커니즘 설명의 어려움
            * 다양한 운전 조건에서의 일반화 성능 부족
            * 복잡한 물리적 특성의 완전한 포착의 어려움

    3. 어텐션 기반 신경망
        - Seq2Seq 아키텍처와 Temporal Fusion Transformer(TFT)가 주목받음
        - 주요 특징:
            * 멀티헤드 어텐션을 통한 시계열 의존성 학습
            * 정적/동적 특성의 통합적 처리
            * 병렬 처리 가능한 구조로 학습 효율성 향상
            * 어텐션 가중치를 통한 모델 해석성 제공
        - 장기 시계열 의존성 포착과 다양한 시간 스케일의 패턴 학습에 효과적

    - 효율적인 학습을 위해서는 effective feature extraction 이 필요
        대표적 지표
            - 전압, 전류 곡선의 기울기
            - 증분 용량 (Incremental capacity)
        - 소량의 열화 데이터로 데이터 가용성이 떨어짐


    