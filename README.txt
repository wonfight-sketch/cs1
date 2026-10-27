청렴 신고 웹사이트 + 자동 RSS 갱신

중요: ZIP을 Netlify Drop에 올리기만 해서는 자동 갱신이 작동하지 않습니다.
1. GitHub에서 새 저장소를 만들고 이 폴더의 파일/숨김 .github 폴더까지 업로드합니다.
2. GitHub 저장소 Actions 탭 > Update government press releases > Run workflow를 실행합니다.
3. news.json에 실제 보도자료 5건 이상 저장됐는지 확인합니다.
4. Netlify > Add new project > Import an existing project > GitHub에서 해당 저장소를 연결합니다.
5. Build command는 비워 두고 Publish directory는 . (루트)로 설정합니다.
6. GitHub Actions가 매일 한국시간 09:17, 15:17, 21:17에 RSS를 수집하여 news.json을 업데이트합니다.
7. 변경이 push되면 Netlify가 자동 재배포합니다. GitHub/Netlify 무료 플랜의 일정 지연이나 제한은 있을 수 있습니다.

수동 새로고침: GitHub Actions > Update government press releases > Run workflow
RSS 공급처: https://www.korea.kr/rss/dept_mois.xml
실패 시 이전 news.json 유지. 최초 수집 전에는 보도자료가 표시되지 않습니다.
