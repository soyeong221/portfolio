# Smart Factory Packaging Alert System

> AI 기반 제품 분류와 작업자 포장 알림을 제공하는 스마트팩토리 팀 프로젝트

> 🚧 **현재 개발 진행 중인 팀 프로젝트입니다.**

## 시스템 아키텍처

<p align="center">
  <img src="https://github.com/user-attachments/assets/d695a594-d3a1-4d8d-973d-6c3d63892e49" width="1000" alt="Smart Factory Packaging Alert System ERD"/>
</p>

<br>

## ERD

<p align="center">
  <img src="https://github.com/user-attachments/assets/f8692914-2d8f-4b67-af39-0f04a263ae9e" width="1000" alt="Smart Factory Packaging Alert System 시스템 아키텍처"/>
</p>

<br>

## 프로젝트 개요

컨베이어로 이동하는 제품을 카메라로 인식하고 제품 종류와 생산량을 집계한 뒤,
박스 적재가 완료되면 작업자에게 포장이 필요하다는 알림을 제공하는 시스템입니다.

실제 밀봉·포장 장치 대신 제품 분류, 생산 이력 관리, 박스 완료 감지,
작업자 알림 및 관리자 모니터링에 초점을 맞춰 개발하고 있습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 팀 프로젝트 (진행 중) |
| 핵심 기술 | Python, Raspberry Pi, OpenCV, YOLO, MQTT, MySQL |
| 하드웨어 | 컨베이어, 카메라, 센서, 서보모터, LCD, LED, 부저 |
| 담당 | 작업자용 PyQt5 UI 개발, MQTT 통신 연동, 요구사항 정리, DB 설계, 일정·회의록 관리 |

## 현재 진행 내용

- 요구사항 정의 및 프로젝트 구현 범위 확정
- 전체 시스템 아키텍처 설계
- 6개 핵심 테이블 기반 DB 및 ERD 설계
- Raspberry Pi 기반 작업자용 PyQt5 UI 개발
- MQTT 기반 시스템 간 통신 연동
- 요구사항·DB 설계·회의록 등 프로젝트 산출물 관리

> 이 프로젝트는 현재 개발 진행 중이며, 구현 진행에 따라 실행 화면과 주요 기능을 추가할 예정입니다.
