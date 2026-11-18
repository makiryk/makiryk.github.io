---
name: site-update
description: 個人サイト https://makiryk.github.io/ （リポジトリ C:\cloud\repo\makiryk.github.io）の「作ったもの」と「いま」を更新する手順。作品の追加・削除・並べ替え・説明の変更、開発中バッジの付け外し、「いま」の差し替えを、content/*.json の編集と tools/build.py の実行で行い、表示を確かめてから commit・push する。「サイトに〇〇を追加して」「作ったものを更新」「いまを〇〇にして」「開発中を外して」と言われたら、HTML を直接書き換える前に必ずこのスキルを使う。
---

# 個人サイトの「作ったもの」「いま」を更新する

リポジトリ: `C:\cloud\repo\makiryk.github.io`（公開先 https://makiryk.github.io/ 、`main` に push すると約 30〜40 秒で反映）

`index.html` の「作ったもの」と「いま」は **生成物**。`<!-- works:start -->`〜`end`、`<!-- now:start -->`〜`end` のあいだを手で書き換えない（次の生成で消える）。内容は JSON に書き、スクリプトで作り直す。

## 1. 内容を聞き取る
足りない項目だけをユーザーに聞く。推測で作品の説明を書かない（書いたら「私が書いた文なので確かめて」と伝える）。
- 作品名、ひとこと概要（全角 30 字前後。スマホで 2 行以内）、開発中かどうか
  - 作品名（カードのタイトル）は **リポジトリ名にしない**。何をするものかがわかる日本語の名前にする（例: darts-crowd-map → ダーツ店混雑マップ、BRBouyomi → 棒読みちゃん 区切り読みプラグイン）。製品として決まった呼び名があればそれを使う（例: Alexa スキルの呼び出し名「ジェミニ」）。スマホで 1 行に収まる長さ（全角 17 字程度まで）。
- 中身の流れ（何 → 何 → 何）。これが流れ図とイラストになる
- 公開してよい情報か（非公開リポジトリの作品は、リンクを付けず概要だけにする）

## 2. JSON を編集する
### `content/works.json`（配列。上から順に表示。PC もスマホも 3 列で並び、端数の段は中央に寄る。3 の倍数だときれいにそろう。スマホ（760px 以下）では流れ図を隠し、イラスト・名前・概要だけを出す。流れ図は「→」が次のステップと一緒に折り返す。下の例の `//` は説明用で、実際の JSON には書かない）
```json
{
  "name": "作品名",
  "badge": "開発中",            // 不要なら ""
  "desc": "ひとこと概要。",
  "color": 5,                   // 1〜8。隣と同じ色を避ける
  "scene": [["pin", "l"], ["target", "l"]],
  "flow": ["pin:地図", "arrow", "target:ダーツ店", "arrow", "clock:混雑予測"]
}
```
- `scene`: イラスト。`[アイコン名, 大きさ]` を左から並べる。大きさは `l`=52・`m`=36・`s`=32。アイコンのあいだに 6 ずつ間隔が入り、間隔を含めた合計が 150 以下（自動で中央にそろう）。3 個なら「l・s・l」（148）か「l・s・m」まで。「l・m・l」は 152 で超えるので、真ん中は `s` にする。主役を `l`、あいだの添え物（spark・wave・bolt・split など）を `s` にすると、これまでの作品とそろう。`arrow`・`handoff` はイラストに入れない（四角の中の矢印は違和感があるとユーザーに言われた。build.py もエラーで止める。矢印は流れ図だけで使う）。
- `flow`: 流れ図。`"アイコン名:ラベル"` と、つなぎの `"arrow"`（→）か `"handoff"`（⇄）を交互に並べる。ステップは 2〜3 個、ラベルは短く（スマホで 1 行に収める）。
- 色 1〜8: 緑・青・茶・紫・青緑・赤・黄土・灰（ライト・ダーク両方の値が `style.css` の `--s1`〜`--s8` にある）。

### `content/now.json`（配列。いま取り組んでいること。1〜2 件。複数なら縦に並ぶ）
```json
[{"icon": "target", "text": "ダーツ店の混雑マップを開発中"}]
```

### 使えるアイコン名
spark（AI）, speaker, wave（音声）, handoff（⇄）, robot, pin（地図）, target, car, phone, mail, code, calendar, sheet（表・辞書）, gear, bolt（自動化）, link, clock, folder, arrow, usb, wifi, split（ハサミ・分割）, apps（アプリ群・Google）, pc（モニター）, devices（モニター＋スマホ）, cloud（雲・クラウド）

合うものがなければ、`index.html` 冒頭の `<svg class="defs">` に `<symbol id="i-名前" viewBox="0 0 24 24">…</symbol>` を足す。24×24・線のみ（fill なし、`stroke` は currentColor が継承される）・線幅 2 に収まる単純な形で描く。上に寄った形（robot など）は `tools/build.py` の `NUDGE_Y` で下にずらす。

## 3. 生成する
```
python -X utf8 C:\cloud\repo\makiryk.github.io\tools\build.py
```
（PowerShell ツールで。`built N works, M now items` と出れば成功。存在しないアイコン名・色・幅超過はエラーで止まるので、JSON を直して再実行）

## 4. 表示を確かめる（必須）
Chrome のヘッドレスで撮って Read で見る。ライトとスマホ幅（390px）の両方。
```
$c="C:\Program Files\Google\Chrome\Application\chrome.exe"; $t="<一時フォルダ>"
& $c --headless=new --disable-gpu "--user-data-dir=$t\prof" --blink-settings=preferredColorScheme=1 --virtual-time-budget=8000 --hide-scrollbars --window-size=1280,1500 "--screenshot=$t\pc.png" "file:///C:/cloud/repo/makiryk.github.io/index.html"
```
- スマホ幅は、ウィンドウを 390px にしても最小幅で撮られるので、幅 390px の iframe に入れた HTML を `--allow-file-access-from-files` 付きで撮る。
- この PC の Windows はダークモードなので、ライトを見るには `--blink-settings=preferredColorScheme=1` が要る（ダークは `--force-dark-mode`）。
- 見るところ: イラストのアイコンが枠の中央にあるか、概要と流れ図がスマホで不自然に折り返していないか（1〜2 字だけの行がないか）、カードの並びと中央揃えが崩れていないか。

## 5. commit と公開
- `git add -A` → `git commit`（このリポジトリの user.email は GitHub の noreply に設定済み。個人のメールアドレスや本名をコミットに入れない）。
- push は公開の操作なので、ユーザーに確認してから `git push origin main`。実行できない場合は `! cd /c/cloud/repo/makiryk.github.io && git push origin main` を案内する。
- push 後、`https://makiryk.github.io/?v=<連番>` を取得して新しい内容が含まれるまで待ち（約 30〜40 秒）、反映を確かめてから報告する。

## 守ること
- 本名は「K.Ejima」まで。それ以上（フルネーム・ふりがな）を書かない。
- `tools/`・`content/`・`drafts/`・`README.md` は `_config.yml` で公開対象から外してある。消さない。
- デザイン（配色・中央揃え・カードの形）は変えない。変えるよう頼まれたら、このスキルの範囲外として通常どおり作業する。
