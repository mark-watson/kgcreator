from os import scandir
from os.path import splitext, exists
from pprint import pprint
import spacy

try:
  nlp_model = spacy.load('en_core_web_sm')
except:
  print("Loading spaCy model file...")
  from os import system
  system("python -m spacy download en_core_web_sm")
  nlp_model = spacy.load('en_core_web_sm')


def find_entities_in_text(some_text):

    def clean(s):
        return s.replace('\n', ' ').strip()
    doc = nlp_model(some_text)
    return map(list, [[clean(entity.text), entity.label_] for entity in doc.ents])


def data2Rdf(meta_data, entities, fout):
    for [value, abbreviation] in entities:
        a_literal = '"' + value + '"'
        if value in v2umap:
            a_literal = v2umap[value]
        fout.write('<' + meta_data + '>\t' + e2umap[abbreviation] + '\t' +
            a_literal + ' .\n') if abbreviation in e2umap else None

        
def data2Cypher(meta_data, entities, fout):
    " TBD: implement "
    SUMMARY = "To Be Done"
    for [name, atype] in entities:
        if atype in e2umap:
            fout.write('CREATE (' + name.replace(" ", '_') + ':CategoryType {name:' + e2umap[atype] + '})\n')
    # start by creating a node for source URI:
    meta_print_name = meta_data[meta_data.index('//') + 2:]
    fout.write('CREATE (' + meta_print_name + ':News {name:"' + meta_print_name + '", uri: "' +
               meta_data + '", summary: "' + SUMMARY + '"})\n')

    for [name, atype] in entities:
        fout.write('CREATE (' + name.replace(" ", '_') + ')-[:Category]->(' + e2umap[atype] + '))\n')
        fout.write('CREATE (' + meta_print_name + ')-[:' + e2umap[atype] + ')->(' + name.replace(" ", '_') + ')\n')

e2umap = {'ORG': '<https://schema.org/Organization>',
          'LOC': '<https://schema.org/location>',
          'GPE': '<https://schema.org/location>',
          'NORP': '<https://schema.org/nationality>',
          'PRODUCT': '<https://schema.org/Product>',
          'PERSON': '<https://schema.org/Person>'}
v2umap = {'IBM': '<http://dbpedia.org/page/IBM>',
          'The Wall Street Journal': '<http://dbpedia.org/page/The_Wall_Street_Journal>',
          'Banco Espirito': '<http://dbpedia.org/page/Banco_Esp%C3%ADrito_Santo>',
          'Australian Broadcasting Corporation': '<http://dbpedia.org/page/Australian_Broadcasting_Corporation>',
          'Australian Writers Guild': '<http://dbpedia.org/page/Australian_Broadcasting_Corporation>',
          'Microsoft': '<http://dbpedia.org/page/Microsoft>'}


def process_directory(directory_name, output_rdf, output_neo4j):
    with open(output_rdf, 'w') as frdf:
        with open(output_neo4j, 'w') as fneo4j:
            with scandir(directory_name) as entries:
                for entry in entries:
                    [_, file_extension] = splitext(entry.name)
                    if file_extension == '.txt':
                        check_file_name = entry.path[0:-4:None] + '.meta'
                        if exists(check_file_name):
                            process_file(entry.path, check_file_name, frdf, fneo4j)
                        else:
                            print('Warning: no .meta file for', entry.path, 'in directory', directory_name)

def process_file(txt_path, meta_path, frdf, fneo4j):

    print(f"** process_file txt_path={txt_path} meta_path={meta_path}")
    def read_data(text_path, meta_path):
        with open(text_path) as f:
            t1 = f.read()
        with open(meta_path) as f:
            t2 = f.read()
        return [t1, t2]

    def modify_entity_names(ename):
        return ename.replace('the ', '')

    [txt, meta] = read_data(txt_path, meta_path)
    entities = find_entities_in_text(txt)
    entities = [[modify_entity_names(e), t] for [e, t] in entities if t in
        ['NORP', 'ORG', 'PRODUCT', 'GPE', 'PERSON', 'LOC']]
    data2Rdf(meta, entities, frdf)
    data2Cypher(meta, entities, fneo4j)


# process_directory('../test_data', 'out.rdf', 'out.cypher')

