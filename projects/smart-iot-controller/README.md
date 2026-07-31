# Smart IoT Controller

> Raspberry Pi 센서 데이터 실시간 모니터링 및 제어 GUI

## 프로젝트 개요

Raspberry Pi에 연결한 LED, RGB LED, 부저, 조도센서,
초음파센서를 PyQt5 GUI에서 실시간 모니터링하고 수동·자동 제어하는 애플리케이션입니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| Language / UI | Python, PyQt5, Qt Designer |
| Hardware | Raspberry Pi, RGB LED, Buzzer, CDS, HC-SR04 |
| Library | gpiozero, smbus, pyqtgraph |
| 주기 | QTimer 500ms |

## 주요 기능

- 거리·조도 센서값 실시간 표시
- 최근 측정값 그래프 시각화
- RGB LED와 부저 수동 제어
- 거리 기준 DANGER·NOTICE·SAFE 상태 판정
- 자동 경고와 수동 제어 상태 분리

## 시스템 흐름

```text
CDS / HC-SR04
    ↓ GPIO / I2C
Python Sensor Logic
    ↓ QTimer
PyQt5 LCD / Progress / Graph
    ↓
RGB LED / Buzzer
```

## 대표 트러블슈팅

### 1. 수동·자동 제어 충돌

**문제**  
주기적 자동 제어가 사용자의 수동 명령을 즉시 덮어씀

**해결**  
수동 모드 상태 변수를 분리해 자동 제어 실행 조건을 제한

### 2. UI 멈춤

**문제**  
센서값을 반복문에서 계속 읽으면 이벤트 루프가 중단

**해결**  
QTimer를 사용해 500ms마다 비동기로 갱신

### 3. 그래프 데이터 증가

**문제**  
측정값을 무제한 저장하면 메모리와 그래프 성능 저하

**해결**  
최근 50개 값만 유지

## 프로젝트 결과

- 하드웨어 센서와 GUI를 실시간 연동
- 자동 제어와 사용자 제어의 우선순위 분리
- 주기적 데이터 갱신과 그래프 시각화 구현

## 폴더 안내

- `README.md`: 프로젝트 핵심 내용
- `docs/`: 설계·요구사항 등 상세 문서
- `images/`: 실행 화면이나 구성도 추가 위치

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드는 각 원본 GitHub 저장소에서 관리합니다.
