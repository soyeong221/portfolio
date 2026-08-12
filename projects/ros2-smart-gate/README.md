# Smart Gate Monitoring System

> ROS2와 Arduino를 연동한 센서 기반 실시간 게이트 제어 시스템

## 실행 화면

<p align="center">
  <img src="https://github.com/user-attachments/assets/b3e87c35-14cd-48c5-840b-fd66d33ca493" width="600" alt="Smart Gate Monitoring System 실행 화면"/>
</p>

<br>

## 시스템 구조

<p align="center">
  <img src="https://github.com/user-attachments/assets/9cce5030-4bbd-4cab-8995-ab3aed89795d" width="1000" alt="Smart Gate Monitoring System 시스템 구성 예시 및 동작 흐름"/>
</p>

<p align="center">
  <sub>※ 시스템 구성을 이해하기 위한 예시 이미지입니다.</sub>
</p>

<br>

## 🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-cpp-2026-mini-project/tree/main#smartgate)

---

## 프로젝트 개요

Arduino에서 측정한 거리·온도·습도·조도 데이터를 Serial 통신으로
Raspberry Pi에 전달하고, ROS2에서 센서별 Topic으로 변환해 상태를 판단하는 시스템입니다.

`controller_node`에서 센서 데이터를 기반으로 위험 상태를 판단하고,
결과를 `/led_cmd`, `/gate_cmd` Topic으로 발행하여
Arduino의 RGB LED와 스테퍼 모터를 제어하도록 구성했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 개인 프로젝트 |
| 개발 환경 | Ubuntu, ROS2 Jazzy, Arduino UNO |
| Language | Python, Arduino C++ |
| Sensor / Actuator | HC-SR04, DHT11, CDS, RGB LED, Stepper Motor |
| 통신 | Serial Communication, ROS2 Pub/Sub |

## 주요 기능

- Arduino에서 거리·온도·습도·조도 센서 데이터 수집
- 센서 데이터를 `distance,temp,humidity,light` 형식의 CSV로 Serial 전송
- `sensor_bridge`를 이용한 ROS2 센서 Topic 변환 및 발행
- `/distance`, `/temperature`, `/humidity`, `/light_level` Topic 기반 상태 모니터링
- `controller_node` 기반 복수 센서 위험 상태 판단
- `/led_cmd`, `/gate_cmd` Topic 발행
- RGB LED를 이용한 위험·주의·안전 상태 표시
- 스테퍼 모터를 이용한 게이트 OPEN / CLOSE 제어
- 콘솔 Dashboard를 통한 센서값·시스템 상태·제어 명령 실시간 확인

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
    ↓
/led_cmd
/gate_cmd
    ↓
sensor_bridge.py
    ↓ Serial Command
Arduino
    ├─ RGB LED
    └─ Stepper Motor
