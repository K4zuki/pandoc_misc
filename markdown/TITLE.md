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
---

# 使用例 {.unnumbered}
`$ this is a code`{.sh}

```cpp
ThisIsAnother(){
  code_block();
}
```
![WaveDrom画像](images/waves/wave.png)

`images/waves/wave.png`{.rotate .caption="任意角度（90度）で回転させたWaveDrom画像" .angle=90}{}

`images/waves/wave.png`{.rotate .caption="任意角度（45度）で回転させたWaveDrom画像" .angle=45}{}

![bit-field画像](images/bitfields/bit.png)

<#include "source.md">

# 必要なもの
## GNU Make

- 全体のコンパイルに必要

### syntax
#### 生成物を消去
`$ make clean`

#### pandoc(HTML出力)
`$ make html`

#### XeLaTeX(PDF出力)
`$ make pdf`

## Python _3_

- データ変換とpandocフィルタに必要
- **やはりPython２は悪い文明！粉砕する！**

### ワンライナーYAML - JSON コンバータ {#yaml2json}
Makefileの中に直接記述

```makefile
PYWAVEOPTS:= -c
PYWAVEOPTS += 'import sys, yaml, json; \
							json.dump(yaml.load(sys.stdin), \
              sys.stdout, indent=4)'

python $(PYWAVEOPTS) < $< > $@
```
### include.py(自作フィルタ)

    `path/to/filename.file`{command}

の書式で各種ファイルをインポート
するためのpandoc前段フィルタ

#### 画像を任意回転して貼り付け

| type            | command            |
|-----------------|--------------------|
| images          | .rotate            |
| `filename.file` | .caption="caption" |
|                 | .angle=\<angle\>   |

変換後の出力：`![ caption ]( filename_r<angle>.file ){ }`

＊例外的に画像リンクのオプション(`width=80%`とか)を使える

#### ソースコードなどをリストとして表にする

\\<extention\\>に合わせたマークアップが施される

| type         | command                        |
|--------------|--------------------------------|
| source codes | .listingtable .\\<extention\\> |

#### ~~CSVファイルをmarkdownのテーブルに変換してコピペ取り込み~~後述のフィルタで置き換え

| type                          | command  |
|-------------------------------|----------|
| pre-converted csv table`.tmd` | .include |

`data/table.csv`{.listingtable .csv}

```markdown

<#include "table.tmd">

```

<!-- `Out/table.tmd`{.include} -->

### pantable

自作フィルタは廃止して[pantable](https://github.com/ickc/pantable)フィルタを使う

- install
    - `pip install pantable`
- syntax
```yaml
---
# yaml front matter
caption: '*Awesome* **Markdown** Table'
alignment: RCDL # Right, Center, Default, Left
table-width: 2/3 # default is 1.0 * page width
markdown: True # inline markdown
include: "data/table.csv" # eternal file
---
```
- csv file
    - see @lst:table_csv
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

## wavedrom

`$ npm --install -g wavedrom-cli`

`$ make wavedrom` → 波形画像をYAMLから[コンバータ](#yaml2json)を通して生成

`data/waves/wave.yaml`{.listingtable .yaml}

```sh
$ python -c
  'import sys, yaml, json; json.dump(yaml.load(sys.stdin),
  sys.stdout, indent=4)' < data/waves/wave.yaml > Out/wave.wavejson
$ phantomjs /Users/yamamoto/.nodebrew/current/bin/wavedrom
  -i Out/wave.wavejson -p images/waves/wave.png
```

## bit-field / librsvg

`$ npm --install -g bit-field`

`$ make bitfield` → レジスタ構成画像をYAMLから[コンバータ](#yaml2json)を通して生成

`$(BITFIELD) --input $< --vspace 80 --hspace 640 --lanes 1 --bits 8 > $<.svg`
`rsvg-convert $<.svg --format=png --output=$@`

`data/bitfields/bit.yaml`{.listingtable .yaml}

## GPP (Generic Preprocessor)

- Ubuntu - `$ apt-get install gpp`{.sh}
    - 日本語でおｋ
- Mac - `$ brew install gpp`{.sh}
    - 日本語でおｋ
- Windows - **日本語ダメ**

# 基本的ディレクトリ構成

```
project root
|-- markdown (markdown原稿)
|   |-- TITLE.md (必ず必要)
|   `-- other.md
`-- data
    |-- bitfields
    |   `-- bit.yaml (bitfield形式)
    |-- waves
    |   `-- wave.yaml (wavedrom形式)
    `-- images
        `-- front-image.png (表紙絵・原稿ファイル内でファイル名を指定できる)
```
