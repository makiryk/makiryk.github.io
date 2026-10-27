# makiryk.github.io

K.Ejima のサイト（GitHub Pages）。名刺の QR コードの行き先。

- `index.html` と `style.css` だけの静的サイト（ビルド不要）。アイコンは `index.html` 冒頭の SVG シンボルにまとめてある。
- 「作ったもの」と「いま」は `content/works.json`・`content/now.json` から `python tools/build.py` で生成する（`index.html` の該当箇所は手で直さない）。手順は Claude Code のスキル `site-update`。
- `tools/`・`content/`・`drafts/`・`README.md` は `_config.yml` で公開対象から外している。
- 公開先: https://makiryk.github.io/
