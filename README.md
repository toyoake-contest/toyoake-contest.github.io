# README

## セットアップ

サイト作成

```shell
hugo new site toyoake-contest.github.io
```

レポジトリ初期化

```shell
cd toyoake-contest.github.io
git init
echo '*~' >> .gitignore
echo '*.bak' >> .gitignore
echo '*.orig' >> .gitignore
echo '.env' >> .gitignore
echo 'public' >> .gitignore
echo 'resources' >> .gitignore
```

テーマ設定

```shell
git submodule add https://github.com/onweru/newsroom.git themes/newsroom
```

(参考)submoduleの削除

```shell
git submodule deinit -f themes/newsroom
git rm themes/newsroom
rm -fr .git/modules
```

csvファイル用レポジトリ追加(事前に準備しておく)

```shell
git submodule add https://github.com/toyoake-contest/data.git csv
git submodule update --remote
git submodule update --init --recursive
```

サイト設定

```shell
cd ..
cp -pr themes/newsroom/exampleSite/{content,data,config.toml} .
```

config.toml

```toml
baseURL = "https://toyoakekaki.github.io/toyoake-contest.github.io"
languageCode = "ja"
title = "Hugo Newsroom"
theme = "newsroom"
```

> github pagesやnetlifyで使う場合はbaseURLのプロトコルはhttpsにすること

起動確認(http://localhost:1313)

```shell
cp /path/to/someplace/Makefile .
make run
```

Githubレポジトリ作成後

```shell
git remote add origin git@github.com:toyoakekaki/toyoake-contest.github.io.git
git add .
git commit -m 'init'
# <ortanization>.github.ioの場合はmasterブランチが出力なのでソースはsrcブランチで管理
git branch -m src
git push -u origin src
```

Settings>Branches>Default branchでsrc->masterに変更(してもしなくてもよい)

## Github Actionsの利用

* .github/workflows/gh-pages.yamlを作成
    * ソースはsrcブランチ
    * 出力はpublicフォルダの内容をmasterxブランチに

```shell
make deploy
```

* Github>Settings>Gighub Pages>Source>gh-pages branchに設定する
* しばらく時間がかかる

## 既存のレポジトリからクローンする場合

```shell
git clone git@github.com:toyoakekaki/toyoake-contest.github.io.git
cd toyoake-contest.github.io
git submodule update --init --recursive
```

## 使い方

### 事前確認情報

* 品評会ID: 対象の品評会のID(LIST.md参照)
* 品評会ディレクトリ: 対象の品評会のID(LIST.md参照)
    * ポットプランツの場合は品評会IDと同じ
        * 例)
    * 鉢物の場合、東海と全国で品評会IDをハイフン連結
        * 例)

### データの準備

1. 以下のフィールド順でcsv形式のファイルを生成(文字コードutf-8)
    * 特賞フラグ/特賞名/代表者名/荷受No/品名/鉢サイズ/都道府県
    * **1行目はタイトル行**
    * 保存先は static/images/<品評会ディレクトリ>/<品評会ID>.csv

### 画像の準備

1. リサイズ前の画像ファイルをworkディレクトリ以下に準備
2. 以下を実行 

ポットプランツの場合

```shell
python scripts/resize.py --input=work/contest/20200408_PPC春 --output=static/images/128
```

### 投稿

新規投稿

```shell
hugo new contest/999.md
content/contest/999.md created
```

編集

```shell
vi content/contest/999.md
```


## Link

* [Newsroom \| Hugo Themes](https://themes.gohugo.io/newsroom/)
