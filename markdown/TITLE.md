# まえがき {.unnumbered}
このドキュメントは、筆者が本を書くために構築したオレオレMarkdown-PDF変換環境
を解説するための本です。^[このドキュメント自身もその環境で出力されました。よくあることですね]

OSはUNIXを前提にします。具体的に言うとMac、Ubuntuなら16.04LTSです。
Windows10とWSLなUbuntu^[ぐぐってね]ならUbuntu16.04のやり方が
うまくいくかもしれませんが、Win10機を持ってないので
あまり良いアドバイスができません。ごめんなさい。

# 背景というか、どうやって変換するの？
最終的にはシンプル３ステップで出力されます

1. Markdownで原稿を書きます
1. コンパイルします
1. PDFが出力されます

Markdownコンパイラは**Pandoc**^[マニュアルを日本語化している有志の方がいますね]と各種フィルタを使います。
各種フィルタはあちこちから都合のいいものをかき集めてるので**_使用言語がバラバラです_**。
Homebrewあるいはaptでインストールすれば比較的楽ちんなので気にせずに構築してきましたが、
Windowsはこのあたりが非常にめんどいのでMacまたはUbuntuの使用をおすすめします。
プロいひとはDockerイメージとかCIとかでもっと楽にできるかもしれません。

# 環境構築する
やることはいっぱいあります。~~やっぱりDockerイメージ欲しいな()~~

## インストールそしてインストールそれからインストール
インストールしまくります。

### パッケージ管理ツールのインストール

#### Homebrew(Mac)
https://brew.sh/index_ja.html

全てに先んじてHomebrewのインストールをします。
```sh
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Ubuntuユーザはaptがほぼ全てやってくれるので特別にインストールするものはありません

### 言語のインストール
主に４言語使います - **Haskell・Python・NodeJS・LaTeXです**^[_もううんざりしてきた？_]。
HaskellはPandocとpandoc-crossrefフィルタのインストールで必要です。NodeJSはフィルタと画像生成、
Pythonはフィルタとシェルスクリプトの代わり、そしてLaTeXはPDF出力のためです。

#### Mac {.unnumbered}
```sh
$ brew install cabal-install
$ brew install python3
$ brew install nodebrew
$ nodebrew use v6.5.0
$ brew cask install mactex
```

#### Ubuntu {.unnumbered}
```sh
$ sudo apt-get install python3 python3-pip
$ sudo apt-get install nodejs-legacy npm
$ sudo apt-get install texlive-xetex
```

[https://texwiki.texjp.org/?TeX%20Live]

### 各言語のパッケージのインストール
#### Mac {.unnumbered}
```sh
$ cabal install pandoc-crossref
$ pip3 install pyyaml pillow
$ pip3 install pantable csv2table
$ pip3 install six pandoc-imagine
$ npm install -g phantomjs-prebuilt bit-field wavedrom-cli
```
pandoc-crossrefがpandocに依存しているので自動的にインストールされます。

##### Ubuntu {.unnumbered}
aptで入るpandocは1.16でだいぶ古いのでpandocのGitHubサイト^[https://github.com/jgm/pandoc/releases]
からdebファイルを落としてきます
```sh
$ wget -C https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb
$ sudo dpkg -i pandoc-1.19.2.1-1-amd64.deb
$ sudo -H pip3 install pyyaml pillow
$ sudo -H pip3 install pantable csv2table
$ sudo -H pip3 install six pandoc-imagine
$ sudo npm install -g phantomjs-prebuilt bit-field wavedrom-cli
$ sudo apt-get install xzdec texlive-lang-japanese
$ tlmgr init-usertree
$ tlmgr option repository ftp://tug.org/historic/systems/texlive/2015/tlnet-final
$ wget -c https://github.com/zr-tex8r/BXptool/archive/v0.4.zip
$ unzip v0.4.zip
$ sudo mkdir -p /usr/share/texlive/texmf-dist/tex/latex/BXptool/
$ sudo cp BXptool-0.4/bx*.{sty,def} /usr/share/texlive/texmf-dist/tex/latex/BXptool/
$ sudo mktexlsr
```
<!--
#### TeXLive
https://github.com/zr-tex8r/BXptool
```sh
$ sudo apt-get install xzdec texlive-lang-japanese
$ tlmgr init-usertree
$ tlmgr option repository ftp://tug.org/historic/systems/texlive/2015/tlnet-final
$ wget -c https://github.com/zr-tex8r/BXptool/archive/v0.4.zip
$ unzip v0.4.zip
$ sudo mkdir -p /usr/share/texlive/texmf-dist/tex/latex/BXptool/
$ sudo cp BXptool-0.4/bx*.{sty,def} /usr/share/texlive/texmf-dist/tex/latex/BXptool/
$ sudo mktexlsr
```
 -->
### ツールのインストール
#### Mac {.unnumbered}
```sh
$ brew install librsvg gpp plantuml
```
#### Ubuntu {.unnumbered}
```sh
$ sudo apt-get install librsvg2-bin gpp
```
### フォントのインストール
#### Mac {.unnumbered}
#### Ubuntu {.unnumbered}
#### Source Code Pro
#### Source Sans Pro
#### Ricty Diminished

## ダウンロード
### pandoc_misc
この本の原稿が置かれたリポジトリです。`$(HOME)/.pandoc`にクローンします。
```sh
$ cd ~/.pandoc
$ git clone https://github.com/K4zuki/pandoc_misc.git
$ git submodule update --init
```

# 本を書く
## 原稿リポジトリの準備
新規に原稿管理用Gitリポジトリを作りましょう。たとえば
ホームディレクトリ直下のworkspaceディレクトリにMyBookというGitリポジトリを作ります。
```sh
$ mkdir -p ~/workspace/MyBook
$ cd workspace/MyBook
$ git init
```
ここでpandoc_miscディレクトリに戻り、原稿リポジトリにコンパイル環境をコピーします
```sh
$ cd ~/.pandoc/pandoc_misc
$ make init PREFIX=~/workspace/MyBook
```
初期状態では以下のようなディレクトリ構成のはずです
```
~/workspace/MyBook
|-- Makefile
|-- Out/
|-- images/
|-- markdown/
|   |-- TITLE.md
|   `-- config.yaml
`-- data/
    |-- bitfields/
    |-- bitfield16/
    `-- waves/
```

## 原稿リポジトリの調整
原稿のファイル名・置き場所・ディレクトリ構成は自由に配置してください。

### ファイル名・ディレクトリ名の設定(Makefile)
タイトルファイル名、ディレクトリ名を変更した場合は、そのことをコンパイラに知らせる必要があります。
コンパイラはタイトルページのファイル名と各種ディレクトリ名をMakefileから取得します。
ディレクトリ名はすべてMakefileが置かれたディレクトリからの相対パスです。

```table
---
caption: Makeコンパイルオプション
width:
  - 0.15
  - 0.2
  - 0.55
  - 0.1
header: True
---
変数名,種類,意味,初期値
CONFIG,ファイル,pandocのコンフィグファイル,config.yaml
INPUT,ファイル,タイトルファイル,TITLE.md
TARGET,ファイル,出力ファイル,TARGET
MDDIR,ディレクトリ,タイトルファイルの置き場所,markdown/
DATADIR,ディレクトリ,データディレクトリ,data/
TARGETDIR,ディレクトリ,出力先ディレクトリ,Out/
IMAGEDIR,ディレクトリ,画像ファイルの置き場所,images/
WAVEDIR,ディレクトリ,WaveDromファイルの置き場所,waves/
BITDIR,ディレクトリ,８ビット幅Bitfieldファイルの置き場所,bitfields/
BIT16DIR,ディレクトリ,１６ビット幅Bitfieldファイルの置き場所,bitfield16/
```

### Pandocオプションの設定(config.yaml)
Pandocはmarkdownファイル内のYAML FrontMatterもしくは独立したYAMLファイルから
コンパイルオプションを取得します。
```table
---
caption: Pandocコンパイルオプション
header: True
markdown: True
width:
  - 0.2
  - 0.5
  - 0.3
---
パラメータ,意味,初期値
title,タイトル,本のタイトル
abstract,サブタイトル,本の概要
circle,サークル名,サークル名
author,作者の名前,本の作者
comiket,イベント名,コミケ
year,発行年,出版年
publisher,印刷所,出版社で印刷製本
docrevision,リビジョン番号,1.0
front,表紙画像ファイル名,images/front-image.png
```

## 原稿を書く
いわゆる普通のPandoc式Markdown記法に則って書いていきます。
デフォルトの`config.yaml`では章番号がつく設定で、例外的に消すこともできます。
例外が適用できるのは深さ４までの章番号に限られ、深さ５より深いものは_無条件に_ナンバリングされます。
```markdown
# 1 {.unnumbered} <!--章番号なし-->
## 2 {.unnumbered} <!--章番号なし-->
### 3 {.unnumbered} <!--章番号なし-->
#### 4 {.unnumbered} <!--章番号なし-->
##### 5 {.unnumbered} <!--章番号復活-->
```

### 原稿を連結する
### 表を書く・引用する
### ソースコードを引用する
### ビットフィールド画像を描く
### ロジック波形を書く
## コンパイルする
`Makefile`/`config.yaml`と原稿一式をリポジトリに登録して最初のコミットをします。
```sh
$ git add Makefile
$ git commit -m"initial commit"
```
この状態でmake htmlとするとOut/TARGET.htmlというファイルができあがるはずです。

# 必要なもの
## pandoc
汎用Markdownコンバータ

### インストール
- Mac
```sh
$ brew install pandoc pandoc-crossref
```
- Ubuntu
    - aptで入るのは1.16でだいぶ古いのでpandocのGitHubサイトからdebファイルを落としてくる
```sh
$ wget -C https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb
$ dpkg -i pandoc-1.19.2.1-1-amd64.deb
```

## GNU Make
全体のコンパイルに必要

### syntax
#### 生成物を消去
`$ make clean`{.sh}

#### pandoc(HTML出力)
`$ make html`{.sh}

#### pandoc + XeLaTeX(PDF出力)
`$ make pdf`{.sh}

## Python _3_

- データ変換とpandocフィルタに必要
- **やはりPython２は悪い文明！粉砕する！**

### インストール
- Mac
    - `$ brew install python3`{.sh}
- Linux
    - `$ sudo apt-get install python3 python3-pip`{.sh}
        - このpip3はパーミッションエラーを引き起こすようなのでアップグレードするべきではない
        - もしくはプレフィックス付きでアップデートしなければならない（けどやり方は知らない）

### ワンライナーYAML - JSON コンバータ {#yaml2json}

~~一部~~殆どのJSライブラリが _当然のように_ JSONを利用するが、JSONはバイナリでもないのに
人間に読めない形式なのでYAMLでデータを作り、それをワンライナーでJSONに変換する前処理をして、
それらのライブラリに渡す。みんなしあわせ

- `$ pip3 install pyyaml`{.sh}

Makefileの中に直接記述

```makefile
PYWAVEOPTS:= -c
PYWAVEOPTS += 'import sys, yaml, json; \
							json.dump(yaml.load(sys.stdin), \
              sys.stdout, indent=4)'

python3 $(PYWAVEOPTS) < $< > $@
```

### pantable
CSVファイルをpandocのgrid tableに変換して取り込む。以前は自作スクリプトを使用していたが廃止。

<https://github.com/ickc/pantable>

#### インストール
```sh
$ pip3 install pantable
```

#### 書式
`table`クラスのコードブロック内にYAMLヘッダを記述する。外部ファイルをインポートすることも直書きもできる。

~~~~~markdown
```table
---
# yaml front matter
caption: '*Awesome* **Markdown** Table'
alignment: RCDL # Right, Center, Default, Left
table-width: 2/3 # default is 1.0 * page width
markdown: True # inline markdown
include: "data/table.csv" # eternal file
---
```
~~~~~
- csv file

```listingtable
source: data/table.csv
class: csv
tex: True
---
```

- result
```table
---
# yaml front matter
caption: '*Awesome* **Markdown** Table'
alignment: RCDL
table-width: 2/3
markdown: True
include: "data/table.csv"
---
```

### rotateimg.py(自作フィルタ)
`pantable`と同様の書式で画像を任意角度で回転する。
内部でPillowライブラリを利用している。

#### インストール
```sh
$ pip3 install pillow
```

#### 書式
~~~~~markdown
```rotate
source: images/waves/wave.png
angle: 45
# title: 'Alt title'
caption: 任意角度（45度）で回転させたWaveDrom画像
attr:
#  width: 20%
#  height: 50%
---
```
~~~~~
```rotate
source: images/waves/wave.png
angle: 45
# title: 'Alt title'
caption: 任意角度（45度）で回転させたWaveDrom画像
attr:
#  width: 20%
#  height: 50%
---
```

### include.py(自作フィルタ)

    `path/to/filename.file`{command}

の書式で各種ファイルをインポートするためのpandoc前段フィルタ。

#### ソースコードなどをリストとして表にする

`<extention>`に合わせたマークアップが施される

| type         | command                        |
|--------------|--------------------------------|
| source codes | `.listingtable .<extention>` |

## Node.js と npm

更新頻度高すぎ\&\&ワケワカラン過ぎてあんまり好きじゃない。
偶数バージョンがLTSらしいので当面Macは**6系**を使用。Ubuntu16.04は**4系**のLTSが入る

`npm install`は`-g`なしだと現在のディレクトリにインストールしちゃうオモシロ仕様なのでつけるのを忘れずに

### インストール
- Mac
```sh
$ brew install nodebrew
$ nodebrew use v6.5.0
~/.nodebrew/current/bin/{node,npm}
```
- Ubuntu
```sh
$ sudo apt-get install nodejs-legacy npm
```

### wavedrom
#### インストール

- Mac
```sh
$ npm install -g wavedrom-cli
```
- Ubuntu
```sh
$ sudo npm install -g wavedrom-cli
```
#### 使用例
`$ make wavedrom` → 波形画像をYAMLから[コンバータ](#yaml2json)を通して生成

```listingtable
source: data/waves/wave.yaml
class: yaml
tex: True
---
```

```sh
$ python -c \\
  'import sys, yaml, json; json.dump(yaml.load(sys.stdin),
  sys.stdout, indent=4)' < data/waves/wave.yaml > Out/wave.wavejson
$ phantomjs /Users/yamamoto/.nodebrew/current/bin/wavedrom \\
  -i Out/wave.wavejson -p images/waves/wave.png
```

### bit-field / librsvg
#### インストール

- bit-field
    - `$ npm install -g bit-field`{.sh}
    - `$ sudo npm install -g bit-field`{.sh}

- librsvg
  - Mac
```sh
$ brew install librsvg
```
  - Ubuntu
```sh
$ sudo apt-get install librsvg2-bin
```

#### 使用例

`$ make bitfield` → レジスタ構成画像をYAMLから[コンバータ](#yaml2json)を通して生成

```makefile
$(BITFIELD) --input $< --vspace 80 --hspace 640 --lanes 1 --bits 8 > $<.svg
rsvg-convert $<.svg --format=png --output=$@
```

```listingtable
source: data/bitfields/bit.yaml
class: yaml
tex: True
---
```


### mermaid-filter
<https://github.com/raghur/mermaid-filter>

#### インストール

- `$ npm install -g mermaid raghur/mermaid-filter`
- `$ sudo npm install -g mermaid raghur/mermaid-filter`

#### syntax
```markdown
~~~{.mermaid loc=images}
sequenceDiagram
    Alice->>John: Hello John, how are you?
    John-->>Alice: Great!
~~~
```
#### オプション(リポジトリREADMEより)

> You have a couple of formatting options via attributes of the fenced code block to control the rendering
>
> - Image Format - Use ```{.mermaid format=svg} Default is png
> - Width - Use ```{.mermaid width=400} default with is 500
> - Save path - Use ```{.mermaid loc=img} default loc=inline which will encode the image in a data uri scheme.
>     - Possible values for loc
>         - loc=inline - default; encode image to data uri on img tag.
>             - For widest compatibility, use png (default)
>             - SVG has trouble on IE11
>         - loc=imgur - upload png to imgur and link to it.
>         - loc=\\<anythingelse\\> - treat as folder name to place images into

## GPP (Generic Preprocessor) 汎用プリプロセッサ
C言語などの`＃include "stdio.h"`{.c}と同様のことができる。そのままではヘッダ記述を誤解されるので
HTML形式を使用する。

### インストール

- Ubuntu - `$ apt-get install gpp`{.sh}
    - 日本語ファイル使える
- Mac - `$ brew install gpp`{.sh}
    - 日本語ファイル使える
- Windows - https://github.com/makc/gpp.2.24-windows からコンパイル済バイナリを入手
    - 日本語ファイル使える

### syntax

`＜＃include "source.md"＞` で外部ファイル読み込み(`-H` オプション)

HTMLのコメントが使えるように`+c "＜!--" "--＞"`オプションを使用

### options

```sh
gpp -H +c "＜!--" "--＞"
```

# 使用例 {.unnumbered}
`$ this is a code`{.sh}

```cpp
ThisIsAnother(){
  code_block();
}
```
![WaveDrom画像](images/waves/wave.png)

<!-- `images/waves/wave.png`{.rotate .caption="任意角度（90度）で回転させたWaveDrom画像" .angle=90}{} -->
```rotate
source: images/waves/wave.png
angle: 90
# title: 'Alt title'
caption: 任意角度（90度）で回転させたWaveDrom画像
---
```
```rotate
source: images/waves/wave.png
angle: 45
# title: 'Alt title'
caption: 任意角度（45度）で回転させたWaveDrom画像
---
```

![bit-field画像](images/bitfields/bit.png)

<#include "source.md">
