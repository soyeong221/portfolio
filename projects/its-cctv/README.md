# ITS CCTV Monitoring System

> ITS OpenAPI 기반 실시간 CCTV 영상·지도 통합 모니터링

## 프로젝트 개요

ITS OpenAPI에서 전국 CCTV 위치와 영상 URL을 가져와
WPF 애플리케이션에서 지도·영상·상세 정보를 통합 제공하는 시스템입니다.
ASP.NET Core Web API를 중계 계층으로 두어 외부 API 데이터와
WPF 클라이언트 간의 데이터 흐름을 분리했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| Client | C#, WPF, WebView2, LibVLCSharp |
| Server | ASP.NET Core Web API |
| Map | Leaflet.js |
| Data | ITS OpenAPI, CCTV 위치·HLS URL |

## 주요 기능

- ITS OpenAPI 기반 CCTV 목록 조회
- 지도 마커와 CCTV 위치 시각화
- HLS 실시간 영상 재생
- 선택 CCTV 상세 정보 표시
- WPF 클라이언트와 ASP.NET Core API 연동
- WebView2를 통한 Leaflet 지도 통합

## 시스템 흐름

```text
ITS OpenAPI
    ↓
ASP.NET Core Web API
    ↓ JSON
WPF Client
    ├─ CCTV List
    ├─ LibVLCSharp HLS Player
    └─ WebView2 + Leaflet Map
```

## 대표 트러블슈팅

### 1. 404 응답

**문제**  
클라이언트 요청 경로와 API Controller Route가 일치하지 않음

**해결**  
BaseAddress와 endpoint 경로를 분리해 실제 Route에 맞게 수정

### 2. 포트 불일치

**문제**  
API 실행 포트를 변경했지만 WPF 설정은 기존 포트를 참조

**해결**  
launchSettings와 HttpClient BaseAddress를 동일하게 맞춤

### 3. 지도·영상 연계

**문제**  
지도에서 선택한 마커와 WPF 영상 정보 동기화 필요

**해결**  
WebView2 JavaScript 메시지와 WPF 이벤트를 연결

## 프로젝트 결과

- 외부 API–서버–클라이언트 데이터 연계 구조 구현
- 지도와 실시간 영상을 한 화면에 통합
- API 경로·포트 오류를 단계별로 분석해 안정화
- 시스템 구성과 데이터 흐름 문서화

## 폴더 안내

- `README.md`: 프로젝트 핵심 내용
- `docs/`: 설계·요구사항 등 상세 문서
- `images/`: 실행 화면이나 구성도 추가 위치

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드는 각 원본 GitHub 저장소에서 관리합니다.
