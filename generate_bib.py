import sys
from pathlib import Path

import bibtexparser
from bibtexparser.customization import *
from bibtexparser.bparser import BibTexParser


def filter_pubtype(list, pubtype):
    '''filter by pubtype and sort in reverse chronological order'''
    filtered_list = [b for b in list if b['publicationtype'] == pubtype]
    return sorted(filtered_list, key=lambda b: b['year'], reverse=True)

def nonempty(string, item):
    return (string in item) and (item[string] != '')

def format_bibitem(item):
    '''the main workhorse'''
    if 'doi' in item:
        link = f'https://dx.doi.org/{item["doi"]}'
    elif 'url' in item:
        link = item['url']
    else:
        link = ''

    # authors and title
    s =  f'<li>{item["author"]} ({item["year"]}):<br />\n'
    s += f'<a href="{link}">{item["title"]}</a>.<br />\n'

    # venue formatting
    if item['ENTRYTYPE'] == 'article':
        if nonempty('journal', item):
            s += f'{item["journal"]}'
            if nonempty("volume", item):
                s += f' ({item["volume"]})'
            # if nonempty('publisher', item):
            #     s += f', {item["publisher"]}'
            s += '<br />\n'
    if item['ENTRYTYPE'] == 'inproceedings':
        if nonempty('booktitle', item):
            s += f'{item["booktitle"]}'
            # if nonempty('publisher', item):
            #     s += f', {item["publisher"]}'
            s += '<br />\n'


    if nonempty('comment', item):
        s += f'({item["comment"]})<br />\n'

    if nonempty('abstract', item):
        s += f'<p class="discreet">{item["abstract"]}</p>\n'

    # footer row with optionals
    s += '<p class="discreet">\n'
    if nonempty('pdf', item):
        s += f'[<a href="{item["pdf"]}">pdf</a>]\n'
    if nonempty('poster', item):
        s += f'[<a href="{item["poster"]}">poster</a>]\n'
    if nonempty('slides', item):
        s += f'[<a href="{item["slides"]}">slides</a>]\n'
    if nonempty('video', item):
        s += f'[<a href="{item["video"]}">video</a>]\n'
    if nonempty('code', item):
        s += f'[<a href="{item["code"]}">code</a>]\n'
    if nonempty('reproduciblerun', item):
        s += f'[<a href="{item["reproduciblerun"]}">reproducible run</a>]\n'
    if nonempty('doi', item):
        s += f'[<a href="https://dx.doi.org/{item["doi"]}">doi</a>]\n'
    if nonempty('reviews', item):
        s += f'[<a href="{item["reviews"]}">reviews</a>]\n'
    if nonempty('eprint', item):
        s += f'[<a href="https://arxiv.org/abs/{item["eprint"]}">arXiv</a>]\n'        
    if nonempty('biburl', item):
        s += f'[<a href="{item["biburl"]}">bibtex</a>]\n'
    if nonempty('venuetype', item):
        s += f'[<a href="{item["venueurl"]}">{item["venuetype"]}</a>]\n'
    
    s += '</p>'
    s += '</li>\n'
    return s


def get_pubtype_html(list, pubtype):
    '''Create a html list of all (sorted) items of type pubtype'''
    s = '<ol>\n'
    for b in filter_pubtype(list, pubtype):
        s += format_bibitem(b)
    s += '</ol>\n'
    return s


def authorfirstlast(record):
    record = author(record)

    authors = list()
    for a in record['author']:
        l, f = a.split(', ')
        s = f + ' ' + l
        authors.append(s)
    record['author'] = ', '.join(authors)
    return record


def customizations(record):
    '''A function to customize our entries.
    It takes a record and return this record.'''

    record = convert_to_unicode(record)
    record = authorfirstlast(record)
    return record

def convert(bibfile, pubtypes=['preprint', 'publication', 'lecturenote', 'nonarchival', 'book']):
    with open(bibfile) as bibtex_file:
        parser = BibTexParser()
        parser.customization = customizations
        bibdict = bibtexparser.load(bibtex_file, parser=parser)

        for pubtype in pubtypes:
            pubs = get_pubtype_html(bibdict.entries, pubtype)
            with open(f'{pubtype}.html_part', 'w') as o:
                o.write(pubs)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        bibfile = sys.argv[1]
    else:
        sys.stderr.write(f'Usage: python {sys.argv[0]} BIBFILE\n')
        sys.exit(1)

    convert(bibfile)