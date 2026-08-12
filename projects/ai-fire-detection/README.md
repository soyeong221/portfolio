# AI Fire Detection Monitoring

> YOLO와 MQTT를 활용한 실시간 화재·연기 감지 및 경보 시스템

## 실행 화면

<p align="center">
  <img src="https://github.com/user-attachments/assets/0d03d636-cd6c-4a09-9757-b8a1138970fe" width="600" alt="AI Fire Detection Monitoring 실행 화면"/>
</p>

<br>

## 실행 영상

https://github.com/user-attachments/assets/2685a4fb-a967-4e5f-b010-a6270ba172b6

<br>

🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-dotnet-2026/blob/main/TOYPROJECT4.md#화재연기-감지-알람시스템)

---

## 프로젝트 개요

YOLO와 OpenCV를 활용한 실시간 객체인식 및 MQTT WebSocket 기반
웹 스트리밍 구조를 학습하고, 이를 화재·연기 감지 시스템으로 확장한 프로젝트입니다.

Python에서 영상 프레임을 분석한 뒤 감지 결과와 처리 영상을
MQTT Broker를 통해 웹 모니터링 화면으로 실시간 전달하도록 구성했습니다.

`firedetect-11s.pt` 사전학습 모델을 적용하여 화재·연기를 감지하고,
연속 감지 횟수와 정상 감지 횟수, 알람 재발생 대기시간을 적용해
반복적인 경보 발생을 줄이도록 구현했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 개인 실습 프로젝트 |
| 핵심 기술 | Python, OpenCV, YOLO, PyTorch, MQTT, JavaScript |
| 통신 | Mosquitto WebSocket, JSON, Base64 Image |
| 핵심 기능 | 화재·연기 감지, 실시간 영상 전달, 연속 감지 판정, 경보 쿨다운 |

## 주요 기능

- OpenCV 기반 웹캠·동영상 프레임 처리
- YOLO 기반 실시간 객체 탐지
- `firedetect-11s.pt` 사전학습 모델을 활용한 화재·연기 감지
- 감지 결과와 Base64 이미지를 JSON으로 MQTT 발행
- Mosquitto Broker와 WebSocket을 이용한 실시간 웹 스트리밍
- 브라우저에서 실시간 영상과 화재 감지 상태 표시
- 연속 감지 임계값 기반 화재 경보
- 정상 프레임 누적과 쿨다운을 이용한 반복 알람 방지

## 시스템 흐름

```text
Camera / Video
      ↓
OpenCV Frame Processing
      ↓
YOLO Fire / Smoke Detection
      ↓
감지 결과 + Base64 Image
      ↓
MQTT Broker
      ↓ WebSocket
Browser Monitoring
      ↓
연속 감지 임계값 확인
      ↓
화재 알림 표시
