# SmartHome IoT Monitoring System

> MQTT 기반 SmartHome 센싱 데이터 수집·저장 시스템

## 실행 화면

### MQTT Publish

https://github.com/user-attachments/assets/4749c579-4239-4940-846b-4ceea4f8086b

<br>

### MQTT Subscribe

https://github.com/user-attachments/assets/0844072f-f579-4127-a76e-351a69ffcc25

<br>

## 🔗 **Original Project**

> WPF 기반 Dummy Simulator의 센싱 데이터 생성부터 MQTT Broker 구성,
> Publish / Subscribe 및 MySQL 데이터 저장까지의 전체 구현 과정을 확인할 수 있습니다.

[View on GitHub](https://github.com/soyeong221/iot-dotnet-2026/blob/main/README2.md#13-smarthome-솔루션)

---

## 프로젝트 개요

실제 IoT 장치 없이 SmartHome 환경의 데이터 흐름을 구현하기 위해
WPF 기반 Dummy Simulator에서 가상의 센싱 데이터를 생성하고,
MQTT를 통해 송수신하는 시스템을 구성했습니다.

침실·욕실·거실·주방의 온·습도 데이터를 생성하여 JSON 형태로
Eclipse Mosquitto Broker에 Publish하고,
Subscriber에서 데이터를 Subscribe하여 MySQL에 저장하도록 구현했습니다.

MQTT Broker의 Topic 및 접속 환경을 직접 구성하고,
약 20시간 동안 시스템을 실행하여 약 29만 4천 건의
센싱 데이터가 저장되는 것을 확인했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 개인 실습 프로젝트 |
| Language / UI | C#, WPF |
| Messaging | MQTT, MQTTnet |
| Broker | Eclipse Mosquitto |
| Database | MySQL, MySQLConnector |
| Data | SmartHome 온·습도 Dummy Data, JSON |
| 핵심 기능 | 센싱 데이터 생성, MQTT Publish / Subscribe, DB 저장 |

## 주요 기능

- WPF 기반 SmartHome Dummy Simulator 구현
- Bogus Package를 이용한 가상 센싱 데이터 생성
- 침실·욕실·거실·주방 4개 공간의 온·습도 데이터 생성
- 센싱 데이터를 JSON 형태로 변환
- MQTTnet 기반 MQTT Publish / Subscribe 구현
- Eclipse Mosquitto Broker 구축 및 연결
- 세대별 MQTT Topic을 이용한 메시지 구분
- MQTT Subscriber에서 센싱 데이터 수신
- MySQL `sensor_data` 테이블에 수신 데이터 저장
- MQTT Explorer를 이용한 Broker 연결 및 메시지 확인
- 약 20시간 동안 약 29만 4천 건의 센싱 데이터 저장 확인

## 시스템 흐름

```text
SmartHome Dummy Simulator
      (C# / WPF)
           ↓
   Bogus Dummy Data
  온도 / 습도 데이터
           ↓
         JSON
           ↓
     MQTT Publish
           ↓
Eclipse Mosquitto Broker
           ↓
     MQTT Subscribe
           ↓
    Subscriber App
           ↓
        MySQL
     (sensor_data)

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드와 상세 개발 과정은 원본 GitHub 저장소에서 관리합니다.