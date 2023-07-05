from pathlib import Path
from generate_bib import convert

import re
import subprocess


def create_homepage(pubtypes):
	# convert bibfile to html lists
	convert('pascal.bib', pubtypes, format='html')

	# load files
	index = Path('index.html_template').read_text()

	for pubtype in pubtypes:
		reflist = Path(f'{pubtype}.html_part').read_text()
		index = index.replace(f'<object type="text/html" data="{pubtype}.html_part"></object>', reflist)

	# write 
	Path('index.html').write_text(index)

	# clean up
	for pubtype in pubtypes:
		Path(f'{pubtype}.html_part').unlink()


def create_latex(pubtypes, baseurl):
	# convert bibfile to html lists
	convert('pascal.bib', pubtypes, format='tex')

	# load files
	index = Path('reflist.tex_template').read_text()

	for pubtype in pubtypes:
		reflist = Path(f'{pubtype}.tex_part').read_text()
		index = index.replace(f'\\input{{{pubtype}.tex_part}}', reflist)

	# add baseurl to relative urls for a standalone pdf version
	index = re.sub('\\\\href\{(?!https://)', f'\\\\href{{{baseurl}', index)

	# write 
	Path('reflist.tex').write_text(index)

	cmd = ['latexmk', '-xelatex', '-shell-escape', 'reflist.tex']
	subprocess.run(cmd)

	# clean up
	for pubtype in pubtypes:
		Path(f'{pubtype}.tex_part').unlink()

	for extension in ['aux', 'fdb_latexmk', 'fls', 'log', 'out', 'xdv']:
		Path(f'reflist.{extension}').unlink()



if __name__ == '__main__':
	# specify the categories
	pubtypes = ['preprint', 'publication', 'lecturenote', 'nonarchival', 'book']

	create_homepage(pubtypes)
	create_latex(pubtypes, baseurl='https://pwelke.github.io/')