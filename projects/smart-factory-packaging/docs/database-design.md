# Database Design

## 핵심 테이블

- `USERS`: 작업자·관리자 계정 및 권한
- `PRODUCTION_SESSIONS`: 작업자의 생산 작업 단위
- `PRODUCT_TYPES`: 제품 종류 및 세트 기준
- `PRODUCTS`: 인식된 개별 제품과 판정 결과
- `SYSTEM_COMPONENTS`: 센서·카메라·AI·컨베이어 등 구성요소 상태
- `ALERTS`: 오류·경고·박스 완료 알림 이력

## 주요 관계

```text
USERS 1 ─── N PRODUCTION_SESSIONS
PRODUCTION_SESSIONS 1 ─── N PRODUCTS
PRODUCT_TYPES 1 ─── N PRODUCTS
PRODUCTION_SESSIONS 1 ─── N ALERTS
PRODUCTS 1 ─── N ALERTS
SYSTEM_COMPONENTS 1 ─── N ALERTS
USERS 1 ─── N ALERTS
```

PRODUCTS에 작업자 ID를 중복 저장하지 않고 `session_id`를 통해 작업자를 추적합니다.
이를 통해 작업자별 생산 실적과 생산 중 발생한 오류를 같은 세션 기준으로 조회할 수 있습니다.
