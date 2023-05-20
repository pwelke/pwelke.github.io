import bibtexparser
from bibtexparser.customization import *
from bibtexparser.bparser import BibTexParser


def filter_pubtype(list, pubtype):
    return [b for b in list if b['publicationtype'] == pubtype]

def listitem(item):
    if 'doi' in item:
        link = f'https://dx.doi.org/{item["doi"]}'
    elif 'url' in item:
        link = item['url']
    else:
        link = ''

    s =  f'<li>{item["author"]}:<br />\n<a href="{link}">{item["title"]}</a><br />\n'
    if 'journal' in item:
        pass
    s += '</li>\n'
    return s


def get_pubtype_html(list, pubtype):
    s = '<ol>\n'
    for b in filter_pubtype(list, pubtype):
        s += listitem(b)
    s += '</ol>\n'
    return s



bibfile = 'smallref.bib'

def authorfirstlast(record):
    record = author(record)

    authors = list()
    for a in record['author']:
        l, f = a.split(', ')
        s = f + ' ' + l
        authors.append(s)
    record['author'] = ', '.join(authors)
    return record

# Let's define a function to customize our entries.
# It takes a record and return this record.
def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    record = convert_to_unicode(record)
    record = authorfirstlast(record)
    # record = editor(record)
    # record = journal(record)
    # record = keyword(record)
    # record = link(record)
    # record = page_double_hyphen(record)
    # record = doi(record)
    
    # record = add_plaintext_fields(record)
    return record

with open(bibfile) as bibtex_file:
    parser = BibTexParser()
    parser.customization = customizations
    bibdict = bibtexparser.load(bibtex_file, parser=parser)
    print(bibdict.entries)

    for pubtype in ['preprint', 'publication', 'lecturenote']:

        pubs = get_pubtype_html(bibdict.entries, pubtype)
        with open(f'{pubtype}.html', 'w') as o:
            o.write(pubs)
        print(pubtype)
        print(pubs)

