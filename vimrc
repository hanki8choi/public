set shell=/bin/bash
set tabstop=4
set shiftwidth=4
set tags=tags,./tags,../tags,../../tags,../../../tags,../../../../tags,../../../../../tags

set fencs=utf-8,euc-kr,cp949,cp932,euc-jp,shift-jis,big5,latin1,ucs-2le
set hlsearch
set path=.,./include,../include,../../include,../../../include,../../../../include,../../../../../include

set viewoptions=cursor
au BufWinLeave *.c,*.cc,*.h,*.cpp,*.hh,*.html,*.php,Makefile,*.mak mkview
au BufWinEnter *.c,*.cc,*.h,*.cpp,*.hh,*.html,*.php,Makefile,*.mak silent loadview

set mouse=""

