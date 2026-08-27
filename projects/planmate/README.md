# PlanMate

> C++ 콘솔 기반 일정·할일 관리 프로그램

## 실행 화면

### 기본 화면

<p align="center">
  <img src="https://github.com/user-attachments/assets/be99dadf-775b-48d1-a063-26bf381e2ac2" width="700" alt="PlanMate 기본 화면"/>
</p>

<br>

### 일정 추가

<p align="center">
  <img src="https://github.com/user-attachments/assets/367f1ecf-8d5e-4e9a-b7ac-73ef1b9a3aad" width="700" alt="PlanMate 일정 추가 화면"/>
</p>

<br>

🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-cpp-2026-mini-project/tree/main#track1)

---

## 프로젝트 개요

사용자 입력 기반 메뉴형 프로그램에서 시작해,
날짜를 중심으로 일정과 할일을 함께 관리하는 달력형 콘솔 애플리케이션으로 발전시킨 프로젝트입니다.

기능 추가에 그치지 않고 입력 안정성, 데이터 구조, 화면 흐름을 반복적으로 개선했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| Language | C++ |
| 핵심 개념 | OOP, STL vector, sort, File I/O, Exception Handling |
| 저장 방식 | tasks.txt 자동 저장·불러오기 |

## 주요 기능

- 일정·할일 추가, 조회, 수정, 삭제
- 완료 상태와 우선순위 관리
- 날짜·유형·우선순위 기준 정렬
- 달력에서 일정이 있는 날짜 표시
- 선택 날짜의 상세 일정 조회
- 파일 저장과 실행 시 자동 불러오기

## 시스템 흐름

```text
Program Start
    ↓
tasks.txt Load
    ↓
Calendar Display
    ↓
Date Selection
    ↓
Schedule / Todo CRUD
    ↓
Auto Save

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드와 상세 개발 과정은 원본 GitHub 저장소에서 관리합니다.