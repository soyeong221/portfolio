# SmartHome IoT Monitoring System

> MQTT와 Raspberry Pi를 활용한 실내 환경 모니터링 및 원격 제어

## 프로젝트 개요

실내 환경과 기기 상태를 실시간으로 모니터링하고,
조명·온습도·출입 상태 등 다양한 홈 환경을 원격 제어하는 IoT 시스템입니다.
Raspberry Pi에서 센서 데이터를 수집하고 MQTT로 전달하며,
PyQt5 화면과 MySQL 데이터베이스를 통해 상태 확인과 이력 관리를 수행합니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 핵심 기술 | Python, Raspberry Pi, MQTT, PyQt5, MySQL |
| 통신 | Eclipse Mosquitto |
| 데이터 | 센서 수집, MQTT 메시지, DB 저장 |
| UI | 실시간 상태 확인 및 원격 제어 |

## 주요 기능

- 온습도·조도·출입 등 센서 데이터 수집
- MQTT Publish / Subscribe 통신
- PyQt5 기반 실시간 모니터링 UI
- 조명과 장치 원격 제어
- 화재·이상 상태 경보
- MySQL 기반 센서 이력 저장

## 시스템 흐름

```text
Sensors / Devices
    ↓
Raspberry Pi
    ↓ MQTT Publish
Mosquitto Broker
    ├─ PyQt5 Monitoring UI
    ├─ Remote Control Command
    └─ MySQL Data Storage
```

## 대표 트러블슈팅

### 1. Broker 접근 설정

**문제**  
기본 설정에서는 외부 장치 접속이 제한됨

**해결**  
listener와 인증 설정을 구성하고 서비스 재시작

### 2. Topic 구조

**문제**  
기기별 메시지가 섞여 구독 범위가 불명확

**해결**  
공간·기기 기준 Topic 규칙을 정하고 `#` wildcard로 전체 모니터링

### 3. UI 실시간 갱신

**문제**  
센서 수신 처리로 화면이 멈출 수 있음

**해결**  
주기적 갱신과 통신 처리를 분리해 UI 응답성 유지

## 프로젝트 결과

- 센서 데이터 수집부터 화면 표시까지 전체 흐름 구현
- MQTT 기반 장치 간 비동기 통신 구조 이해
- 실시간 모니터링과 DB 이력 관리 연계

## 폴더 안내

- `README.md`: 프로젝트 핵심 내용
- `docs/`: 설계·요구사항 등 상세 문서
- `images/`: 실행 화면이나 구성도 추가 위치

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드는 각 원본 GitHub 저장소에서 관리합니다.
