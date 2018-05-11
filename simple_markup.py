import  sys,re
from util import  *
print '<html><head><title>XML</title><body>'
title=True
for block in blocks(sys.stdin):
    block=re.sub(r'\*(.+?)\*',r'<em>\l</em>',block)
    if title:
        print '<h1>'
        print block
        print '</h1>'
        title=False
    else:
        print '<p>'
        print block
        print '</p>'
    print '</body></html>'

