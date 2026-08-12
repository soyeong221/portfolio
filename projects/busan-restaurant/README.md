# Busan Restaurant Data Service

> 부산 공공데이터를 활용한 맛집 정보 조회·상세정보 및 랜덤 추천 애플리케이션

## 실행 화면

<p align="center">
  <img src="https://github.com/user-attachments/assets/5b390f32-14bd-4c89-a993-2cb7d9aaa760" width="600" alt="Busan Restaurant Data Service 실행 화면"/>
</p>

<br>

### 실행 영상

https://github.com/user-attachments/assets/ae3f8def-134a-423c-941e-343ef4586461

<br>

🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-dotnet-2026/blob/main/README2.md#openapi를-사용한-맛집정보제공-앱-wpfbusanfoodapp)

---

## 프로젝트 개요

부산광역시 부산맛집정보 서비스를 활용하여 부산 지역 맛집 정보를 조회하고
상세정보를 확인할 수 있도록 구현한 애플리케이션입니다.

페이지 번호와 결과 수를 지정해 맛집 데이터를 조회할 수 있으며,
선택한 맛집의 대표 이미지, 주소, 지도, 대표메뉴, 전화번호, 홈페이지,
상세 설명을 별도의 상세정보 창에서 확인할 수 있도록 구성했습니다.

또한 현재 조회된 맛집 중 하나를 무작위로 선택해 상세정보를 보여주는
`오늘 뭐 먹지?` 기능과 NLog 기반 로그 기록 기능을 추가했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 데이터 | 부산광역시 부산맛집정보 서비스 |
| 주요 기능 | 맛집 목록 조회, 상세정보 조회, 랜덤 맛집 추천 |
| 화면 구성 | 맛집 목록, 상세정보 창, 상태표시줄 |
| 부가 기능 | 홈페이지 연결, 지도 표시, NLog 로그 기록 |
| 형태 | 학습·미니 프로젝트 |

## 주요 기능

<p align="center">
  <img src="https://github.com/user-attachments/assets/7633b677-264b-4f2e-9b1f-9510607a7adc" width="600" alt="맛집 목록 조회 화면"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/d33c55b5-91e6-45f9-8903-05dcda33bc9a" width="600" alt="맛집 상세정보 화면"/>
</p>

- 페이지 번호와 결과 수를 이용한 맛집 데이터 조회
- 맛집명, 구군, 주소, 대표메뉴, 전화번호 표시
- 페이지 번호와 결과 수를 기준으로 화면 표시용 순번 계산
- 선택한 맛집의 상세정보를 별도 창에 표시
- 대표 이미지, 주소, 지도, 대표메뉴, 전화번호, 홈페이지, 상세 설명 제공
- 홈페이지 링크 클릭 시 기본 브라우저 실행
- 상태표시줄에 데이터 로드 결과 표시

<br>

<p align="center">
  <img src="https://github.com/user-attachments/assets/5ee2fdc5-08c3-4440-b02b-c244dd1f5e13" width="600" alt="NLog 로그 기록 화면"/>
</p>

- NLog를 이용한 앱 실행 및 API 조회 로그 기록

<br>

<p align="center">
  <img src="https://github.com/user-attachments/assets/cedd7392-35f8-4db3-a9ba-0bedd63366d1" width="600" alt="오늘 뭐 먹지 랜덤 추천 화면"/>
</p>

- 현재 조회된 맛집 중 하나를 무작위로 선택하는 `오늘 뭐 먹지?` 기능

## 시스템 흐름

```text
부산광역시 부산맛집정보 서비스
            ↓
       맛집 데이터 조회
            ↓
       맛집 목록 표시
            ↓
   ┌────────┴────────┐
   ↓                 ↓
맛집 선택       오늘 뭐 먹지?
   ↓                 ↓
상세정보 선택     랜덤 맛집 선택
   └────────┬────────┘
            ↓
       상세정보 창
            ↓
 이미지 / 주소 / 지도 / 대표메뉴
 전화번호 / 홈페이지 / 상세 설명
