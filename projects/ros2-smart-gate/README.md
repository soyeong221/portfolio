# Smart Gate Monitoring System

> ROS2와 Arduino를 연동한 센서 기반 실시간 게이트 제어 및 모니터링 시스템

## 시스템 구조

<p align="center">
  <img src="https://github.com/user-attachments/assets/3f4a3dee-494f-46cf-8ff2-f0a4adbd16cc" width="1000" alt="Smart Gate Monitoring System 시스템 구성도"/>
</p>

<p align="center">
  <sub>※ 실제 시스템 사진이 아닌, 시스템 구성과 동작 흐름을 설명하기 위한 구성도입니다.</sub>
</p>

<br>

## 모니터링 화면

<p align="center">
  <img src="https://github.com/user-attachments/assets/0515eaf4-ab6e-405a-9cf0-7cb0fb399124" width="500" alt="Smart Gate Monitoring System 콘솔 Dashboard 실행 화면"/>
</p>

<p align="center">
  <sub>ROS2 센서 데이터와 시스템 상태, LED·게이트 제어 명령을 실시간으로 확인하는 콘솔 Dashboard</sub>
</p>

<br>

## 🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-cpp-2026-mini-project/tree/main#smartgate)

---

## 프로젝트 개요

Arduino에서 측정한 거리·온도·습도·조도 데이터를 Serial 통신으로 ROS2 환경에 전달하고,
센서별 Topic으로 변환하여 현재 시스템 상태를 판단하는 개인 프로젝트입니다.

`controller_node`에서 복수 센서 데이터를 기반으로 위험 상태를 판단하고,
결과를 `/led_cmd`, `/gate_cmd` Topic으로 발행하여
Arduino의 RGB LED와 스테퍼 모터를 제어하도록 구성했습니다.

센서값과 시스템 상태, 현재 제어 명령은 콘솔 Dashboard를 통해 실시간으로 확인할 수 있습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 개인 프로젝트 |
| 개발 환경 | Ubuntu, ROS2 Jazzy, Arduino UNO |
| Language | Python, Arduino C++ |
| Sensor / Actuator | HC-SR04, DHT11, CDS, RGB LED, Stepper Motor |
| 통신 | Serial Communication, ROS2 Pub/Sub |

## 주요 기능

- 거리·온도·습도·조도 센서 데이터 수집 및 Serial CSV 전송
- `sensor_bridge`를 통한 센서별 ROS2 Topic 변환 및 발행
- 복수 센서 데이터를 기반으로 한 위험 상태 판단
- `/led_cmd`, `/gate_cmd` Topic 기반 RGB LED·게이트 제어
- 콘솔 Dashboard를 통한 센서값·시스템 상태·제어 명령 실시간 모니터링

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
    ├─ 상태 판단
    ├─ Console Dashboard
    └─ /led_cmd, /gate_cmd
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

## 핵심 구현 코드

### 1. Serial 센서 데이터를 ROS2 Topic으로 변환

Arduino에서 CSV 형식으로 전달된 거리·온도·습도·조도 데이터를 파싱하고,
각 데이터를 독립적인 ROS2 Topic으로 발행했습니다.

```python
def read_serial(self):
    if self.ser.in_waiting > 0:
        line = self.ser.readline().decode(errors='ignore').strip()

        try:
            d, t, h, l = map(float, line.split(','))

            self.pub_dist.publish(Float32(data=d))
            self.pub_temp.publish(Float32(data=t))
            self.pub_humi.publish(Float32(data=h))
            self.pub_light.publish(Float32(data=l))

        except:
            pass
```

**구현 포인트**
- Serial CSV 데이터를 거리·온도·습도·조도로 분리
- 센서별 독립적인 ROS2 Topic으로 Publish
- Arduino와 ROS2 사이의 데이터 Bridge 구성

[전체 프로젝트 소스](https://github.com/soyeong221/iot-cpp-2026-mini-project/tree/main)

### 2. 복수 센서 기반 상태 판단 및 제어

센서 Topic으로 수신한 값을 조합하여 현재 상태를 판단하고,
LED와 게이트 제어 명령을 결정했습니다.

```python
led, gate, status = "GREEN", "CLOSE", "NORMAL"

if self.humi > 80:
    status, led = "HUMID WARNING", "YELLOW"

if self.light < 300:
    status = "NIGHT SECURITY"
    if self.dist < 50:
        led = "YELLOW"

if 0 < self.dist < 30:
    status, led, gate = "NEAR APPROACH", "YELLOW", "CLOSE"

if 0 < self.dist < 10:
    status, led, gate = "INTRUSION DETECTED", "RED", "OPEN"

if self.temp > 35:
    status, led, gate = "FIRE EMERGENCY", "RED", "OPEN"
```

상태가 변경된 경우에만 새로운 제어 명령을 Publish합니다.

```python
if led != self.last_led:
    self.led_pub.publish(String(data=led))
    self.last_led = led

if gate != self.last_gate:
    self.gate_pub.publish(String(data=gate))
    self.last_gate = gate
```

**구현 포인트**
- 거리·온도·습도·조도를 조합한 상태 판단
- 상태에 따른 LED·게이트 명령 생성
- 이전 명령과 비교하여 변경된 경우에만 Publish

[전체 프로젝트 소스](https://github.com/soyeong221/iot-cpp-2026-mini-project/tree/main)

### 3. ROS2 명령을 실제 하드웨어 제어로 연결

ROS2에서 생성된 제어 명령을 Serial로 Arduino에 전달하여
RGB LED와 스테퍼 모터를 제어했습니다.

```cpp
if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "RED")    setLED(LOW, HIGH, HIGH);
    if (cmd == "YELLOW") setLED(LOW, LOW, HIGH);
    if (cmd == "GREEN")  setLED(HIGH, LOW, HIGH);

    if (cmd == "OPEN")   myStepper.step(512);
    if (cmd == "CLOSE")  myStepper.step(-512);
}
```

**구현 포인트**
- ROS2 제어 명령을 Arduino에서 Serial로 수신
- ACTIVE LOW 방식의 RGB LED 제어
- `OPEN/CLOSE` 명령에 따른 스테퍼 모터 방향 제어
- ROS2의 판단 결과를 실제 하드웨어 동작까지 연결

[전체 프로젝트 소스](https://github.com/soyeong221/iot-cpp-2026-mini-project/tree/main)

## 대표 트러블슈팅

### 1. Serial Parsing 오류

**문제**  
`ARDUINO READY`와 같은 디버그 문자열이 센서 CSV 데이터와 함께 전송되어
`sensor_bridge`에서 파싱 오류가 발생했습니다.

**해결**  
Serial 출력 형식을 `distance,temp,humidity,light` 네 개의 센서값으로 고정하여
센서 데이터만 전달하도록 수정했습니다.

### 2. RGB LED 색상 불일치

**문제**  
RGB LED의 ACTIVE LOW 특성과 실제 핀 매핑을 반대로 이해하여
원하는 색상이 정상적으로 출력되지 않았습니다.

**해결**  
실제 핀 매핑을 다시 확인하고 `LOW = ON`, `HIGH = OFF` 기준으로 제어 로직을 수정했으며,
YELLOW는 RED와 GREEN을 동시에 점등하도록 구성했습니다.

### 3. ROS2-Arduino 명령 불일치

**문제**  
ROS2에서 발행하는 명령과 Arduino에서 비교하는 문자열이 일치하지 않아
LED와 게이트가 정상적으로 동작하지 않았습니다.

**해결**  
양쪽의 명령을 `RED`, `YELLOW`, `GREEN`, `OPEN`, `CLOSE`로 통일하여
Serial 제어 명령의 일관성을 확보했습니다.

## 프로젝트 결과

- ROS2와 Arduino 간 양방향 Serial 통신 구현
- 센서 데이터를 ROS2 Topic으로 분리하여 실시간 처리
- 복수 센서 기반 상태 판단 및 RGB LED·게이트 제어 구현
- 센서 데이터와 제어 명령 형식을 표준화하여 통신 안정성 개선
- 콘솔 Dashboard를 통한 센서값·시스템 상태·제어 명령 모니터링
- **센서 수집 → ROS2 상태 판단 → 하드웨어 제어**로 이어지는 전체 시스템 흐름 구현

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드와 상세 개발 과정은 원본 GitHub 저장소에서 관리합니다.