import time
from tqdm import tqdm
from nltk import word_tokenize
import spacy
import stanza
from spacy.lang.en import English
from spacy.lang.de import German
from spacy.lang.fr import French
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER
from spacy.lang.char_classes import CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex
from spacy.lang.zh import Chinese
import hanlp

"This file contains the tokenization functions."
def sent_token_with_nltk_en(input_file, output_file):
    wt = word_tokenize
    output_f = open(output_file, 'w', encoding='utf-8')
    with tqdm(total=1000000) as bar:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                res_token = wt(line.strip(), language="english")
                new_line = " ".join(str(ele) for ele in res_token)
                output_f.write(new_line + "\n")
                bar.update(1)
    output_f.close()


def sent_token_with_nltk_de(input_file, output_file):
    wt = word_tokenize
    output_f = open(output_file, 'w', encoding='utf-8')
    with tqdm(total=1000000) as bar:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                res_token = wt(line.strip(), language="german")
                new_line = " ".join(str(ele) for ele in res_token)
                output_f.write(new_line + "\n")
                bar.update(1)
    output_f.close()


def sent_token_with_nltk_fr(input_file, output_file):
    wt = word_tokenize
    output_f = open(output_file, 'w', encoding='utf-8')
    with open(input_file, 'r', encoding='utf-8') as input_f:
        for line in input_f:
            res_token = wt(line.strip(), language="french")
            new_line = " ".join(str(ele) for ele in res_token)
            output_f.write(new_line + "\n")
    output_f.close()


def sent_token_with_spacy_en(input_file, output_file):
    output_f = open(output_file, 'w', encoding='utf-8')
    sentences = []
    with open(input_file, 'r', encoding='utf-8') as input_f:
        for line in input_f:
            sentences.append(line.strip())
    nlp = English()
    
    infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
            ),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            # ✅ Commented out regex that splits on hyphens between letters:
            # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
            r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
        ]
    )
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer
    tokenizer = nlp.tokenizer
    for doc in tokenizer.pipe(sentences):
        new_line = " ".join(token.text for token in doc)
        output_f.write(new_line + "\n")
    output_f.close()


def sent_token_with_spacy_de(input_file, output_file):
    output_f = open(output_file, 'w', encoding='utf-8')
    sentences = []
    with tqdm(total=30000000) as bar:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                sentences.append(line.strip())
        nlp = German()
        tokenizer = nlp.tokenizer
        for doc in tokenizer.pipe(sentences):
            new_line = " ".join(token.text for token in doc)
            output_f.write(new_line + "\n")
            bar.update(1)
    output_f.close()
    

def sent_token_with_spacy_fr(input_file, output_file):
    output_f = open(output_file, 'w', encoding='utf-8')
    sentences = []
    with open(input_file, 'r', encoding='utf-8') as input_f:
        for line in input_f:
            sentences.append(line.strip())
    nlp = French()
    tokenizer = nlp.tokenizer
    with tqdm(total=6000000) as bar:
        for doc in tokenizer.pipe(sentences):
            new_line = " ".join(token.text for token in doc)
            output_f.write(new_line + "\n")
            bar.update(1)
    output_f.close()


def sent_token_with_spacy_default_zh(input_file, output_file):
    output_f = open(output_file, 'w', encoding='utf-8')
    sentences = []
    with tqdm(total=30000000) as bar:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                sentences.append(line.strip())
        # Character segmentation (default)
        nlp = Chinese()
        tokenizer = nlp.tokenizer
        for doc in tokenizer.pipe(sentences):
            new_line = " ".join(token.text for token in doc)
            output_f.write(new_line + "\n")
            bar.update(1)
    output_f.close()
   
   
def sent_token_with_spacy_pkuseg_zh(input_file, output_file):
    output_f = open(output_file, 'w', encoding='utf-8')
    sentences = []
    with tqdm(total=30000000) as bar:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                sentences.append(line.strip())
        # Character segmentation (default)
        # PKUSeg with "mixed" model provided by pkuseg
        cfg = {"segmenter": "pkuseg"}
        nlp = Chinese.from_config({"nlp": {"tokenizer": cfg}})
        nlp.tokenizer.initialize(pkuseg_model="mixed")
        tokenizer = nlp.tokenizer
        for doc in tokenizer.pipe(sentences):
            new_line = " ".join(token.text for token in doc)
            output_f.write(new_line + "\n")
            bar.update(1)
    output_f.close()
    

def sent_token_with_spacy_jieba_zh(input_file, output_file):
    output_f = open(output_file, 'w', encoding='utf-8')
    sentences = []
    with tqdm(total=30000000) as bar:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                sentences.append(line.strip())
        # Jieba
        cfg = {"segmenter": "jieba"}
        nlp = Chinese.from_config({"nlp": {"tokenizer": cfg}})
        tokenizer = nlp.tokenizer
        for doc in tokenizer.pipe(sentences):
            new_line = " ".join(token.text for token in doc)
            output_f.write(new_line + "\n")
            bar.update(1)
    output_f.close()


def sent_token_with_hanlp_zh(input_file, output_file):
    output_f = open(output_file, 'w', encoding='utf-8')
    sentences = []
    with tqdm(total=30000000) as bar:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                sentences.append(line.strip())
        tok_fine = hanlp.load(hanlp.pretrained.tok.FINE_ELECTRA_SMALL_ZH)
        for sent in tok_fine(sentences):
            new_line = " ".join(word for word in sent)
            output_f.write(new_line + "\n")
            bar.update(1)
    output_f.close()

    
def sent_token_with_stanza_en(input_file, output_file):
    nlp = stanza.Pipeline(lang='en', processors='tokenize', tokenize_no_ssplit=True, tokenize_batch_size=100)
    output_f = open(output_file, 'w', encoding='utf-8')
    with tqdm(total=1000000) as bar:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                doc = nlp(line.strip())
                for sentence in doc.sentences:
                    new_line = " ".join(token.text for token in sentence.tokens)
                output_f.write(new_line + "\n")
                bar.update(1)
    output_f.close()
    

def sent_token_with_stanza_de(input_file, output_file):
    nlp = stanza.Pipeline(lang='de', processors='tokenize', tokenize_no_ssplit=True)
    output_f = open(output_file, 'w', encoding='utf-8')
    with tqdm(total=1000000) as bar:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                doc = nlp(line.strip())
                for sentence in doc.sentences:
                    new_line = " ".join(token.text for token in sentence.tokens)
                output_f.write(new_line + "\n")
                bar.update(1)
    output_f.close()


def sent_token_with_stanza_fr(input_file, output_file):
    nlp = stanza.Pipeline(lang='fr', processors='tokenize', tokenize_no_ssplit=True)
    output_f = open(output_file, 'w', encoding='utf-8')
    sent_list = []
    with open(input_file, 'r', encoding='utf-8') as input_f:
        for line in input_f:
            sent_list.append(line.strip())
    in_doc = [stanza.Document([],text=d) for d in sent_list]
    docs = nlp(in_doc)
    for doc in docs:
        for sentence in doc.sentences:
            new_line = " ".join(token.text for token in sentence.tokens)
            output_f.write(new_line + "\n")
    output_f.close()
    

if __name__ == '__main__':
    #road = "D:\\thesis_data\\cc_Matrix\\1000k\\sou\\"
    #input_name = "de-1000k.txt"
    road = "D:\\thesis_data\\cc_Matrix\\en_fr\\"
    input_name = "en_6000k.txt"
    output_name = "en_token_6000k.txt"
    time_s = time.time()
    sent_token_with_spacy_en(road+input_name, road+output_name)
    time_e = time.time()
    time_line = 'time cost ' + str(time_e-time_s) + ' s.\n'
    print(time_line)
    #for idx in range(2, 11):
        #input_name = "de_token_"+str(idx)+".txt"
        #output_name = "de_token_new_"+str(idx)+".txt"
        #time_s = time.time()
        #sent_token_with_spacy_de(road+input_name, road+output_name)
        #time_e = time.time()
        #time_line = 'time cost ' + str(time_e-time_s) + ' s.\n'
        #print(time_line)
    #time_name = "time_stanza_fr.txt"
    #time_f = open(road+time_name, 'w', encoding='utf-8')
    #time_f.write(time_line)
    #time_f.close()

