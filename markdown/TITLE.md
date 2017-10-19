# まえがき {.unnumbered}
このドキュメントは、筆者が本を書くために構築したオレオレMarkdown-PDF変換環境
を解説するための本です。^[このドキュメント自身もその環境で出力されました。よくあることですね]

筆者が以前使っていたGitBookでは表の扱いなどに制限があり不満があったので、「なければ作る」の原則に従ってみました。

使用OSはUNIXを前提にします。具体的に言うとMac、LinuxならUbuntu16.04LTSです。
Windows10とWSLなUbuntuならUbuntu16.04のやり方がうまくいくと思います[^creators]。
Win10機は持っているのですが、当該機がとっても遅い[^i5-2500k]
ので検証が進まず、あまり良いアドバイスができません。ごめんなさい。

## 背景というか {-}
2x歳になってはじめてコミケにサークル参加してみた。本を書かねばならなくなった（？）。ネタはあった。

楽な開発（？）方法をネットで探したらGitBookというのが良さそうだった^[ここで初めてMarkdownを使いだした]。

GitBookはまあまあ使えたけど、本体が開発途上かつよくわからん言語での開発だったので開発者に問題を報告したりができず、
結果的に細かいことができなかった。しょうがないので乗り換え先を探していったらPandocが見つかった。神だった（？）

Pandoc=ｻﾝはたしかに神だったけどオプションも大量にあったので何かで管理しなければならなかった。
そこでみんな大好き^[個人の意見です]GNU Makeを使うことにした。

## 何が変換されて何が出力されるの？ {.unnumbered}
Markdown原稿がGNU Make x Pandocという*グレイトな*アプリケーションの*ファンタスティックな*コンビネーションによって
*HTML*、*TeX*または/および*PDF*に変換されます。

書き手の作業を要約するとこうです：

1. Markdownで原稿を書きます
1. コンパイルします
1. PDFが出力されます

コンパイルの制御にはGNU Makeを使います。コンパイルの前処理としてGPPによる原稿の連結を行い[^gpp]、
各種YAMLデータから画像もしくは表を生成し[^pandable][^pandoc-imagine][^wavedrom][^bitfield]、
最後にMarkdownをPDFもしくはHTMLに出力します[^pandoc][^make-html][^make-pdf]。

[^creators]: Creators Updateの適用が必要です。2017年のFall Creators Updateで正式な機能になったっぽい・なるっぽいです。
[^i5-2500k]: i5-2500Kかつメインディスクが2.5インチHDDでして
[^gpp]: @sec:gpp を参照
[^pandable]: @sec:pantable を参照
[^pandoc-imagine]: @sec:pandoc-imagine を参照
[^wavedrom]: @sec:wavedrom を参照
[^bitfield]: @sec:bitfield を参照
[^pandoc]: @sec:pandoc を参照
[^make-html]: `make html`を実行
[^make-pdf]: `make pdf`を実行

Markdownコンパイラは**Pandoc**^[マニュアルを日本語化している有志の方がいますね]と各種フィルタを使います。
各種フィルタはあちこちから都合のいいものをかき集めてるので**_使用言語がバラバラです_**。
Homebrewあるいはaptでインストールすれば _比較的_ 楽ちんなので筆者は気にせずに構築してきましたが、
Windowsはこのあたりが非常にめんどいのでMacまたはUbuntuの使用をおすすめします。
プロいひとはDockerイメージとかCIとかでもっと楽にできるかもしれません。

# 環境構築する
やることはいっぱいあります。~~やっぱりDockerイメージ欲しいな()~~

## インストールそしてインストールそれからインストール
インストールしまくります。

### パッケージ管理ツールのインストール
#### Homebrew(Mac) - https://brew.sh/index_ja.html

全てに先んじてHomebrewのインストールをします。
```sh
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Ubuntuユーザはaptがほぼ全てやってくれるので特別にインストールするものはありません

### 言語のインストール
主に４言語使います - **Haskell・Python _３_・NodeJS・LaTeXです**。
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

参考サイト： https://texwiki.texjp.org

### 各言語のパッケージのインストール
#### Mac {.unnumbered}
```sh
$ cabal install pandoc-crossref
$ pip3 install pyyaml pillow
$ pip3 install pantable csv2table
$ pip3 install six pandoc-imagine
$ pip3 install six svgutils
$ npm install -g phantomjs-prebuilt bit-field wavedrom-cli
```
pandoc-crossrefがpandocに依存しているので自動的にインストールされます。

#### Ubuntu {.unnumbered}
aptで入るpandocは1.16でだいぶ古いのでpandocのGitHubサイト^[https://github.com/jgm/pandoc/releases]
からdebファイルを落としてきます
```sh
$ wget -c https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb
$ sudo dpkg -i pandoc-1.19.2.1-1-amd64.deb
$ sudo -H pip3 install pyyaml pillow
$ sudo -H pip3 install pantable csv2table
$ sudo -H pip3 install six pandoc-imagine
$ sudo -H pip3 install svgutils
$ sudo npm install -g phantomjs-prebuilt wavedrom-cli
$ sudo npm install -g fs-extra yargs onml bit-field
$ sudo apt-get install xzdec texlive-lang-japanese
$ tlmgr init-usertree
$ tlmgr option repository ftp://tug.org/historic/systems/texlive/2015/tlnet-final
$ wget -c https://github.com/zr-tex8r/BXptool/archive/v0.4.zip
$ unzip v0.4.zip
$ sudo mkdir -p /usr/share/texlive/texmf-dist/tex/latex/BXptool/
$ sudo cp BXptool-0.4/bx*.{sty,def} /usr/share/texlive/texmf-dist/tex/latex/BXptool/
$ sudo mktexlsr
$ tlmgr install oberdiek
```
### ツールのインストール
#### Mac {.unnumbered}
```sh
$ brew install librsvg gpp plantuml wget
```
#### Ubuntu {.unnumbered}
```sh
$ sudo apt-get install librsvg2-bin gpp
$ sudo apt-get install graphviz plantuml
```
### フォントのインストール
各リポジトリからアーカイブをダウンロード・解凍してTTFファイル(TrueTypeフォント)を全部、
ユーザフォントディレクトリにコピーします。
```sh
mkdir -p $HOME/.local/share/fonts/
cd $HOME/.local/share/fonts/
wget -c https://github.com/adobe-fonts/source-code-pro/archive/2.030R-ro/1.050R-it.zip
wget -c https://github.com/adobe-fonts/source-sans-pro/archive/2.020R-ro/1.075R-it.zip
wget -c https://github.com/mzyy94/RictyDiminished-for-Powerline/archive/3.2.4-powerline-early-2016.zip
```

## ダウンロード
### pandoc_misc
この本の原稿が置かれたリポジトリです。`$(HOME)/.pandoc`にクローンします。
```sh
$ cd ~/.pandoc
$ git clone https://github.com/K4zuki/pandoc_misc.git
$ git submodule update --init
$ cd bitfield
$ npm install
```

# 本を書く
## 原稿リポジトリの準備
新規に原稿管理用Gitリポジトリを作りましょう。たとえば
ホームディレクトリ直下のworkspaceディレクトリにMyBookというGitリポジトリを作ります。
```sh
$ mkdir -p ~/workspace/MyBook
$ cd ~/workspace/MyBook
$ git init
```
ここでpandoc_miscディレクトリに戻り、原稿リポジトリにコンパイル環境をコピーします。
```sh
$ cd ~/.pandoc/pandoc_misc
$ make init PREFIX=~/workspace/MyBook
```
初期状態では以下のようなディレクトリ構成のはずです。
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
原稿のファイル名・置き場所・ディレクトリ構成は自由に配置してください。日本語ファイル名は
問題ないと思います^[推奨しません]が、スペースを入れるのは避けるべきです。

#### ファイル名・ディレクトリ名の設定(Makefile) {.unnumbered}
タイトルファイル名、ディレクトリ名を変更した場合は、そのことをビルドスクリプトに知らせる必要があります。
ビルドスクリプトはタイトルページのファイル名と各種ディレクトリ名をMakefileから取得します。
ディレクトリ名はすべてMakefileが置かれたディレクトリからの相対パスです。

```table
---
caption: Makeコンパイルオプション
width:
  - 0.15
  - 0.2
  - 0.50
  - 0.15
header: True
markdown: True
---
変数名,種類,意味,初期値
`CONFIG`,ファイル,pandocのコンフィグファイル,`config.yaml`
`INPUT`,ファイル,タイトルファイル,`TITLE.md`
`TARGET`,ファイル,出力ファイル,`TARGET`
`MDDIR`,ディレクトリ,タイトルファイルの置き場所,`markdown/`
`DATADIR`,ディレクトリ,データディレクトリ,`data/`
`TARGETDIR`,ディレクトリ,出力先ディレクトリ,`Out/`
`IMAGEDIR`,ディレクトリ,画像ファイルの置き場所,`images/`
`WAVEDIR`,ディレクトリ,WaveDromファイルの置き場所,`waves/`
`BITDIR`,ディレクトリ,8ビット幅Bitfieldファイルの置き場所,`bitfields/`
`BIT16DIR`,ディレクトリ,16ビット幅Bitfieldファイルの置き場所,`bitfield16/`
```

\\newpage
#### Pandocオプションの設定(config.yaml) {.unnumbered}
Pandocはmarkdownファイル内のYAML FrontMatterもしくは独立したYAMLファイルから
コンパイルオプションを取得します。これらの値は表紙絵と奥付に使用されます
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
`title`,タイトル,本のタイトル
`abstract`,サブタイトル,本の概要
`circle`,サークル名,サークル名
`author`,作者の名前,本の作者
`comiket`,イベント名,コミケ
`year`,発行年,出版年
`publisher`,印刷所,出版社で印刷製本
`docrevision`,リビジョン番号,1.0
`front`,表紙画像ファイル名,images/front-image.png
```

\\newpage
## 原稿リポジトリをコンパイル
ここでいったんコンパイルできるかどうか試してみましょう。`TITLE.md`の中身が空でも
コンパイルすることはできます。コンパイルする前に`Makefile`/`config.yaml`と
原稿一式をリポジトリに登録して最初のコミットをします。
```sh
$ git add .
$ git commit -m"initial commit"
```
この状態で`make html`とすると`Out/TARGET.html`というファイルができあがるはずです。
以下に代表的なコマンドの一覧を載せます。

`````table
---
caption: コンパイル方法
markdown: True
width:
  - 0.2
  - 0.3
  - 0.5
---
コマンド,効果,成果物
`make html`,HTMLファイル生成,`$(TARGETDIR)/$(TARGET).html`
`make pdf`,PDFファイル生成,`$(TARGETDIR)/$(TARGET).pdf`
`make clean`,成果物を全部消去,"`rm -rf $(TARGETDIR)/*`\\
`rm -rf $(IMAGEDIR)/$(WAVEDIR)/`\\
`rm -rf $(IMAGEDIR)/$(BITDIR)/`\\
`rm -rf $(IMAGEDIR)/$(BIT16DIR)/`
"
`````
`make pdf` を使うとXeLaTeXを使ってPDFに出力します。表紙、目次、本文、奥付けが体裁されたPDFができあがるはずです。

## 原稿を書く {#sec:pandoc}
これでとりあえずコンパイルが通るようになったので、実際の原稿を書けるようになりました。
**~~デファクトスタンダードこと~~**Pandoc式Markdown記法に則って書いていきます。

### ヘッダの書き方
デフォルトの`config.yaml`では章番号がつく設定で、例外的に消すこともできます。
例外が適用できるのは深さ４までの章番号に限られ、深さ５より深いものは _強制的に_ ナンバリングされます。
_**バグっぽいんだけどどうなんですかね**_。そこまで深く章分けする人あまりいないんですかね。

Listing: 章番号は深さ5以上で強制される

```{.markdown #lst:section-numbering}
# 深さ1：章番号なし {.unnumbered}
## 深さ2：章番号なし {.unnumbered}
### 深さ3：章番号なし {.unnumbered}
#### 深さ4：章番号なし {.unnumbered}
##### 深さ5+：章番号復活 {.unnumbered}
```

### 原稿を連結する {#sec:gpp}
原稿の連結にはGeneric Preprocessor^[https://github.com/logological/gpp]を使います。
C言語で`＃include "stdio.h"`などと記述するアレです。
C言語風そのままだとヘッダと間違われるのでHTML風に&lt;`＃include "ファイル名"`&gt;
と記述します。該当部分は指定されたファイルに
置き換えられます(入れ子になっていても機能します)。

\\newpage
### 表を書く・引用する {#sec:pantable}
表の引用とレンダリングにはpantableフィルタ^[https://github.com/ickc/pantable]を使います。
コードブロックに直接CSVを書くか、`include: ファイル名`でファイル名を指定します。
タイトルの有無やCSVセルの内容をMarkdownとして解釈するかどうか
を選択するオプションがあります。１セルが複数行に渡る表も書けます。
`include`でファイルを指定しているときは直接記述部分は無視されます。
```table
---
caption: pantableフィルタオプション（抜粋）
markdown: True
alignment: CCCD
width:
  - 0.15
  - 0.15
  - 0.20
  - 0.5
---
オプション,省略可能,デフォルト値,意味
`caption`,Y,,表のタイトル。Markdown記法が使える
`include`,Y,,CSVファイル名
`markdown`,Y,False,セルの内容をMarkdownとして解釈するフラグ
`alignment`,Y,,列ごとの右揃え(R)/左揃え(L)/中央揃え(C)/デフォルト(D)の指定
`table-width`,Y,1.0,表全体の幅 ページ幅に対する比率で指定する(ページ幅いっぱいが1.0)
`width`,Y,,列ごとの幅
```

#### 記述例 {.unnumbered}
~~~~~markdown
```table
---
caption: '*Awesome* **Markdown** Table'
alignment: RCDL # Right, Center, Default, Left
table-width: 0.8 # default is 1.0 * page width
markdown: True # inline markdown
include: "data/table.csv" # external file
width:
  - 0.1
  - 0.2
  - 0.2
  - 0.3
---
```
~~~~~

\\newpage
#### CSVファイルの中身 {.unnumbered}
```listingtable
source: data/table.csv
class: csv
tex: True
---
```

#### 変換結果 {.unnumbered}
```table
---
caption: '*Awesome* **Markdown** Table'
alignment: RCDL
table-width: 0.8
markdown: True
include: "data/table.csv"
width:
  - 0.1
  - 0.2
  - 0.2
  - 0.3
---
```

\\newpage
### ソースコードを引用する {#sec:listingtable}
ソースコードの引用とレンダリングにはPythonで組んだ自作フィルタ^[pandoc_misc/panflute/ListingTable.py]
を使います。生成物は自動的にナンバリングされます(`pandoc-crossref`[^pandoc-crossref][^pandoc-creooref-ref]
との組み合わせ運用を前提にしています)。

[^pandoc-crossref]: https://github.com/lierdakil/pandoc-crossref
[^pandoc-crossref-ref]: http://d.hatena.ne.jp/LaclefYoshi/20150616/crossref

```table
---
caption: ListingTableフィルタオプション
markdown: True
alignment: DCCD
---
オプション,省略可能,デフォルト値,意味
source,N,,ソースファイル名(フルパス)
class,N,,"ソースファイル種類(python,cpp,markdown etc.)"
tex,Y,False,LaTeXを出力するとき"True"にする。case sensitive
```

`````markdown
```listingtable
source: data/table.csv
class: csv
tex: True
---
```
`````

\\newpage
### ビットフィールド画像を描く・挿入する {#sec:bitfield}
bitfield^[https://github.com/drom/bitfield]はあまり知られていませんがJSONファイルを
レジスタマップ風SVGに描画するJSライブラリです。

Pandocフィルタを2種類用意しました。pantable同様のブロック形式と
画像リンクにソースファイル名を指定するインライン形式で本文中に挿入できます。
形式ごとにオプションが若干違います。

ソースコードはJSONまたはYAML形式が使えます。コードブロック直接記述もファイル指定も可能です。
YAML形式は内部でJSONへの変換を試みます。pantableフィルタと同様にソースコードを
指定すると直接記述は無視されます。指定されたソースコードが見つからないときはエラーが出ます。

出力形式はPNG/PDF/EPSが指定できますが、pandocの出力ファイル形式(`-f`オプション)によって
ある程度自動判定されます。出力形式にhtmlが指定されていると暗黙にSVGをリンクします。
同様にlatexが指定されているとPDF画像をリンクします。中間ファイルはデフォルトで`svg`ディレクトリに
保存されます。

```table
---
caption: BitFieldフィルタオプション
markdown: True
width:
  - 0.20
  - 0.20
  - 0.20
  - 0.40
alignment: DCCD
---
オプション,省略可能,デフォルト値,意味
`input`,N,,ソースファイル名
`png`,Y,**True**,PNG出力フラグ
`eps`,Y,False,EPS出力フラグ
`pdf`,Y,False,PDF出力フラグ
`lane-height`,Y,80,レーンあたりの高さ
`lane-width`,Y,640,レーンの幅
`lanes`,Y,1,レーンの数
`bits`,Y,8,総ビット数
`fontfamily`,Y,"source code pro",フォントファミリ名
`fontsize`,Y,16,フォントサイズ
`fontweight`,Y,normal,フォントのウェイト
`caption`,Y,Untitled(*),タイトル
`directory`,Y,"`./svg`",出力ディレクトリ
`attr`,Y,,画像幅などの指定
```
(*) インライン形式のときはタイトルなしにできる
\\newpage

#### 記述例 - ブロック形式
~~~~~markdown
```bitfield
# input: data/bitfields/bit.yaml
caption: _**block bitfield sample**_
---
# list from LSB
# bits: bit width
# attr: information RO/WO/RW etc.
# name: name of bitfield
- bits: 5
- bits: 1
  attr: RW
  name: IPO
- bits: 1
  attr: RW
  name: BRK
- bits: 1
  name: CPK
```
~~~~~

#### インライン形式 {.unnumbered}
```markdown
![**inline bitfield sample**](data/bitfields/bit.yaml){.bitfield}
```

#### 変換結果 - ブロック形式
```bitfield
# input: data/bitfields/bit.yaml
caption: _**block bitfield sample**_
---
# list from LSB
# bits: bit width
# attr: information RO/WO/RW etc.
# name: name of bitfield
- bits: 5
- bits: 1
  attr: RW
  name: IPO
- bits: 1
  attr: RW
  name: BRK
- bits: 1
  name: CPK
```
#### インライン形式 {.unnumbered}
![**inline bitfield sample**](data/bitfields/bit.yaml){.bitfield}

\\newpage
### WaveDromロジック波形を描く・挿入する {#sec:wavedrom}

WaveDrom^[`http://wavedrom.com`] は、ロジック波形を記述ためのJSライブラリです。
@sec:bitfield と同様のインライン形式で本文に挿入できます。

~~~markdown
![inline wavedrom sample](data/waves/wave.yaml){.wavedrom}
~~~
![inline wavedrom sample](data/waves/wave.yaml){.wavedrom}

\\newpage
### その他各種レンダラを使う {#sec:pandoc-imagine}
他にもplantuml、Mermaid、GNU Plotなどの画像レンダラをを仲介するPandocフィルタを使うことができます。
種類があまりにも多くてPlantUML以外未テストですが、
Imagineフィルタ[^imagine-filter]を使えばコードブロックから
画像生成が可能です。
**このフィルタは出力形式がPNG縛りになっているという欠点があります。**issueが上がってる
ので[^imagine-png-only-issue]きっと近い将来改善されると思います。

- 参考にしたサイトはこちら： UbuntuのVimでPlantUMLをプレビューする on @Qiita[^plantuml-reference]

[^imagine-filter]: https://github.com/hertogp/imagine
[^imagine-png-only-issue]: https://github.com/hertogp/imagine/issues/1
[^plantuml-reference]: https://qiita.com/mitsugu/items/014e13ca0696c7c53d4c

```{.plantuml im_out="fcb,img" caption="PlantUML sample"}
@startuml
skinparam monochrome true
skinparam defaultFontName Ricty Diminished

Bob->Alice: Hello
@enduml
```

PlantUMLからditaa図をレンダリングすることもできます。詳細なオプションがよくわからないんですが、
`scale=3`とすると3倍拡大してくれました。ditaaはもともとPNG出力のみなのでたとえ先述の問題が
解決されSVG出力オプションが付けられるようになっても（拡張子がSVGになっても）
中身はPNGのままです[^plantuml-svg-ditaa]。

[^plantuml-svg-ditaa]: http://plantuml.sourceforge.net/qa/?qa=231/allow-ditaa-png-export-even-when-svg-is-selected

\\newpage
```{.plantuml im_out="fcb,img" caption="ditaa diagram Created through plantuml"}
@startditaa(scale=3)
.                                                     +-------+
------*---------------*---------------*---------------+ FORCE |
      |               |               |               +-------+
      |               |               |
      |               |               |           +-------+
---*---------------*---------------*--------------+ SENSE |
   |  |            |  |            |  |           +-------+
   |  |            |  |            |  |                 +-----+
---|--|--------/---|--|--------/---|--|--------/----/---+ I2C |
   |  |        |   |  |        |   |  |        |    16  +-----+
   |  |        |   |  |        |   |  |        |
 +-+--+------+ | +-+--+------+ | +-+--+------+ |
 | |  |      | | | |  |      | | | |  |      | |
 | *  *      | | | *  *      | | | *  *      | |
 | /<-/<-------+ | /<-/<-------+ | /<-/<-------+
 | *  *      |   | *  *      |   | *  *      |
 | |  |      |   | |  |      |   | |  |      |
 | channel 0 |   | channel 1 |   | channel 2 |
 +-+--+------+   +-+--+------+   +-+--+------+
   |  |            |  |            |  |
 /----+--------+ /----+--------+ /----+--------+
 |             | |             | |             |
 +-------------/ +-------------/ +-------------/
   |               |               |
 /-+-----------+ /-+-----------+ /-+-----------+
 |             | |             | |             |
 +-------------/ +-------------/ +-------------/
@endditaa
```

\\newpage
### 画像を回転する
シンプルな画像回転フィルタです。wavedromとbitfieldとの組み合わせ、拡大縮小も可能です。
wavedrom/bitfieldと組み合わせた場合はSVG/PDF画像の回転を試みます。~~たまにSVGの回転がイマイチになります。~~
_angle_ 指定が正の数で時計回り、負の数は反時計回りです。実際の _angle_ は360で割った余りを用います。
_angle=365_ なら右に5度回転します。
`````markdown
![inline wavedrom rotation sample 30degree](data/waves/wave.yaml){.wavedrom .rotate angle=30}

![inline bitfield rotation sample -30degree](data/bitfields/bit.yaml){.bitfield .rotate angle=-30}

```rotate
source: images/bitfields/bit.png
caption: block png rotation 90degree
angle: 90
---
```
`````

![inline wavedrom rotation sample 30degree](data/waves/wave.yaml){.wavedrom .rotate angle=30}

![inline bitfield rotation sample -30degree](data/bitfields/bit.yaml){.bitfield .rotate angle=-30}


<div id="fig:RotateImage">
![0](data/bitfields/bit.yaml){.bitfield height=30% width=30%}

![30](data/bitfields/bit.yaml){.bitfield .rotate angle=30 height=30% width=30% #fig:RotateImageA}
![60](data/bitfields/bit.yaml){.bitfield .rotate angle=60 height=30% width=30% #fig:RotateImageB}
![90](data/bitfields/bit.yaml){.bitfield .rotate angle=90 height=30% width=30% #fig:RotateImageC}
![120](data/bitfields/bit.yaml){.bitfield .rotate angle=120 height=30% width=30% #fig:RotateImageD}

![150](data/bitfields/bit.yaml){.bitfield .rotate angle=150 height=30% width=30% #fig:RotateImageE}
![180](data/bitfields/bit.yaml){.bitfield .rotate angle=180 height=30% width=30% #fig:RotateImageF}
![210](data/bitfields/bit.yaml){.bitfield .rotate angle=210 height=30% width=30% #fig:RotateImageG}
![240](data/bitfields/bit.yaml){.bitfield .rotate angle=240 height=30% width=30% #fig:RotateImageH}

![270](data/bitfields/bit.yaml){.bitfield .rotate angle=270 height=30% width=30% #fig:RotateImageI}
![300](data/bitfields/bit.yaml){.bitfield .rotate angle=300 height=30% width=30% #fig:RotateImageJ}
![330](data/bitfields/bit.yaml){.bitfield .rotate angle=330 height=30% width=30% #fig:RotateImageK}
![360](data/bitfields/bit.yaml){.bitfield .rotate angle=360 height=30% width=30% #fig:RotateImageL}

回転サンプル
</div>

```rotate
source: images/bitfields/bit.png
#caption: foo
angle: 90
---
```

# 更新履歴 {-}
## Revision1.0（技術書典3） {-}
- 最初の発行。
- 次の目標はDockerイメージ構築です。インストールが楽になる^[予定である]反面、ﾂﾜﾓﾉ以外受け付けなくなる、かも
