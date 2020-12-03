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

テーマ設定(submoduleはhttpsプロトコルで追加)

```shell
git submodule add https://github.com/onweru/newsroom.git themes/newsroom
```

(参考)submoduleの削除

```shell
git submodule deinit -f themes/newsroom
git rm themes/newsroom
rm -fr .git/modules
```

サイト設定

```shell
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
# <ortanization>.github.ioの場合はmasterブランチが出力先になるのでソースはsrcブランチで管理するようリネーム
git branch -m src
git push -u origin src
```

Settings>Branches>Default branchでsrc->masterに変更(してもしなくてもよい)

## Github Actionsの利用

* .github/workflows/gh-pages.yamlを作成
    * ソースはsrcブランチ
    * 出力はpublicフォルダの出力をmasterブランチにプル

```shell
make deploy
```

* Github>Settings>Gighub Pages>Source>gh-pages branchに設定する
* 反映するまでしばらく時間がかかる

### データ用のcsvレポジトリの準備

submodule化すると以下のような問題がある

* sshプロトコル接続だとGithub Actionsで認証エラーが出る
* httpsプロトコル接続だとプッシュのたびにユーザ名などを聞いてくる
* その他諸々の問題がある(Detached HEAD 他)
* submodule化しているブランチはsrc-csv-submoduleを参照

csvファイル用レポジトリ追加(事前に準備しておく(submoduleはsshプロトコルで追加)

```shell
git clone git@github.com:toyoake-contest/data.git csv
echo 'csv' >> .gititnore
```

## 既存のレポジトリからクローンする場合

```shell
git clone -b src --recursive git@github.com:toyoake-contest/toyoake-contest.github.io.git
# or
git clone -b src git@github.com:toyoakekaki/toyoake-contest.github.io.git
cd toyoake-contest.github.io
git submodule update --init --recursive
# add csv repository (not submodule)
git clone git@github.com:toyoake-contest/data.git csv
```

## 使い方

### 事前確認情報

* 品評会ID: 対象の品評会のID({{< ref "content/schedule.md" >}}参照)
* 品評会ディレクトリ: 対象の品評会のID
    * ポットプランツの場合は品評会IDと同じ
        * 例) 224
    * 鉢物の場合、東海と全国で品評会IDをハイフン連結
        * 例) 225-226

### データの準備

1. 以下のフィールド順でcsv形式のファイルを生成(**文字コードutf-8**)
    * 特賞フラグ/特賞名/代表者名/荷受No/品名/鉢サイズ/入数/都道府県
    * **1行目はタイトル行**
    * 保存先は static/images/<品評会ディレクトリ>/<品評会ID>.csv

### 画像の準備

1. リサイズ前の画像ファイルをworkディレクトリ以下に準備
2. 以下を実行(outputオプションで指定する品評会ディレクトリは自動生成される)

```shell
python scripts/resize.py --input=<元画像フォルダ> --output=static/images/<品評会ディレクトリ>
```

2017年ポットプランツコンテスト春の部の場合(品評会ID: 206)

```shell
python scripts/resize.py --input=work/contest/20170405_PPC --output=static/images/206
```

東海鉢物品評会2017年観葉植物の部(品評会ID: 207)および鉢物品評会2017年観葉植物の部(品評会ID: 208)の場合(下記例では元画像が同一フォルダに存在する)

```shell
python scripts/resize.py --input=work/contest/20170405_観葉品評会_1 --output=static/images/207-208
```

### 投稿

新規投稿

```shell
hugo new contest/<品評会ID>.md
content/contest/<品評会ID>.md created
```

編集

```shell
vi content/contest/<品評会ID>.md
```

日程の追加

```shell
vi content/schedule.md
```

## 注意事項

Javascriptでリンクの挙動を制御しているので適切なクラスを指定しないと別タブで開く

assets/js/index.js

```js
  (function(){
    let links = document.querySelectorAll('a');
    if(links) {
      Array.from(links).forEach(function(link){
        let target, rel, blank, noopener, attr1, attr2, url, isExternal;
        url = elemAttribute(link, 'href');
        isExternal = (url && typeof url == 'string' && url.startsWith('http')) && !containsClass(link, 'nav_item') && !isChild(link, ['.archive', '.article', '.post_nav', '.pager']) ? true : false;
        if(isExternal) {
          target = 'target';
          rel = 'rel';
          blank = '_blank';
          noopener = 'noopener';
          attr1 = elemAttribute(link, target);
          attr2 = elemAttribute(link, noopener);

          attr1 ? false : elemAttribute(link, target, blank);
          attr2 ? false : elemAttribute(link, rel, noopener);
        }
      });
    }
  })();
```

nav_itemクラスを指定するのがcssでの装飾が特にないので無難

## 独自ドメインの設定

`toyoake-contest.github.io`に`contest.toyoake.or.jp`を割り当てる場合

github

Settings>GitHub Pages>Custome Domain>contest.toyoake.or.jp

bind

```
contest IN      CNAME   toyoake-contest.github.io.
```

## Link

* [Newsroom \| Hugo Themes](https://themes.gohugo.io/newsroom/)
* [Git Submoduleについてまとめてみる \- Qiita](https://qiita.com/BlueSilverCat/items/19bb9b814572cd35b2ae)
