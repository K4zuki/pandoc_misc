$if(title)$
::: {custom-style="Title"}
`<w:fldSimple w:instr="DOCPROPERTY  TITLE-META \* MERGEFORMAT"></w:fldSimple>`{=openxml}
:::
$endif$

$if(subtitle)$
::: {custom-style="Abstract"}
$subtitle$
:::
$endif$

$if(author)$
::: {custom-style="Author"}
`<w:fldSimple w:instr="DOCPROPERTY  AUTHOR-META \* MERGEFORMAT"></w:fldSimple>`{=openxml} $if(circle)$/ $circle$$endif$
:::
$endif$
\newpage
