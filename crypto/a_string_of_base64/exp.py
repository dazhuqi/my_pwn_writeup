import os
import re
import base64
import html

from boltons.urlutils import unquote

curr_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(curr_dir, 'file.txt') # a file include base64 encode

with open(file_path, 'r') as f:
    for line in f:
        if not line.strip():
            continue
        raw_text = base64.b64decode(line).decode('unicode_escape') # base64 -> oct -> hex -> unicode -> js

        next_layer = "".join(chr(int(n)) for n in re.findall(r'\d+', raw_text)) # js -> html

        res = unquote(html.unescape(next_layer)) # html(2) -> URL -> flag

        print(res)