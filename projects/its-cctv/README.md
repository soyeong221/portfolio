# ITS CCTV Monitoring System

> ITS OpenAPI 기반 실시간 CCTV 영상·지도 통합 모니터링 시스템

## 실행 화면

<p align="center">
  <img src="https://github.com/user-attachments/assets/ed683467-1581-406e-b848-3ecdbaa022f7" width="600" alt="ITS CCTV Monitoring System 실행 화면"/>
</p>

<br>

## 실행 영상

https://github.com/user-attachments/assets/4ca559a0-485a-4708-af60-494a696dbcf1

<br>

🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-dotnet-2026/blob/main/TOYPROJECT1.md#국가교통정보센터-cctv-모니터링-시스템)

---

## 프로젝트 개요

국가교통정보센터 ITS Open API를 활용하여 전국 고속도로·국도 CCTV를 검색하고,
실시간 영상과 위치 정보를 함께 확인할 수 있도록 구현한 WPF 기반 데스크톱 애플리케이션입니다.

WPF 클라이언트가 외부 Open API를 직접 호출하지 않고,
ASP.NET Core Web API로 구현한 브릿지 서버를 통해 데이터를 전달받도록 구성했습니다.

이를 통해 API 인증키를 클라이언트에서 분리하고,
외부 API 요청과 화면 표시 기능의 역할을 구분했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 프로젝트 유형 | 개인 토이 프로젝트 |
| Client | C#, WPF, Wpf.Ui, WebView2, LibVLCSharp |
| Server | ASP.NET Core Web API |
| Map | Leaflet.js |
| Data | 국가교통정보센터 ITS Open API |
| 주요 기능 | CCTV 검색, 실시간 영상 재생, 지도 표시, 상세정보 조회 |

## 주요 기능

<p align="left">
  <img src="https://github.com/user-attachments/assets/80429187-bc10-4f9d-beac-4c54fcae1f64" width="600" alt="ITS CCTV 기본 화면"/>
</p>

- 전국 시·도 단위의 위도·경도 범위를 이용한 CCTV 검색
- 고속도로와 국도 CCTV 구분 조회
- 검색 중 ProgressBar를 이용한 진행 상태 표시
- 초기화 버튼을 통한 검색 조건, 목록, 영상 및 지도 초기화

<br>

<p align="left">
  <img src="https://github.com/user-attachments/assets/ed683467-1581-406e-b848-3ecdbaa022f7" width="600" alt="ITS CCTV 정상 실행 화면"/>
</p>

- LibVLCSharp을 활용한 HLS 실시간 영상 재생
- WebView2와 Leaflet.js를 활용한 CCTV 위치 지도 표시
- 선택한 CCTV의 이름, 좌표, 영상 URL 등 상세정보 제공
- WPF 클라이언트와 ASP.NET Core Web API 연동

<br>

<p align="left">
  <img src="https://github.com/user-attachments/assets/4bc9016a-a79a-49c4-bb1c-511f9954893f" width="600" alt="ITS CCTV 스트리밍 연결 불량 화면"/>
</p>

- 스트리밍 연결 성공·실패 상태 표시
- 영상 재생 실패 및 API 키 누락 등에 대한 예외 처리

## 시스템 흐름

```text
국가교통정보센터 ITS Open API
            ↓
     HTTP / API Request
            ↓
ASP.NET Core Web API
      (Bridge Server)
            ↓
        HTTP / JSON
            ↓
        WPF Client
       ├─ CCTV List
       ├─ LibVLCSharp HLS Player
       ├─ WebView2 + Leaflet Map
       └─ CCTV Detail
