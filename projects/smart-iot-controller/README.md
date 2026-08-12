# Smart IoT Controller

> Raspberry Pi 센서 데이터 실시간 모니터링 및 제어 GUI

## 시스템 구성 예시

<p align="center">
  <img src="https://github.com/user-attachments/assets/6025b2d9-e502-4902-a7d5-8e8bb7f154ac" width="1000" alt="Smart IoT Controller 시스템 구성 예시"/>
</p>

> Raspberry Pi와 조도·거리 센서, RGB LED, 부저를 연동한 시스템 구성을 이해하기 위한 예시 이미지입니다.

<br>

## GUI 실행 화면

<p align="center">
  <img src="https://github.com/user-attachments/assets/2ae74064-fc8a-4650-aa95-9c2aafba6b3d" width="400" alt="Smart IoT Controller GUI 실행 화면"/>
</p>

<br>

## 🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-cpp-2026-mini-project/tree/main#d0507)

---

## 프로젝트 개요

Raspberry Pi에 연결된 조도센서와 초음파센서의 데이터를
PyQt5 GUI에서 실시간으로 모니터링하고,
RGB LED와 부저를 수동·자동으로 제어하는 임베디드 IoT 컨트롤러입니다.

Qt Designer로 GUI를 설계하고 Python(PyQt5)과 GPIO를 연동했으며,
`QTimer`를 이용해 센서 데이터를 500ms 주기로 갱신하도록 구현했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 개인 실습 프로젝트 |
| Language / UI | Python, PyQt5, Qt Designer |
| Hardware | Raspberry Pi 4, RGB LED, Buzzer, CDS, HC-SR04 |
| Library | gpiozero, smbus, pyqtgraph |
| 데이터 갱신 | QTimer 500ms |
| 통신 / 제어 | GPIO, I2C |

## 주요 기능

- CDS 조도센서 데이터 실시간 표시
- HC-SR04 초음파센서 거리 실시간 측정
- LCD 및 ProgressBar를 이용한 센서값 시각화
- 최근 거리·조도 측정값 그래프 표시
- RGB LED 및 부저 수동 ON/OFF 제어
- 거리값에 따른 `DANGER`, `NOTICE`, `SAFE` 상태 판정
- 위험 상태에 따른 RGB LED 자동 제어
- 10cm 미만 접근 시 부저 자동 경고
- 수동 제어 상태와 자동 제어 로직 분리

## 시스템 흐름

```text
CDS / HC-SR04
      ↓
GPIO / I2C
      ↓
Python Sensor Logic
      ↓
QTimer (500ms)
      ↓
PyQt5 GUI
 ├─ LCD
 ├─ ProgressBar
 ├─ Status
 └─ Real-time Graph
      ↓
Control Logic
      ↓
RGB LED / Buzzer
```

## 제어 로직

| 거리 | 상태 | RGB LED | Buzzer |
|---|---|---|---|
| 10cm 미만 | DANGER | RED | ON |
| 10cm 이상 ~ 40cm 미만 | NOTICE | YELLOW | OFF |
| 40cm 이상 | SAFE | OFF | OFF |

수동 제어가 활성화된 경우에는 자동 제어가 해당 장치를
즉시 덮어쓰지 않도록 `manual_led`, `manual_buzz` 상태 변수를 분리했습니다.

## 대표 트러블슈팅

### 1. Qt UI 파싱 및 SyntaxError

**문제**

`uic.loadUiType()` 호출 시 UI 파일이 정상적으로 로딩되지 않고
`SyntaxError`가 발생했습니다.

**원인**

Qt Designer와 PyQt5 간 Qt Enum 값 해석 방식의 차이로
UI XML 내부의 C++ 스타일 네임스페이스(`::`)가
Python 변환 과정에서 그대로 남아 오류가 발생했습니다.

**해결**

- Qt Designer에서 UI 속성을 다시 설정해 XML 구조 정리
- 빌드 캐시 초기화
- `.autosave` 및 중복 UI 파일 제거
- 단일 UI 소스 구조로 정리

**결과**

UI 로딩을 정상화하고 Raspberry Pi 환경에서
GPIO 제어 기능과 안정적으로 연동되는 것을 확인했습니다.

### 2. 수동·자동 제어 분리

**문제**

센서값에 따른 자동 제어와 사용자의 버튼 제어가
동일한 RGB LED와 부저를 제어해야 했습니다.

**해결**

`manual_led`, `manual_buzz` 상태 변수를 두고
수동 제어 중에는 해당 장치의 자동 제어가 실행되지 않도록 구성했습니다.

### 3. 실시간 센서 데이터 갱신

**문제**

센서 데이터를 지속적으로 읽으면서도
GUI 입력과 화면 갱신이 정상적으로 처리되어야 했습니다.

**해결**

`QTimer`를 이용해 500ms마다 `update_sensor()`를 호출하여
센서 읽기와 화면 갱신을 주기적으로 처리했습니다.

그래프 데이터는 최근 50개의 측정값만 유지하도록 구성했습니다.

## 프로젝트 결과

- Qt Designer와 PyQt5를 이용한 Raspberry Pi 제어 GUI 구현
- GPIO/I2C 기반 센서 데이터와 GUI 실시간 연동
- 거리값에 따른 상태 판정 및 RGB LED·부저 자동 제어
- 사용자 수동 제어와 센서 기반 자동 제어 로직 분리
- QTimer 기반 주기적 센서 데이터 갱신
- pyqtgraph를 이용한 거리·조도 데이터 실시간 시각화
- Qt UI 파싱 오류의 원인을 분석하고 UI 구조를 정리하여 실행 안정화

## 폴더 안내

- `README.md`: 프로젝트 핵심 내용
- `docs/`: 설계·요구사항 등 상세 문서
- `images/`: 실행 화면이나 구성도 추가 위치

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드는 원본 GitHub 저장소에서 관리합니다.
