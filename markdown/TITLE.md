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
mainfont: RictyDiminished-Regular
sansfont: RictyDiminished-Regular
monofont: RictyDiminished-Regular
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

# 必要なもの
## GNU Make
`$ make clean` → 生成物を消去

## pandoc(HTML出力)
`$ make html` → HTML出力

### XeLaTeX(PDF出力)
`$ make pdf` → PDF出力

## Python
### yaml - json converter {#yaml2json}
Makefileの中に直接記述

```makefile
PYWAVEOPTS:= -c
PYWAVEOPTS += 'import sys, yaml, json; \
							json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)'

python $(PYWAVEOPTS) < $< > $@
```
### include.py
\` `path/to/filename.file` \` `{command}`

#### rotate image + import

|type|command|
|---|---|
|images|.rotate .caption .angle|

#### code listing as table

|type|command|
|---|---|
|source codes|.listingtable .\<extention\>|

#### csv to table convert

|type|command|
|---|---|
|pre-converted csv table`.tmd`|.include|

`data/table.csv`{.listingtable .csv}

```markdown
`Out/table.tmd`{.include}
```
## wavedrom
`$ npm --install -g wavedrom-cli`

`$ make wavedrom` → 波形画像をYAMLから[コンバータ](#yaml2json)を通して生成

`data/waves/wave.yaml`{.listingtable .yaml}

```sh
$ python -c 'import sys, yaml, json; json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)' < data/waves/wave.yaml > Out/wave.wavejson
$ phantomjs /Users/yamamoto/.nodebrew/current/bin/wavedrom -i Out/wave.wavejson -p images/waves/wave.png
```

## bit-field / librsvg
`$ npm --install -g bit-field`

`$ make bitfield` → レジスタ構成画像をYAMLから[コンバータ](#yaml2json)を通して生成

```
$(BITFIELD) --input $< --vspace 80 --hspace 640 --lanes 1 --bits 8 > $<.svg
rsvg-convert $<.svg --format=png --output=$@
```
`data/bitfields/bit.yaml`{.listingtable .yaml}
