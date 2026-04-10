# 🛒 쇼핑 리스트 앱

순수 HTML/CSS/JS로 만든 로컬 쇼핑 리스트 웹 앱입니다.

## 기능

- 아이템 추가 (버튼 클릭 또는 Enter)
- 아이템 삭제
- 체크(완료) 표시 및 해제
- 전체 / 미완료 / 완료 필터
- 완료 항목 일괄 삭제
- `localStorage`에 자동 저장 (새로고침 후에도 유지)

## 실행 방법

`shopping_list.html` 파일을 브라우저에서 열면 바로 실행됩니다.

## 자동 테스트

Playwright 기반 자동 테스트 포함 (15개 테스트 케이스)

```bash
pip install playwright
python -m playwright install chromium
python -X utf8 test_shopping_list.py
```

### 테스트 항목

| 섹션 | 테스트 |
|------|--------|
| 아이템 추가 | 버튼/Enter 키 추가, 빈 입력 무시 |
| 통계 표시 | 완료 카운터 정확성 |
| 체크 기능 | checked 클래스, 취소선 CSS, 통계 갱신, 해제 |
| 필터 | 미완료 / 완료 / 전체 전환 |
| 삭제 | 개별 항목 삭제 |
| 일괄 삭제 | 완료 항목 전체 삭제, 빈 목록 메시지 |
| 영속성 | localStorage 저장 + 새로고침 복원 |
