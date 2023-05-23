from pathlib import Path
from generate_bib import convert

# specify the categories
pubtypes = ['preprint', 'publication', 'lecturenote', 'nonarchival', 'book']

# convert bibfile to html lists
convert('pascal.bib', pubtypes)

# load files
index = Path('index.html_template').read_text()

for pubtype in pubtypes:
	reflist = Path(f'{pubtype}.html_part').read_text()
	index = index.replace(f'<object type="text/html" data="{pubtype}.html_part"></object>', reflist)

# write 
Path('index.html').write_text(index)