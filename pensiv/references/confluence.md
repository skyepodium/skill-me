# 개인용 컨플루언스 업로드

**현재 구현되어 있지 않다.** 위키 계정이 생기면 이 문서대로 붙인다. 그 전까지
pensiv는 로컬 보관만 하고, 스킬은 "위키 설정 없음"이라고 보고하고 멈춘다.

## 붙이는 지점

`<root>/pensiv.json`:

```json
{
  "confluence": {
    "base_url": "https://<your-site>.atlassian.net/wiki",
    "space_key": "~personal",
    "parent_page_id": "123456",
    "user_email": "skyepodium@gmail.com",
    "token_env": "CONFLUENCE_API_TOKEN"
  }
}
```

토큰 값은 절대 이 파일에도, 저장소에도 넣지 않는다. `token_env`가 가리키는 환경
변수에서만 읽는다. 값이 비어 있으면 업로드를 시도하지 말고 그 사실을 보고한다.

## 먼저 확인할 것 — 스타일은 거의 살아남지 않는다

컨플루언스는 임의의 HTML을 그대로 받지 않는다.

- **Cloud**는 본문을 *storage format*(XHTML 기반의 제한된 태그 집합)으로 저장한다.
  `<style>`, `<script>`, 대부분의 인라인 CSS가 제거된다. 기본 제공되는 HTML 매크로는
  없다 (마켓플레이스 앱이 필요하다).
- **Data Center / Server**는 관리자가 켜둔 경우 HTML 매크로를 쓸 수 있다.

그래서 공들여 만든 페이지를 그대로 올릴 방법은 사실상 없다. 현실적인 선택지는 둘이다.

1. **첨부 + 요약** (권장) — HTML 파일을 그 페이지의 첨부로 올리고, 본문에는 제목,
   날짜, 메모, 태그, 펜시브 경로만 적는다. 원본 모양은 첨부를 내려받아 보면 된다.
2. **본문 변환** — 제목·문단·표·목록만 storage format으로 옮기고 디자인은 버린다.
   글이 중심인 문서라면 이쪽이 읽기 편하다.

어느 쪽이든 **펜시브 쪽이 원본이고 위키는 사본**이다. 반대로 두지 않는다.

## API 메모

쓰기 전에 각자의 인스턴스에서 확인할 것. 버전에 따라 경로가 다르다.

- 인증: Basic. 사용자 이메일 + API 토큰.
- 페이지 생성 (Cloud v2): `POST {base_url}/api/v2/pages`,
  본문은 `{"representation": "storage", "value": "<p>…</p>"}`.
- 첨부: `PUT {base_url}/rest/api/content/{pageId}/child/attachment`,
  멀티파트, 헤더에 `X-Atlassian-Token: no-check`.
- 같은 항목을 다시 올릴 때는 새 페이지를 만들지 말고 기존 페이지를 갱신한다.
  `meta.json`에 `wiki_page_id`를 적어두고 그걸 기준으로 삼는다.

## 구현할 때 지켜야 할 것

- 로컬 보관을 먼저 끝내고 업로드한다. 업로드가 실패해도 항목은 남아야 한다.
- 성공했을 때만 `meta.json`에 `wiki_url`과 `wiki_page_id`를 쓴다.
- 실패하면 돌아온 상태 코드와 메시지를 그대로 보고한다. 추측해서 성공이라고 하지
  않는다.
- 회사 자료를 개인 공간에 올리는 것이 맞는지는 매번 사람이 판단한다. 스킬이 알아서
  정하지 않는다.
