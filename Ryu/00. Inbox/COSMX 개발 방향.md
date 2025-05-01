---
tags:
- 배터리기술
- 리튬이온배터리
- 재료분석
- 전기화학
- 에너지저장장치
- BatteryTechnology
- LithiumIonBattery
- MaterialAnalysis
- Electrochemistry
- EnergyStorageDevice
aliases:
- BET Analysis
- COSMX Development
CMDS: "[[📚 104 Terminologies]]"
index: "[[🏷 Research Notes]]"
author: "[[류성택택]]"
---
## BET 분석 (Brunauer-Emmett-Teller Analysis)
#### What is BET Analysis
- 정의 (Definition):
	- BET (Brunauer-Emmett-Teller) 가스 흡착법은 물질의 비표면적, 기공 크기, 기공 부피 등을 측정하는 데 사용되는 분석 기술이다. 이 방법은 기체 분자를 고체 표면에 흡착시켜 표면적과 기공 구조를 파악한다.
	- BET 이론은 다층 흡착을 가정하며, 단분자층 흡착 용량을 기준으로 표면적을 계산하는 방법을 제공한다.
- 예시 (Examples):
	- 배터리 전극 소재의 표면적 및 기공 구조 분석에 활용
	- 촉매 및 나노 소재의 특성 평가에 사용
	- 리튬이온배터리 음극 소재인 실리콘-탄소 복합체의 구조 분석에 적용

## BET 분석의 기본 원리
- 가스 흡착: BET 분석은 일반적으로 질소(N₂) 가스를 흡착질로 사용하며, 일정 온도(액체 질소 온도, -196°C)에서 시료 표면에 질소 가스를 흡착시킨다.
- 흡착량 측정: 압력을 점진적으로 증가시키면서 시료 표면에 흡착되는 가스의 양을 측정한다. 이때 압력 변화를 가스 센서로 측정하고, 측정된 압력 값을 통해 흡착된 기체의 부피를 계산한다.
- BET 이론 적용: 측정된 흡착 데이터를 BET 이론에 적용하여 비표면적을 계산한다.

## BET 분석 시 고려 사항
1. 기공 크기: BET 분석은 주로 2 nm ~ 300 nm 범위의 기공 크기를 측정하는 데 적합하다.
2. 시료 형태: BET 분석은 분말, 필름, 스펀지 등 다양한 형태의 시료에 적용 가능하다.
3. 측정 가스: 일반적으로 질소 가스를 사용하지만, 시료의 특성에 따라 아르곤(Ar), 이산화탄소(CO₂) 등의 다른 가스를 사용할 수도 있다.
4. 표면적: BET 분석은 0.01 ㎡/g ~ 3,000 ㎡/g 범위의 비표면적을 측정할 수 있다.
5. 주의사항: 폐쇄된 기공(closed pore)의 경우 BET 방식으로 분석하는 데 한계가 있다.

## Literature Review
#### 리튬이온배터리 소재 분석
- 주요 내용 (Key points):
	- Carbon Frame: structure and pore - 탄소 프레임의 구조와 기공 특성이 배터리 성능에 영향
	- CVD process: uniform Si deposition - 화학기상증착법을 통한 균일한 실리콘 증착 가능
	- Bulk CNT enhancement - 벌크 탄소나노튜브를 통한 성능 향상
	- Si을 Carbon shell이 감싸고 이를 CNT가 받쳐주는 형상의 복합 음극 구조

#### 전극 소재 바인더 시스템
- 주요 내용 (Key points):
	- SBR: High elastic modulus rubber, excellent adhesion properties, effective expansion buffering
	- PAA-Li: High mechanical strength, highly salified structure, superior lithium-ion conductivity
	- CMC-Li: Uniform lithium salt dispersion, high ionic conduction pathways
	- SWCNT: Highly dispersed conductive additive, enhanced lithium-ion transport
	- Hydrogen Bonding Network: Dissipates mechanical stress/strain energy

## Pure SiC 시스템의 Fast fading 분석
- Material deterioration: Perform physical & chemistry tests to confirm, degrade mainly on anode
- Active lithium loss: check resistance to confirm, thick SEI and by-product indicate side reaction on SiC
- Abnormal interface: Check morphology by SEM and CT scan, abnormal area happened randomly on top/bottom
- Local high temperature: Check CC/DC temperature distribution, temperature distribute evenly over cell surface

## 전해질 시스템 분석 (Electrolyte System Analysis)
### Fluorinated solvent improving stability at high voltage
- Fluorinated solvent has lower HOMO level, which increases the oxidation resistance of electrolyte and improves the high voltage stability of battery.
- Stable SEI film which can improve cycling performance.
- SEI Stable phase: additive with cyclic structure > form polymer-rich SEI during early stage of cycle, resulting in elastic SEI
- SEI Thickening Region: develop additive with strong reducibility (F-containing additive) > repair broken SEI rapidly, prevent the substantial consumption of electrolyte
- SEI Failure Region: Lone paired electron (N, P or B containing additive) > eliminate HF, complex transition metal ions
  - HF는 리튬이온배터리에서 LiPF6 전해질이 수분과 반응하여 생성되는 부산물로, 전극 표면을 부식시키고 SEI 층을 손상시키는 유해 물질임
- Solid Electrolytes Additive는 고온에서 액체 전해질보다 이온전도도가 낮지만 저온에서도 일정한 이온전도도를 보이는 특징을 지님

## 전극 구조 개선 (Electrode Structure Improvement)
### Composite copper foil
- Copper + Polymer + copper 구조
- 6% 정도의 weight energy density 이득
- 추가적인 roller welding process
- 6% 높은 내부 저항 (0.345 mohm)
- Gravimetric ED 6% up / Volumetric ED 0.26% down

### Pre-lithiation 전략
- Li5FeO4: improve cathode P.D. / Reduce gas generation during storage
- Li5FeO4/Li2NiO2: Enhance the moisture resistance
- Li2NiO2/Li6CoO4: Improve specific capacity
- Li6CoO4/Others: Improve specific capacity

### LCO additive
- LCO(97.7%)+Additive(0.5%) > 고온저장 스웰링 개선 / 사이클 상온, 고온 개선 
- 설계 design: Specific capacity(mAh/g), Coating weight(mg/cm2), Density(g/cc)

### 분리막 구조
- 고온에서 분리막 PE pore 차단으로 thermal runaway 발생 가능성

### PFAS Free cathode binder
- PAA, PAN, PI/PAI, NBR
- PVDF system은 F의 Van der Waals forces 발생

### 비정형 L cell 구조

## 생산 공정 관리 (Manufacturing Process Control)
### 공정 issue 비중 (76% 정도)
- overbaked
- CTQ (Critical To Quality): 리튬이온배터리 생산공정에서 제품 품질에 결정적인 영향을 미치는 핵심 품질 특성 또는 파라미터. 제조 과정에서 반드시 관리되어야 하는 중요 품질 지표로, 배터리의 성능, 안전성, 수명에 직접적인 영향을 미치는 요소들을 의미함
- 5S management: Sort(정리), Set in order(정돈), Shine(청소), Standardize(표준화), Sustain(유지)의 5가지 원칙을 의미함. 배터리 제조 환경에서 품질 향상과 생산성 증대를 위한 기본적인 관리 방법론
- CTQ(Critical To Quality) customized: 제품별 특성에 맞는 품질 관리 기준을 수립함으로써 불량률 감소와 생산성 향상 가능
- MSOP(Manufacturing Standard Operating Procedure): 제조 표준 작업 절차로, 배터리 생산 과정의 표준화된 작업 지침. 이를 customized하여 공정 최적화, 작업자 오류 감소, 일관된 품질 확보 가능

## Si-anode 시스템 분석 (Silicon Anode System Analysis)
### SOC Estimation Error
- Loss of Si
- OCV shift

### Battery Swelling 분석

### Aging 메커니즘
Si-graphite 복합 음극의 열화 모드:
1. 리튬 도금(Lithium plating)
   - 빠른 충전 또는 저온 조건에서 Si-graphite 표면에 금속 리튬이 석출되는 현상
   - Butler-Volmer 방정식에 따라 전류 밀도와 과전압 관계로 설명 가능
   - 리튬 도금은 용량 손실, 내부 단락, 안전성 저하의 주요 원인

2. 활성화 에너지 장벽
   - 그라파이트 결정면별 리튬 삽입 활성화 에너지:
     • (003) 면: 0.44-0.48eV (상대적으로 낮은 에너지 장벽)
     • (104) 면: 0.54-0.56eV (상대적으로 높은 에너지 장벽)
   - 에너지 장벽 차이로 인한 불균일한 리튬 삽입/탈리 현상 발생

3. 기타 열화 메커니즘
   - 실리콘 입자의 부피 팽창/수축에 따른 기계적 스트레스
   - SEI(Solid Electrolyte Interphase) 층의 반복적 파괴 및 재형성
   - 활물질 분리 및 전기적 접촉 손실

## 관련 개념 (Related Concepts)
- [[리튬이온배터리 (Lithium-Ion Battery)]] #LithiumIonBattery
	- 리튬이온배터리는 리튬 이온이 음극과 양극 사이를 이동하며 전기를 저장하고 방출하는 충전식 배터리로, 높은 에너지 밀도와 긴 수명을 특징으로 함
- [[실리콘 음극재 (Silicon Anode Material)]] #SiliconAnode
	- 실리콘은 리튬이온배터리의 음극재로서 높은 이론 용량을 가지지만, 충방전 과정에서 큰 부피 변화를 겪는 한계가 있음
- [[고체 전해질 계면 (Solid Electrolyte Interphase)]] #SEI
	- SEI는 배터리 전극과 전해질 사이에 형성되는 보호막으로, 배터리의 성능과 수명에 중요한 영향을 미침