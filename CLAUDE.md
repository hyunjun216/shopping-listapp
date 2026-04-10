# 프로젝트 규칙

## 언어 & 환경
- Python 3.x 사용
- 패키지 관리: `pip` (requirements.txt 유지)
- 가상환경: `venv` 사용 권장

## 데이터 분석 스택
- 데이터 처리: `pandas`, `numpy`
- 시각화: `matplotlib`, `seaborn`
- 머신러닝: `scikit-learn`
- 노트북: `jupyter`

## 코딩 규칙
- 변수명, 함수명: snake_case
- 함수마다 docstring 작성
- 매직 넘버 금지 — 상수로 분리
- 한 함수는 한 가지 역할만

## 파일 구조
```
project/
├── data/           # 원본 데이터 (git 제외 권장)
├── notebooks/      # 탐색적 분석 (EDA)
├── src/            # 재사용 가능한 코드
├── outputs/        # 결과물 (그래프, 리포트)
├── requirements.txt
└── CLAUDE.md
```

## 데이터 작업 규칙
- 원본 데이터는 절대 수정하지 않음 (read-only)
- 전처리 과정은 코드로 재현 가능하게 작성
- 데이터 경로는 하드코딩 금지 — 변수나 config로 관리

## 금지 사항
- `import *` 사용 금지
- 민감한 데이터(개인정보, API 키)를 코드에 직접 작성 금지
- 분석 결과를 설명 없이 숫자만 출력 금지
