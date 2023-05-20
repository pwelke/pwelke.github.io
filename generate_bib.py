import sys

import bibtexparser
from bibtexparser.customization import *
from bibtexparser.bparser import BibTexParser


def filter_pubtype(list, pubtype):
    '''filter by pubtype and sort in reverse chronological order'''
    filtered_list = [b for b in list if b['publicationtype'] == pubtype]
    return sorted(filtered_list, key=lambda b: (b['year'], b['author']), reverse=True)

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
        s += f'{item["journal"]}, {item["publisher"]}<br />'
    if item['ENTRYTYPE'] == 'inproceedings':
        s += f'{item["booktitle"]}, {item["publisher"]}<br />'

    # footer row with optionals
    s += '<p class="discreet">\n'
    if 'url' in item:
        s += f'[<a href="{item["url"]}">pdf</a>]\n'
    if 'poster' in item:
        s += f'[<a href="{item["poster"]}">poster</a>]\n'
    if 'video' in item:
        s += f'[<a href="{item["video"]}">poster</a>]\n'
    if 'codeurl' in item:
        s += f'[<a href="{item["codeurl"]}">code</a>]\n'
    if 'doi' in item:
        s += f'[<a href="https://dx.doi.org/{item["doi"]}">doi</a>]\n'
    if 'biburl' in item:
        s += f'[<a href="{item["biburl"]}">bibtex</a>]\n'
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

def convert(bibfile):
    with open(bibfile) as bibtex_file:
        parser = BibTexParser()
        parser.customization = customizations
        bibdict = bibtexparser.load(bibtex_file, parser=parser)
        print(bibdict.entries)

        for pubtype in ['preprint', 'publication', 'lecturenote']:

            pubs = get_pubtype_html(bibdict.entries, pubtype)
            with open(f'{pubtype}.html_part', 'w') as o:
                o.write(pubs)
            print(pubtype)
            print(pubs)



if __name__ == '__main__':

    if len(sys.argv) == 2:
        bibfile = sys.argv[1]
    else:
        sys.stderr.write(f'Usage: python {sys.argv[0]} BIBFILE\n')
        sys.exit(1)

    convert(bibfile)