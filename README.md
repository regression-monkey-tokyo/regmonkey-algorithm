# Regression Monkey Algorithm

アルゴリズムとデータ構造の学習ノートをまとめる Quarto Book です．

## ローカルでの表示

[Quarto CLI](https://quarto.org/docs/get-started/) をインストールし，リポジトリのルートで実行します．Quarto 1.10.19 で動作確認しています．

Python は `.python-version`，依存パッケージは `uv.lock` に従って準備します．
図のコンパイルには Rust／Cargo でインストールした tikzc を使います．

```bash
uv python install
uv sync --locked --group book
cargo install --git https://github.com/RyoNakagami/tikzc --rev cd1df4ceca054cd9d477510d7161170d0070a4aa --locked tikzc
uv run --locked --group book quarto preview
```

ブラウザーで <http://localhost:4213> を開きます．終了は `Ctrl+C` です．
CI では Rust 1.99.1，Quarto 1.10.19，uv 0.13.4，tikzc v1.3.0 の上記コミットを使用します．

## ビルド

```bash
uv run --locked --group book quarto render --to html
uv run --locked --group book quarto render --to epub
```

HTML は `_book/index.html`，EPUB は `_book/` 内に生成されます．
両方をまとめて生成する場合は `uv run --locked --group book quarto render --to all` を実行します．
生成物と Quarto のキャッシュは Git の追跡対象から除外しています．

## ファイル構成

| パス | 役割 |
|:--|:--|
| `_quarto.yml` | 書籍情報，章の順序，テーマ，出力形式 |
| `index.qmd` | はじめに |
| `summary.qmd` | 本書の構成 |
| `notation.qmd` | 記法 |
| `notes/foundations/` | アルゴリズムの基礎と計算量 |
| `notes/search/` | 二分探索 |
| `glossary.qmd` | 用語集 |
| `references.qmd` / `references.bib` | 参考文献 |
| `include/scss/` | 共通スタイルとライト／ダークテーマ |
| `include/math/mathjax.html` | MathJax の設定 |
| `figures/` | サブディレクトリに配置した `.tikz` と生成 SVG |
| `scripts/compile_figures.py` | `.tikz` を再帰的に SVG へ変換 |
| `.github/workflows/publish.yml` | ビルド検証と GitHub Pages への公開 |

## 章の追加

1. `notes/` の適切なディレクトリに `.qmd` を作成します．
2. ファイルの先頭に `# 章のタイトル` を記述します．
3. `_quarto.yml` の `book.chapters` にそのパスを追加します．
4. `summary.qmd` を更新し，`uv run --locked --group book quarto render --to html` で確認します．

日本語の句読点には `，` と `．` を使います．
表示専用のコード例には `python` フェンス，実行するコードセルには `{python}` フェンスを使います．
Jupyter の実行に必要なパッケージは `book` グループに含めています．追加のライブラリは `uv add --group book <package>` で登録し，`pyproject.toml` と `uv.lock` を一緒に管理します．
CI は毎回 Python セルを実行し，実行エラーがあれば公開を中止します．

## TikZ から SVG への自動変換

`figures/` 以下に `.tikz` を配置すると，Quarto の `pre-render` がサブディレクトリを再帰的に探索し，同じ場所に同名の `.svg` を生成します．

```text
figures/
  search/
    binary-search.tikz
    binary-search.svg  # Generated
  sorting/
    merge-sort.tikz
    merge-sort.svg     # Generated
```

`notes/search/binary-search.qmd` から参照する例です．

```markdown
![二分探索の流れ](../../figures/search/binary-search.svg){#fig-binary-search}
```

`.tikz` を管理対象にし，このディレクトリ内の `.svg` は生成専用として Git から除外します．
SVG は `_book/figures/` にもコピーされます．変換エラーが一つでもあれば，ビルドと公開は失敗します．
`.tikz` がない場合は変換をスキップします．図だけを更新する場合や，プレビュー中に `.tikz` の変更が反映されない場合は次を実行します．

```bash
uv run --locked --group book python scripts/compile_figures.py
```

## 参考にしたプロジェクト

- `regression-monkey-nonparametric`：章立て，サイドバー，Cosmo／Darkly テーマ，参考文献の構成．
- `regmonkey-datascience-blog-new`：日本語設定，青／緑のアクセント，MathJax を一度だけ読み込む構成．

MathJax は CDN から読み込むため，数式のブラウザー表示にはインターネット接続が必要です．フォントは端末にあるものを順に使用します．

## 公開先

`_quarto.yml` の URL は，このリポジトリの remote に合わせています．
GitHub の **Settings → Pages → Build and deployment → Source** を **GitHub Actions** に設定します．
workflow を含む変更が `main` に push されると，次の処理が走ります．

1. Python の依存関係を復元し，Cargo で tikzc をインストールします．tikzc はキャッシュがあれば再利用します．
2. `figures/**/*.tikz` を SVG に変換し，Python セルを実行して HTML／EPUB を生成します．
3. 成功した `_book/` を GitHub Pages に公開します．

PR はビルド検証のみを実行します．Actions タブから `Build and publish Quarto book` を手動実行する場合も，公開するブランチは `main` です．
`gh-pages` ブランチや手動の `quarto publish` は使わず，Pages の artifact として公開します．
ローカルでのレンダリングでは公開されません．
詳細は [GitHub Pages のカスタム workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)を参照してください．

## ライセンス

[MIT License](LICENSE)
