# GitHub 업로드 방법

## 새 저장소에 올리기

1. GitHub에서 `portfolio` 저장소를 생성합니다.
2. 이 ZIP의 `portfolio` 폴더 안에 있는 파일 전체를 저장소 최상위에 넣습니다.
3. 아래 명령을 실행합니다.

```bash
git init
git add .
git commit -m "Create portfolio repository"
git branch -M main
git remote add origin https://github.com/soyeong221/portfolio.git
git push -u origin main
```

이미 저장소가 연결되어 있다면 `git init`과 `git remote add origin`은 생략합니다.

## 이미지 추가

각 프로젝트 실행 화면은 해당 프로젝트의 `images/` 폴더에 넣으면 됩니다.
현재 실제 이미지가 확인되지 않은 프로젝트에는 빈 폴더를 유지하기 위해 `.gitkeep`만 들어 있습니다.
