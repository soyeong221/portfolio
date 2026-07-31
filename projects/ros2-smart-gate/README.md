# Smart Gate Monitoring System

> ROS2와 Arduino를 연동한 센서 기반 실시간 게이트 제어 시스템

## 프로젝트 개요

Arduino에서 측정한 거리·온도·습도·조도 데이터를 Serial 통신으로
Raspberry Pi에 전달하고, ROS2에서 센서별 Topic으로 변환해 상태를 판단하는 시스템입니다.
판단 결과는 LED와 게이트 제어 명령으로 다시 Arduino에 전달됩니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 개인 프로젝트 |
| 개발 환경 | Ubuntu, ROS2 Jazzy, Arduino UNO |
| Language | Python, Arduino C++ |
| Sensor / Actuator | HC-SR04, DHT11, CDS, RGB LED, Stepper Motor |

## 주요 기능

- Arduino 센서 데이터 CSV 전송
- ROS2 sensor_bridge 기반 센서 Topic 분리 발행
- controller_node 기반 위험 상태 판단
- RGB LED 상태 표시
- 스테퍼 모터 기반 게이트 개폐
- 콘솔 Dashboard 실시간 모니터링

## 시스템 흐름

```text
Arduino Sensors
    ↓ Serial CSV
sensor_bridge.py
    ↓ /distance /temperature /humidity /light_level
controller_node.py
    ↓ /led_cmd /gate_cmd
sensor_bridge.py
    ↓ Serial Command
Arduino LED / Stepper Motor
```

## 대표 트러블슈팅

### 1. Serial Parsing 오류

**문제**  
`ARDUINO READY` 같은 디버그 문자열이 CSV 데이터와 섞여 파싱 실패

**해결**  
Arduino 출력 형식을 네 개의 센서값 CSV로 고정

### 2. RGB LED 색상 불일치

**문제**  
Active Low 방식과 실제 핀 매핑을 반대로 이해

**해결**  
`LOW=ON`, `HIGH=OFF` 기준으로 수정하고 YELLOW는 RED+GREEN으로 구현

### 3. 명령 불일치

**문제**  
ROS2와 Arduino에서 서로 다른 명령 문자열 사용

**해결**  
`RED`, `YELLOW`, `GREEN`, `OPEN`, `CLOSE`, `OFF`로 규격 통일

## 프로젝트 결과

- ROS2와 Arduino 간 양방향 Serial 통신 구현
- 센서값을 네 개의 Topic으로 분리
- 복수 센서 기반 위험 상태 판단
- 데이터 형식 표준화를 통한 통신 안정성 개선

## 폴더 안내

- `README.md`: 프로젝트 핵심 내용
- `docs/`: 설계·요구사항 등 상세 문서
- `images/`: 실행 화면이나 구성도 추가 위치

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드는 각 원본 GitHub 저장소에서 관리합니다.
