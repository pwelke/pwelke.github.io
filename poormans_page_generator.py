#!/usr/bin/env python

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


def create_latex(pubtypes, baseurl, template):
	# convert bibfile to tex lists
	convert('pascal.bib', pubtypes, format='tex')

	# load files
	index = Path(f'{template}.tex_template').read_text()

	for pubtype in pubtypes:
		reflist = Path(f'{pubtype}.tex_part').read_text()
		index = index.replace(f'\\input{{{pubtype}.tex_part}}', reflist)

	# add baseurl to relative urls for a standalone pdf version
	index = re.sub('\\\\href\{(?!http)', f'\\\\href{{{baseurl}', index)

	# write 
	Path(f'{template}.tex').write_text(index)

def compile_latex(template, pubtypes):
	cmd = ['latexmk', '-xelatex', '-shell-escape', f'{template}.tex']
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
	create_latex(pubtypes, baseurl='https://pwelke.de/', template='reflist')
	create_latex(pubtypes + ['underreview'], baseurl='https://pwelke.de/', template='reflistcv')
	compile_latex('reflist', pubtypes + ['underreview'])