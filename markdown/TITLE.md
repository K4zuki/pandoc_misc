---
title: 本のタイトル
abstract: 本の概要
circle: サークル名
author: 本の作者
date: 本の出版日時
comiket: コミケ
year: 出版年
publisher: 出版社で印刷製本
docrevision: "1.0"
short-hash: (git short hash)
created:

documentclass: book
papersize: b5paper
mainfont: SourceCodePro-Medium
sansfont: SourceCodePro-Medium
monofont: SourceCodePro-Medium
mainlang: Japanese
CJKoptions: BoldFont=RictyDiminished-Bold,
  ItalicFont=RictyDiminished-Oblique,
  BoldItalicFont=RictyDiminished-BoldOblique
CJKmainfont: RictyDiminished-Regular
CJKsansfont: RictyDiminished-Regular
CJKmonofont: RictyDiminished-Regular
geometry: top=30truemm,bottom=30truemm,left=20truemm,right=20truemm
keywords: keyword
secPrefix: Chapter
linkcolor: black
urlcolor: black
citecolor: black
chapter: true
listings: true
codeBlockCaptions: true
listingTitle: 'List'
listingTemplate: '---**$$listingTitle$$ $$i$$$$titleDelim$$ $$t$$**---'

front: images/front-image.png
# include: [markdown, images, data, Out]
---

# 基本的ディレクトリ構成

```
project root
|-- markdown (markdown原稿)
|   |-- TITLE.md (常に必要)
|   `-- other.md
`-- data
    |-- bitfields
    |   `-- bit.yaml (bitfield形式)
    |-- waves
    |   `-- wave.yaml (wavedrom形式)
    `-- images
        `-- front-image.png (表紙絵・原稿ファイル内でファイル名を指定できる)
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

`````markdown
```table
# yaml front matter
caption: '*Awesome* **Markdown** Table'
alignment: RCDL # Right, Center, Default, Left
table-width: 2/3 # default is 1.0 * page width
markdown: True # inline markdown
include: "data/table.csv" # eternal file
---
```
`````
- csv file

`data/table.csv`{.listingtable .csv}

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

### 書式
`````markdown
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
`````
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

<!--
#### 画像を任意回転して貼り付け

| type            | command            |
|-----------------|--------------------|
| images          | .rotate            |
| `filename.file` | .caption="caption" |
|                 | .angle=\\<angle\\> |

```table
---
# yaml front matter
# caption:
alignment: DD
# table-width:
markdown: True # inline markdown
# include:
---
type,command
"images\\
`filename.file`",".rotate\\
.caption=\\'caption\\'\\
.angle=\\<angle\\>"
```

変換後の出力：`![ caption ]( filename_r<angle>.file ){ }`

＊例外的に画像リンクのオプション(`width=80%`とか)を使える
-->

#### ソースコードなどをリストとして表にする

\\<extention\\>に合わせたマークアップが施される

| type         | command                        |
|--------------|--------------------------------|
| source codes | .listingtable .\\<extention\\> |

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

`data/waves/wave.yaml`{.listingtable .yaml}

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

`data/bitfields/bit.yaml`{.listingtable .yaml}

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
C言語などの`#include "stdio.h"`{.c}と同様のことができる。そのままではヘッダ記述を誤解されるので
HTML形式を使用する。

Windowsでの文字コード処理に問題がある（何しても文字化けする）[^1]。

[^1]: Windows7で遭遇。Windows10では未テスト。WSLあるから実質Ubuntuだしね

### インストール

- Ubuntu - `$ apt-get install gpp`{.sh}
    - 日本語ファイル使える
- Mac - `$ brew install gpp`{.sh}
    - 日本語ファイル使える
- Windows - **日本語ファイル化ける**

### syntax

`＜#include "source.md"＞` で外部ファイル読み込み(`-H` オプション)

HTMLのコメントが使えるように`+c "＜!--" "--＞"`オプションを使用

### options

- `gpp -H +c "＜!--" "--＞"`{.sh}
