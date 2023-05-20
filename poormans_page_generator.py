from pathlib import Path
from generate_bib import convert


# convert bibfile to html lists
convert('smallref.bib')

# load files
index = Path('index.html_template').read_text()
publication = Path('publication.html_part').read_text()
preprint = Path('preprint.html_part').read_text()
lecturenote = Path('lecturenote.html_part').read_text()

# replace things
index = index.replace('<object type="text/html" data="preprint.html_part"></object>', preprint)
index = index.replace('<object type="text/html" data="publication.html_part"></object>', publication)
index = index.replace('<object type="text/html" data="lecturenote.html_part"></object>', lecturenote)

# write 
Path('index.html').write_text(index)