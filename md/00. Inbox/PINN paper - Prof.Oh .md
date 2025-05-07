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

    ### PINN
        - 편미분바정식, 상미분방정식을 풀기 위해 도입
        - 유체, 열, 구조 등 공학분야에 적용
        - 신경망이 제한적이며 불균형한 데이터에서도 의미 있는 값을 추출
        - 제약 조건을 둔다는 것은 최적화가 본질적으로 어려워지기 때문에 비선형적인 문제에서 수렴 및 정확도 문제가 발생

# Surrogate Model
- 대리 모델(Surrogate Model)은 복잡한 물리적 시스템을 근사하는 간소화된 수학적 모델
- 주요 특징:
    * 계산 효율성: 원본 모델보다 계산 비용이 낮음
    * 정확성: 핵심 물리적 특성을 보존
    * 일반화: 다양한 운전 조건에서 신뢰할 수 있는 예측 제공
- 배터리 분야에서의 응용:
    * 전기화학적 모델의 복잡성 감소
    * 실시간 모니터링 및 제어에 적합
    * 물리적 제약조건을 통합한 신뢰성 있는 예측
- PINN 기반 대리 모델의 장점:
    * 물리적 법칙을 명시적으로 통합
    * 제한된 데이터로도 효과적인 학습
    * 물리적으로 의미 있는 예측 보장

    ## DeepONet
    비선형 연산자를 근사하는력기능을 보여주는 대리 모델
    함수 간 매핑을 실행하여 확장성을 지님
    입력 및 출력 함수 간의 관계를 식별하여 다양한 작동 조건에서 보간 및 외삽이 가능
    다양한 작동 조건에서 광범위한 학습 데이터가 필요함.

    Distinct time derpendent feature(DTDF)
    초기 100cyclea만 수집 > DTDF = [DTDF1, ..., DTDF100]
    DTDF_N = [mean(x_c,v), var(x_c,v),mean(x_c,I), var(x_c,I),mean(x_d,v), var(x_d,v) ]
    DeepONet은 다음과 같은 과학적, 공학적 메커니즘을 통해 복잡한 열화 특성을 효과적으로 모델링한다:

    1. 함수 공간 매핑 (Function Space Mapping)
        - Universal Approximation Theorem에 기반한 연속 함수 공간의 근사
        - Branch Network와 Trunk Network의 이중 구조를 통한 함수 간 매핑 학습
        - 다양한 작동 조건에서의 패턴을 고차원 함수 공간에서 포착

    2. 비선형 연산자 근사 (Nonlinear Operator Approximation)
        - Koopman 연산자 이론을 활용한 동적 시스템의 비선형성 포착
        - 온도 의존적 열화 특성을 연속적인 함수 공간에서 표현
        - 고차원 비선형 관계의 효율적인 학습

    3. 물리적 제약 통합 (Physical Constraint Integration)
        - PINN 프레임워크와의 통합을 통한 물리 법칙 준수
        - 열역학적 제약조건을 손실 함수에 명시적 반영
        - 물리적으로 의미 있는 예측 결과 보장

    이러한 메커니즘을 통해 DeepONet은 학습 데이터 범위 내에서의 내삽(interpolation)과 범위를 벗어난 외삽(extrapolation) 모두에서 신뢰할 수 있는 예측 성능을 보인다. 이는 함수 간 매핑 전략을 통해 연속적인 함수 공간에서의 일반화 능력을 획득했기 때문이다.


# 모델
    35도, 45도 열화 데이터를 training dataset for surrogate neural network
    sliding window with 30 cycles
    The domain shift learning retrained the pre-trained surrogate neural network, while fine tuning was executed using the initial 200 cycles from each cell.
    1000 epochs using the Adam optimizer with a learning rate of 1e-3
    physics loss coefficient increased form 0.01 to 10 over 1000 epochs
    learning rate 1e-5: 가중치 업데이트를 smoothing

    DTDF의 상관성을 보기 위해 Pearson correlation coefficient (PCC), Maximum information coefficient (MIC)

    - PCC 논의
        방전 CC: useful for identifiying linear relationships
        충전 CCCV: nonlinear 특성
    - MIC 논의


    추세 반영이 가능한 초반 구간은 Data driven 우위
    Domain shift learning 과정에서 과적합으로 후반 수명 트렌드의 정확도 및 강건성이 떨어짐

    Epoch에에따라 물리적 손실 계수를 점진적으로 증가시키는 전략은 학습 과정 전반에 걸쳐 물리 지능의 기여도를 제어함으로써 이 문제를 해결

    - 둘 다 과적합
    물리 손실 계수 0.01~1은 초반 수명 기울기를 따라가고
    10은 empirical 식을 따라감


