$if(title)$
::: {custom-style="Title"}
`<w:fldSimple w:instr="DOCPROPERTY  TITLE-META \* MERGEFORMAT"></w:fldSimple>`{=openxml}
:::
$endif$

$if(subtitle)$
::: {custom-style="Abstract"}
`<w:fldSimple w:instr="DOCPROPERTY  subtitle-meta \* MERGEFORMAT"></w:fldSimple>`{=openxml}
:::
$endif$

$if(author)$
::: {custom-style="Author"}
`<w:fldSimple w:instr="DOCPROPERTY  author-meta \* MERGEFORMAT"></w:fldSimple>`{=openxml}
$if(circle)$/`<w:fldSimple w:instr="DOCPROPERTY  circle \* MERGEFORMAT"></w:fldSimple>`{=openxml}
$endif$
:::
$endif$
\newpage
