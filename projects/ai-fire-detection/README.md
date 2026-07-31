# AI Fire Detection Monitoring

> YOLO와 MQTT를 활용한 실시간 화재 감지 및 경보 시스템

## 프로젝트 개요

카메라 영상을 YOLO로 분석해 화재 여부를 판정하고, 감지 결과와 처리 영상을
MQTT WebSocket으로 브라우저에 전달하는 실시간 모니터링 시스템입니다.
단일 프레임 오탐으로 경보가 반복되지 않도록 연속 감지 횟수와 정상 감지 횟수,
알람 재발생 대기시간을 적용했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 개인 실습 프로젝트 |
| 핵심 기술 | Python, OpenCV, YOLOv8, MQTT, JavaScript |
| 통신 | Mosquitto WebSocket, JSON, Base64 Image |
| 핵심 기능 | 영상 분석, 연속 감지 판정, 경보 쿨다운 |

## 주요 기능

- OpenCV 기반 영상 프레임 처리
- YOLOv8 객체 탐지 모델 연동
- 감지 결과와 Base64 이미지를 JSON으로 MQTT 발행
- 브라우저에서 실시간 영상과 화재 상태 표시
- 연속 감지 임계값 기반 화재 경보
- 정상 프레임 누적과 쿨다운을 이용한 알람 반복 방지

## 시스템 흐름

```text
Camera / Video
    ↓
OpenCV Frame Processing
    ↓
YOLO Object Detection
    ↓
detect + Base64 image
    ↓ MQTT WebSocket
Browser Monitoring
    ↓
연속 감지 임계값 확인
    ↓
화재 알림 표시
```

## 대표 트러블슈팅

### 1. 조건문 오타

**문제**  
`if (firedetect) >= FIRE_DETECT_THRESHOLD`처럼 boolean 값과 숫자를 잘못 비교

**해결**  
`fireDetectCount >= FIRE_DETECT_THRESHOLD`로 수정해 누적 감지 횟수를 기준으로 판정

### 2. 알람 반복

**문제**  
화재가 계속 탐지되면 매 프레임마다 알람이 발생

**해결**  
`lastAlarmTime`과 `ALARM_COOLDOWN`을 두어 일정 시간 후에만 재알림

### 3. MQTT 연결

**문제**  
브라우저와 일반 MQTT TCP 포트를 직접 연결할 수 없음

**해결**  
Mosquitto WebSocket listener를 9001 포트로 구성하고 웹 클라이언트는 WebSocket으로 접속

## 프로젝트 결과

- AI 감지 결과를 실시간 웹 화면으로 전달
- 오탐과 중복 알림을 줄이는 누적 판정 로직 구현
- 영상·판정값을 하나의 JSON 메시지로 통합
- MQTT 기반 느슨하게 결합된 실시간 모니터링 구조 이해

## 폴더 안내

- `README.md`: 프로젝트 핵심 내용
- `docs/`: 설계·요구사항 등 상세 문서
- `images/`: 실행 화면이나 구성도 추가 위치

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드는 각 원본 GitHub 저장소에서 관리합니다.
