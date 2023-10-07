from tqdm import tqdm
import time
from nltk import word_tokenize
from gensim.corpora import WikiCorpus
import xml.dom.minidom



def add_root_to_file(input_file, output_file):
    root_start = "<article>"
    root_end = "</article>"
    with open(output_file, 'w', encoding='utf-8')as output_f:
        output_f.write(root_start + "\n")
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                output_f.write(line)
        output_f.write(root_end + "\n")


def get_articles_from_file(input_file, output_file):
    dom = xml.dom.minidom.parse(input_file)
    root = dom.documentElement
    bb = root.getElementsByTagName('doc')
    with open(output_file, 'w', encoding='utf-8') as output_f:
        for b in bb:
            output_f.write(b.firstChild.data)


def get_articles_size_from_file(input_file, output_file):
    dom = xml.dom.minidom.parse(input_file)
    root = dom.documentElement
    docs = root.getElementsByTagName('doc')
    with open(output_file, 'w', encoding='utf-8') as output_f:
        for doc in docs:
            title_doc = doc.getAttribute("title")
            size_doc = len(doc.firstChild.data)
            output_f.write(title_doc + " ||| " + str(size_doc) + "\n")


def clean_text(input_file, output_file):
    with open(output_file, 'w', encoding='utf-8') as output_f:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                if len(line.strip()) == 0:
                    continue
                output_f.write(line.strip() + "\n")


def get_wiki_article(input_file, output_file):
    i = 0
    wiki = WikiCorpus(input_file, dictionary={}, processes=4, lower=False)
    output = open(output_file, 'w', encoding='utf-8')
    for text in wiki.get_texts():
        str_line = " ".join(text) + "\n"
        output.write(str_line)
        i = i + 1
        if i % 10000 == 0:
            print("Save "+str(i/10000) + " articles.\n")
    output.close()
    print("finished.\n")


def en_token_process(input_file, output_file):
    i = 0
    output = open(output_file, 'w', encoding='utf-8')
    wt = word_tokenize
    with open(input_file, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            original_sent_en = line.strip()
            en_sent_p = wt(original_sent_en, language="english")
            output_sent_en = " ".join(str(ele) for ele in en_sent_p)
            output.write(output_sent_en+"\n")
            i = i + 1
            if i % 10000 == 0:
                print("Save " + str(i) + " articles.\n")
    output.close()


def de_token_process(input_file, output_file):
    i = 0
    output = open(output_file, 'w', encoding='utf-8')
    wt = word_tokenize
    with open(input_file, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            original_sent_de = line.strip()
            de_sent_p = wt(original_sent_de, language="german")
            output_sent_de = " ".join(str(ele) for ele in de_sent_p)
            output.write(output_sent_de+"\n")
            i = i + 1
            if i % 10000 == 0:
                print("Save " + str(i) + " articles.\n")
    output.close()
    
    
if __name__ == '__main__':
    wiki_file_road = "E:\\wiki\\01.11.2022\\wiki_extractor\\zh\\"
    size_road = "E:\\wiki\\01.11.2022\\wiki_extractor\\zh\\size\\"
    for f_idx in range(0, 2):
        idx = "0"+str(f_idx)
        new_wiki_file = "wiki_" + idx +".txt"
        output_file = "wiki_article_size_" + idx + ".txt"
        get_articles_size_from_file(wiki_file_road + new_wiki_file, size_road + output_file)

    
    
