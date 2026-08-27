# Smart Gate Monitoring System

> ROS2와 Arduino를 연동한 센서 기반 실시간 게이트 제어 및 모니터링 시스템

## 시스템 구조

<p align="center">
  <img src="https://github.com/user-attachments/assets/a600b298-508e-4993-a59c-84b71b680056" width="1000" alt="Smart Gate Monitoring System 시스템 구성 예시"/>
</p>

<p align="center">
  <sub>※ 실제 시스템 사진이 아닌, 시스템 구성과 동작 흐름을 설명하기 위한 예시 이미지입니다.</sub>
</p>

<br>

## 모니터링 화면

<p align="center">
  <img src="https://github.com/user-attachments/assets/4bdd9082-4695-4fa0-8edd-cdbfe8df7256" width="500" alt="Smart Gate Monitoring System PyQt5 모니터링 화면"/>
</p>

<p align="center">
  <sub>ROS2 센서 데이터와 시스템 상태, LED·게이트 제어 명령을 실시간으로 확인하는 PyQt5 모니터링 GUI</sub>
</p>

<br>

## 🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-cpp-2026-mini-project/tree/main#smartgate)

---

## 프로젝트 개요

Arduino에서 측정한 거리·온도·습도·조도 데이터를 Serial 통신으로  
Raspberry Pi에 전달하고, ROS2에서 센서별 Topic으로 변환해 상태를 판단하는 시스템입니다.

`controller_node`에서 복수 센서 데이터를 기반으로 위험 상태를 판단하고,  
결과를 `/led_cmd`, `/gate_cmd` Topic으로 발행하여  
Arduino의 RGB LED와 스테퍼 모터를 제어하도록 구성했습니다.

기존 콘솔 Dashboard의 모니터링 기능을 PyQt5 GUI로 확장하여  
센서값과 시스템 상태, 현재 LED·게이트 제어 명령을 한 화면에서 확인할 수 있도록 구현했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 개인 프로젝트 |
| 개발 환경 | Ubuntu, ROS2 Jazzy, Arduino UNO |
| Language | Python, Arduino C++ |
| GUI | PyQt5 |
| Sensor / Actuator | HC-SR04, DHT11, CDS, RGB LED, Stepper Motor |
| 통신 | Serial Communication, ROS2 Pub/Sub |

## 주요 기능

- Arduino에서 거리·온도·습도·조도 센서 데이터 수집
- 센서 데이터를 `distance,temp,humidity,light` 형식의 CSV로 Serial 전송
- `sensor_bridge`를 이용한 ROS2 센서 Topic 변환 및 발행
- `/distance`, `/temperature`, `/humidity`, `/light_level` Topic 기반 상태 모니터링
- `controller_node` 기반 복수 센서 위험 상태 판단
- `/led_cmd`, `/gate_cmd` Topic을 통한 제어 명령 발행
- RGB LED를 이용한 위험·주의·안전 상태 표시
- 스테퍼 모터를 이용한 게이트 OPEN / CLOSE 제어
- PyQt5 GUI를 통한 센서값·시스템 상태·제어 명령 실시간 모니터링

## 시스템 흐름

```text
Arduino Sensors
    ↓ Serial CSV
sensor_bridge.py
    ↓
/distance
/temperature
/humidity
/light_level
    ↓
controller_node.py
    ├────────→ PyQt5 Monitoring GUI
    │          ├─ System Status
    │          ├─ Sensor Data
    │          └─ Active Commands
    │
    ↓
/led_cmd
/gate_cmd
    ↓
sensor_bridge.py
    ↓ Serial Command
Arduino
    ├─ RGB LED
    └─ Stepper Motor
```

## 제어 로직

센서값을 기반으로 현재 시스템 상태를 판단하고,  
상태에 따라 LED와 게이트 제어 명령을 생성하도록 구성했습니다.

| 조건 | 시스템 상태 | LED | Gate |
|---|---|---|---|
| 기본 상태 | `NORMAL` | GREEN | CLOSE |
| 습도 > 80% | `HUMID WARNING` | YELLOW | CLOSE |
| 조도 < 300 | `NIGHT SECURITY` | GREEN | CLOSE |
| 야간 + 거리 < 50cm | `NIGHT SECURITY` | YELLOW | CLOSE |
| 거리 < 30cm | `NEAR APPROACH` | YELLOW | CLOSE |
| 거리 < 10cm | `INTRUSION DETECTED` | RED | OPEN |
| 온도 > 35°C | `FIRE EMERGENCY` | RED | OPEN |

> 여러 조건이 동시에 충족되는 경우 코드의 판단 순서에 따라 후순위 조건이 최종 상태와 제어 명령에 반영됩니다.

### LED 상태

| 상태 | 명령 | RED | GREEN | BLUE |
|---|---|---|---|---|
| 위험 | RED | ON | OFF | OFF |
| 주의 | YELLOW | ON | ON | OFF |
| 안전 | GREEN | OFF | ON | OFF |

> RGB LED는 ACTIVE LOW 방식으로 `LOW = ON`, `HIGH = OFF`로 동작하며,  
> YELLOW는 RED와 GREEN을 동시에 점등하여 구현했습니다.

### Gate 제어

| 명령 | 동작 |
|---|---|
| OPEN | 게이트 열기 (+512 step) |
| CLOSE | 게이트 닫기 (-512 step) |

## 주요 구성 요소

### Arduino

- HC-SR04 초음파 센서 거리 측정
- DHT11 온도·습도 측정
- CDS 조도 측정
- 센서 데이터 Serial 전송
- ROS2 제어 명령 수신
- RGB LED 및 스테퍼 모터 제어

### sensor_bridge

Arduino에서 전달받은 CSV 데이터를 파싱하여 ROS2 Topic으로 변환합니다.

```text
25.3,28.5,54.2,620
```

Publish Topic:

```text
/distance
/temperature
/humidity
/light_level
```

또한 `/led_cmd`, `/gate_cmd`를 Subscribe하여  
ROS2 제어 명령을 다시 Arduino로 전달합니다.

### controller_node

센서 Topic을 Subscribe하여 현재 시스템 상태를 판단하고  
LED 및 게이트 제어 명령을 생성합니다.

Publish Topic:

```text
/led_cmd
/gate_cmd
```

주요 판단 상태:

```text
NORMAL
HUMID WARNING
NIGHT SECURITY
NEAR APPROACH
INTRUSION DETECTED
FIRE EMERGENCY
```

### PyQt5 Monitoring GUI

기존 `controller_node`의 콘솔 Dashboard에서 확인하던 정보를  
PyQt5 GUI로 확장하여 실시간으로 확인할 수 있도록 구현했습니다.

GUI 표시 항목:

- System Status
- Distance
- Temperature
- Humidity
- Light Level
- LED Color
- Gate Status

기존 ROS2 센서 수집·상태 판단·하드웨어 제어 구조는 유지하고,  
모니터링 화면을 GUI 형태로 확장했습니다.

ROS2 Callback과 Qt Event Loop를 함께 처리하기 위해  
`QTimer`에서 `rclpy.spin_once()`를 주기적으로 호출하도록 구성했습니다.

```python
timer = QTimer()

timer.timeout.connect(
    lambda: rclpy.spin_once(
        node,
        timeout_sec=0.0
    )
)

timer.start(20)
```

## 대표 트러블슈팅

### 1. Serial Parsing 오류

**문제**  
`ARDUINO READY`와 같은 디버그 문자열이 센서 CSV 데이터와 함께 전송되어  
`sensor_bridge`에서 파싱 오류가 발생했습니다.

**해결**  
Arduino의 Serial 출력 형식을  
`distance,temp,humidity,light` 네 개의 센서값 CSV로 고정하여  
센서 데이터만 전달하도록 수정했습니다.

### 2. RGB LED 색상 불일치

**문제**  
RGB LED의 ACTIVE LOW 특성과 실제 핀 매핑을 반대로 이해하여  
원하는 색상이 정상적으로 출력되지 않았습니다.

**해결**  
RED(D13), GREEN(D11), BLUE(D12) 핀을 다시 확인하고  
`LOW = ON`, `HIGH = OFF` 기준으로 제어 로직을 수정했습니다.

YELLOW는 RED와 GREEN을 동시에 점등하도록 구현했습니다.

### 3. ROS2-Arduino 명령 불일치

**문제**  
ROS2에서 발행하는 명령 문자열과 Arduino에서 비교하는 문자열이 일치하지 않아  
LED와 게이트가 정상적으로 동작하지 않았습니다.

**해결**  
양쪽에서 사용하는 명령을  
`RED`, `YELLOW`, `GREEN`, `OPEN`, `CLOSE`로 통일하여  
Serial 제어 명령의 일관성을 확보했습니다.

## 프로젝트 결과

- ROS2와 Arduino 간 양방향 Serial 통신 구현
- 센서 데이터를 네 개의 ROS2 Topic으로 분리하여 발행
- 복수 센서 데이터를 기반으로 위험 상태 판단 로직 구현
- RGB LED를 이용한 상태 시각화
- 스테퍼 모터를 이용한 게이트 개폐 제어
- 센서 데이터와 제어 명령의 형식을 표준화하여 통신 안정성 개선
- 기존 콘솔 Dashboard를 PyQt5 기반 모니터링 GUI로 확장
- 센서값·시스템 상태·LED 및 게이트 제어 명령 실시간 시각화
- Arduino 센서 수집 → ROS2 상태 판단 → 하드웨어 제어로 이어지는 시스템 흐름과 PyQt5 기반 실시간 모니터링 구현

## 폴더 안내

- `README.md`: 프로젝트 핵심 내용
- `docs/`: 설계·요구사항 등 상세 문서
- `images/`: 실행 화면 및 시스템 구성 이미지

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드와 상세 구현 과정은 원본 GitHub 저장소에서 관리합니다.
