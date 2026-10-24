# Archive layout

```
~/dev/pensiv/
├── index.html                      생성물. 손대지 않는다
├── pensiv.json                     선택. 위키 설정이 생기면 여기에
├── 2026-10-24-stackchan-boreum/
│   ├── index.html                  담긴 페이지. 혼자 열리는 문서
│   ├── original.html               손대기 전 원본. 감쌌을 때만 생긴다
│   ├── meta.json                   색인이 읽는 것
│   └── <에셋들>                     --asset 으로 같이 넣은 파일
└── 2026-11-08-core2-first-boot/
    └── ...
```

## meta.json

| 필드 | 뜻 |
|---|---|
| `title` | 색인에 뜨는 이름. 기본값은 HTML의 `<title>` |
| `date` | 폴더 이름에 쓰인 날짜. 색인 정렬 기준 |
| `created` | 처음 담은 날. 같은 항목을 갱신해도 안 바뀐다 |
| `updated` | 마지막으로 담은 시각 |
| `file` | 폴더 안의 진입 파일. 항상 `index.html` |
| `tags` | 문자열 배열 |
| `source` | 원본 링크. 아티팩트 URL, 위키 주소, 티켓 |
| `note` | 한 줄 메모 |
| `origin` | 담을 때의 원본 파일 경로. 어디서 왔는지 추적용 |
| `assets` | 같이 복사한 파일 이름들 |
| `normalized` | `wrapped`(문서로 감쌈), `charset`(charset만 넣음), `null`(손 안 댐) |
| `remote_hosts` | 페이지가 부르는 외부 호스트. 있으면 색인에 `외부 리소스` 배지 |

`normalized`가 null이 아니면 같은 폴더에 `original.html`이 있다. 담긴 `index.html`은
열리는 것을 보장하고, `original.html`은 받은 그대로를 보장한다. 둘 다 남긴다.

손으로 고쳐도 된다. 고친 뒤 `rebuild_index.py`를 돌리면 색인에 반영된다.

## 루트 바꾸기

우선순위는 `--root` > `$PENSIV_ROOT` > `~/dev/pensiv`.

다른 곳으로 옮기려면 폴더를 통째로 옮기고 거기서 색인을 다시 만든다:

```
mv ~/dev/pensiv ~/Documents/pensiv
python3 scripts/rebuild_index.py --root ~/Documents/pensiv
```

색인은 상대 경로로 링크하므로 폴더를 옮겨도 링크는 안 깨진다. 헤더에 적히는 경로만
다시 쓰인다.

## 손으로 하는 정리

- **지우기** — 항목 폴더를 지우고 `rebuild_index.py`.
- **옮기기 / 이름 바꾸기** — 폴더 이름을 바꾸고 `rebuild_index.py`. `meta.json`의
  `date`는 폴더 이름과 따로 놀 수 있으니, 날짜를 바꿀 거면 둘 다 바꾼다.
- **되돌리기** — 색인은 전부 디스크에서 다시 읽어 만든다. 색인이 깨졌으면 지우고
  다시 만들면 된다. 잃을 게 없다.

## git

펜시브는 개인 보관소라 기본적으로 git을 걸지 않는다. 걸고 싶으면 보통의 저장소처럼
`git init` 하면 된다. 담기는 게 대부분 자체 완결 HTML이라 바이너리가 거의 없어서
diff가 읽힌다. 회사 자료가 섞이는 순간 원격 저장소는 다시 생각할 것.
