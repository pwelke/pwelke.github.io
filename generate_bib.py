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


def cf(s1, s2, format):
    if format == 'html':
        return s1
    if format == 'tex':
        return s2

def format_bibitem(item, format):
    '''the main workhorse'''
    if nonempty('doi', item):
        link = f'https://dx.doi.org/{item["doi"]}'
    elif nonempty('url', item):
        link = item['url']
    elif nonempty('pdf', item):
        link = item['pdf']
    else:
        link = ''


    # abstract as mouseover if available
    if nonempty('abstract', item):
        abstract = cf(f'title="{item["abstract"]}"', '', format)
    else:
        abstract = ''

    # start list item
    s = cf('<li>\n', '\\item\n', format)

    # add a label, if desired (for tex this is useful for referencing)
    s += cf('', f'\\label{{{item["ID"]}}}\n', format)

    # authors and title
    s +=  f'{item["author"]} ({item["year"]}):'
    s += cf('<br />\n', '\\newline\n', format)
    s += cf(f'<a {abstract} href="{link}">{item["title"]}</a>.', f'\\href{{{link}}}{{{item["title"]}}}', format)
    s += cf('<br />\n', '\\newline\n', format)

    # venue formatting
    if item['ENTRYTYPE'] == 'article':
        if nonempty('journal', item):
            s += f'{item["journal"]}'
            if nonempty("volume", item):
                s += f' ({item["volume"]})'
            s += cf('<br />\n', '\\newline\n', format)

    if item['ENTRYTYPE'] == 'inproceedings':
        if nonempty('booktitle', item):
            s += f'{item["booktitle"]}'
            s += cf('<br />\n', '\\newline\n', format)


    if nonempty('comment', item):
        s += f'({item["comment"]})'
        s += cf('<br />\n', '\\newline\n', format)

    # footer row with optionals
    s += cf('<p class="discreet">\n', f'{{\\footnotesize\n', format)
    if nonempty('pdf', item):
        s += cf(f'[<a href="{item["pdf"]}">pdf</a>]\n', f'[\\href{{{item["pdf"]}}}{{pdf}}]\n', format)
    if nonempty('poster', item):
        s += cf(f'[<a href="{item["poster"]}">poster</a>]\n', f'[\\href{{{item["poster"]}}}{{poster}}]\n', format)
    if nonempty('slides', item):
        s += cf(f'[<a href="{item["slides"]}">slides</a>]\n', f'[\\href{{{item["slides"]}}}{{slides}}]\n', format)
    if nonempty('video', item):
        s += cf(f'[<a href="{item["video"]}">video</a>]\n', f'[\\href{{{item["video"]}}}{{video}}]\n', format)
    if nonempty('code', item):
        s += cf(f'[<a href="{item["code"]}">code</a>]\n', f'[\\href{{{item["code"]}}}{{code}}]\n', format)
    if nonempty('reproduciblerun', item):
        s += cf(f'[<a href="{item["reproduciblerun"]}">reproducible run</a>]\n', f'[\\href{{{item["reproduciblerun"]}}}{{reproducible run}}]\n', format)
    if nonempty('doi', item):
        s += cf(f'[<a href="https://dx.doi.org/{item["doi"]}">doi</a>]\n', f'[\\href{{https://dx.doi.org/{item["doi"]}}}{{doi}}]\n', format)
    if nonempty('reviews', item):
        s += cf(f'[<a href="{item["reviews"]}">reviews</a>]\n', f'[\\href{{{item["reviews"]}}}{{reviews}}]\n', format)
    if nonempty('eprint', item):
        s += cf(f'[<a href="https://arxiv.org/abs/{item["eprint"]}">arXiv</a>]\n', f'[\\href{{https://arxiv.org/abs/{item["eprint"]}}}{{arxiv}}]\n', format)
    if nonempty('biburl', item):
        s += cf(f'[<a href="{item["biburl"]}">bibtex</a>]\n', f'[\\href{{{item["biburl"]}}}{{bibtex}}]\n', format)
    if nonempty('venuetype', item):
        s += cf(f'[<a href="{item["venueurl"]}">{item["venuetype"]}</a>]\n', f'[\\href{{{item["venueurl"]}}}{{{item["venuetype"]}}}]\n', format)
    
    s += cf('</p>\n', f'}}\n', format)
    s += cf('</li>\n', '', format)
    return s


def get_pubtype(list, pubtype, format):
    '''Create a html list of all (sorted) items of type pubtype'''
    s = cf('<ol>\n', '\\begin{enumerate}\n\\conti\n', format)
    noItems = True
    for b in filter_pubtype(list, pubtype):
        s += format_bibitem(b, format)
        noItems = False
    if noItems:
        # suppress 'perhaps a missing \item?' latex error  
        s += cf('', '\\makeatletter\\let\\@noitemerr\\relax\\makeatother\n', format)
    s += cf('</ol>\n', '\\seti\n\\end{enumerate}', format)
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

def convert(bibfile, pubtypes=['preprint', 'publication', 'lecturenote', 'nonarchival', 'book'], format='html'):
    with open(bibfile) as bibtex_file:
        parser = BibTexParser()
        parser.customization = customizations
        bibdict = bibtexparser.load(bibtex_file, parser=parser)

        for pubtype in pubtypes:
            pubs = get_pubtype(bibdict.entries, pubtype, format=format)
            with open(f'{pubtype}.{format}_part', 'w') as o:
                o.write(pubs)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        bibfile = sys.argv[1]
    else:
        sys.stderr.write(f'Usage: python {sys.argv[0]} BIBFILE\n')
        sys.exit(1)

    convert(bibfile)