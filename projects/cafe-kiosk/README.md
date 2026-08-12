# Cafe Kiosk

> 메뉴 주문과 결제 흐름을 구현한 키오스크 프로젝트

## 실행 화면

<p align="center">
  <img src="https://github.com/user-attachments/assets/99563855-d6e9-4ec2-be43-4d88119a0355" width="600" alt="Cafe Kiosk 실행 화면"/>
</p>

<br>

## 실행 영상

https://github.com/user-attachments/assets/d871907f-6564-4364-bd08-e2080f7dd60e

<br>

🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-dotnet-2026/blob/main/README2.md#11-카페-키오스크-개발)

---

## 프로젝트 개요

카페 메뉴를 선택하고 수량과 주문 금액을 확인한 뒤
결제 단계까지 진행할 수 있도록 사용자 주문 흐름을 구현한 키오스크 프로젝트입니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 주요 기능 | 메뉴 조회, 장바구니, 수량 변경, 주문 |
| 핵심 개념 | 상태 관리, 이벤트 처리, 주문 금액 계산 |
| 형태 | 학습·미니 프로젝트 |
| 목적 | 사용자 주문 흐름과 UI 로직 구현 |

## 주요 기능

- 카테고리별 메뉴 표시
- 메뉴 선택과 장바구니 추가
- 수량 변경과 항목 삭제
- 총 주문 금액 자동 계산
- 주문 초기화와 결제 완료 처리

## 시스템 흐름

```text
Menu Category
    ↓
Product Selection
    ↓
Cart
    ↓
Quantity / Total Calculation
    ↓
Order Confirmation
```

## 대표 트러블슈팅

### 1. 합계 불일치

**문제**  
수량 변경 후 전체 금액이 즉시 반영되지 않음

**해결**  
장바구니 상태 변경 시 전체 항목을 다시 계산

### 2. 중복 메뉴

**문제**  
같은 메뉴를 여러 번 누르면 별도 행으로 추가됨

**해결**  
기존 항목을 검색해 수량만 증가하도록 수정

## 프로젝트 결과

- 사용자 입력에 따른 주문 상태 관리
- 메뉴·수량·금액 계산 로직 구현
- 키오스크 화면 흐름과 예외 상황 이해

## 폴더 안내

- `README.md`: 프로젝트 핵심 내용
- `docs/`: 설계·요구사항 등 상세 문서
- `images/`: 실행 화면이나 구성도 추가 위치

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드는 각 원본 GitHub 저장소에서 관리합니다.
