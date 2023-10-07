import flair.nn.model
import spacy
import stanza
import time
from tqdm import tqdm
from flair.data import Sentence
from flair.models import SequenceTagger
import hanlp
import universal_func as uf

"This file implements the functions of using the NER model to identify words that need to be explained."
def get_sentences_res(word_file_road):
    sent_res = []
    #total_word_nums = 0
    print("get sentence begin...\n")
    with open(word_file_road, 'r', encoding='utf-8') as word_file:
        with tqdm(total=1000000) as bar:
            for sent in word_file:
                sent_res.append(sent.strip())
                bar.update(1)
    print("get sentence finish...\n")
    return sent_res


def get_cand_from_file_sou(file_road):
    cand_sou = []
    sou_cand_file = open(file_road, 'r', encoding='utf-8')
    sou_cand = sou_cand_file.readlines()
    for line in sou_cand:
        res_each_align = line.strip().split()
        word = res_each_align[0]
        tar_word = res_each_align[1]
        sentence_idx = int(res_each_align[2])
        align_idx = int(res_each_align[3])
        word_sou_idx = int(res_each_align[4])
        word_tar_idx = int(res_each_align[5])
        sou_idx_2 = int(res_each_align[6])
        tar_idx_2 = int(res_each_align[7])
        sou_word_freq = int(res_each_align[8])
        tar_word_freq = int(res_each_align[9])
        sou_wiki_freq = int(res_each_align[10])
        tar_wiki_freq = int(res_each_align[11])
        new_ele_align = (word, tar_word, sentence_idx, align_idx, word_sou_idx, word_tar_idx,
                                 sou_idx_2, tar_idx_2, sou_word_freq, tar_word_freq, sou_wiki_freq, tar_wiki_freq)
        cand_sou.append(new_ele_align)
    sou_cand_file.close()
    return cand_sou


def get_cand_from_file_tar(file_road):
    cand_tar = []
    tar_cand_file = open(file_road, 'r', encoding='utf-8')
    tar_cand = tar_cand_file.readlines()
    for line in tar_cand:
        res_each_align = line.strip().split()
        word = res_each_align[0]
        sou_word = res_each_align[1]
        sentence_idx = int(res_each_align[2])
        align_idx = int(res_each_align[3])
        word_tar_idx = int(res_each_align[4])
        word_sou_idx = int(res_each_align[5])
        tar_idx_2 = int(res_each_align[6])
        sou_idx_2 = int(res_each_align[7])
        tar_word_freq = int(res_each_align[8])
        sou_word_freq = int(res_each_align[9])
        tar_wiki_freq = int(res_each_align[10])
        sou_wiki_freq = int(res_each_align[11])
        new_ele_align = (word, sou_word, sentence_idx, align_idx, word_tar_idx, word_sou_idx,
                                 tar_idx_2, sou_idx_2, tar_word_freq, sou_word_freq, tar_wiki_freq, sou_wiki_freq)
        cand_tar.append(new_ele_align)
    tar_cand_file.close()
    return cand_tar


def check_ner_stan_sou(cand, sentences, nlp_stan):
    res = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, _, _, _, _, _, _) = cand
    sent = sentences[sent_idx].strip()
    sent_list = sent.split()
    word_start_p = word_sou_idx
    for w_idx in range(word_sou_idx):
        word_start_p = word_start_p + len(sent_list[w_idx])
    doc = nlp_stan(" ".join(sent_list))
    ent_res = None
    for ent in doc.ents:
        ent_s_p = ent.start_char
        ent_e_p = ent.end_char
        if word_start_p in range(ent_s_p,ent_e_p):
            res = True
            ent_res = ent.text
            break
    #for ent in doc.ents:
    #    if word in ent.text:
    #        res = True
    #        ent_res = ent.text
    #        break
    return res, ent_res


def check_ner_stan_tar(cand, sentences, nlp_stan):
    res = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, _, _, _, _, _, _) = cand
    sent = sentences[sent_idx].strip()
    sent_list = sent.split()
    word_start_p = word_tar_idx
    for w_idx in range(word_tar_idx):
        word_start_p = word_start_p + len(sent_list[w_idx])
    doc = nlp_stan(" ".join(sent_list))
    ent_res = None
    for ent in doc.ents:
        ent_s_p = ent.start_char
        ent_e_p = ent.end_char
        if word_start_p in range(ent_s_p,ent_e_p):
            res = True
            ent_res = ent.text
            break
    #for ent in doc.ents:
    #    if tar_word in ent.text:
    #        res = True
   #         ent_res = ent.text
    #        break
    return res, ent_res


def check_ner_spacy_sou(cand, sentences, nlp_spacy:spacy.Language):
    res = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, _, _, _, _, _, _) = cand
    sent = sentences[sent_idx].strip()
    sent_list = sent.split()
    word_start_p = word_sou_idx
    for w_idx in range(word_sou_idx):
        word_start_p = word_start_p + len(sent_list[w_idx])
    doc = nlp_spacy(" ".join(sent_list))
    ent_res = None
    for ent in doc.ents:
        ent_s_p = ent.start_char
        ent_e_p = ent.end_char
        if word_start_p in range(ent_s_p, ent_e_p):
            res = True
            ent_res = ent.text
            break
    #for ent in doc.ents:
    #    if word in ent.text:
    #        res = True
    #        ent_res = ent.text
    #        break
    return res, ent_res


def check_ner_spacy_tar(cand, sentences, nlp_spacy:spacy.Language):
    res = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, _, _, _, _, _, _) = cand
    sent = sentences[sent_idx].strip()
    sent_list = sent.split()
    word_start_p = word_tar_idx
    for w_idx in range(word_tar_idx):
        word_start_p = word_start_p + len(sent_list[w_idx])
    doc = nlp_spacy(" ".join(sent_list))
    ent_res = None
    for ent in doc.ents:
        ent_s_p = ent.start_char
        ent_e_p = ent.end_char
        if word_start_p in range(ent_s_p, ent_e_p):
            res = True
            ent_res = ent.text
            break
    #for ent in doc.ents:
    #    if tar_word in ent.text:
    #        res = True
    #        ent_res = ent.text
    #        break
    return res, ent_res


def check_ner_flair_sou(cand, sentences, nlp_flair:flair.nn.model.Model):
    res = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, _, _, _, _, _, _) = cand
    sent = sentences[sent_idx].strip()
    sent_list = sent.split()
    word_start_p = word_sou_idx
    for w_idx in range(word_sou_idx):
        word_start_p = word_start_p + len(sent_list[w_idx])
    sent_new = Sentence(" ".join(sent_list), use_tokenizer=False)
    nlp_flair.predict(sent_new)
    ent_res = None
    for entity in sent_new.get_spans('ner'):
        entity_s_p = entity.start_position
        entity_e_p = entity.end_position
        if word_start_p in range(entity_s_p, entity_e_p):
            res = True
            ent_res = entity.text
            break
    #for entity in sent_new.get_spans('ner'):
    #    if word in entity.text:
    #        res = True
    #        ent_res = entity.text
    #        break
    return res, ent_res


def check_ner_flair_tar(cand, sentences, nlp_flair:flair.nn.model.Model):
    res = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, _, _, _, _, _, _) = cand
    sent = sentences[sent_idx].strip()
    sent_list = sent.split()
    word_start_p = word_tar_idx
    for w_idx in range(word_tar_idx):
        word_start_p = word_start_p + len(sent_list[w_idx])
    sent_new = Sentence(" ".join(sent_list), use_tokenizer=False)
    nlp_flair.predict(sent_new)
    ent_res = None
    for entity in sent_new.get_spans('ner'):
        entity_s_p = entity.start_position
        entity_e_p = entity.end_position
        if word_start_p in range(entity_s_p, entity_e_p):
            res = True
            ent_res = entity.text
            break
    #for entity in sent_new.get_spans('ner'):
    #    if tar_word in entity.text:
    #        res = True
    #        ent_res = entity.text
    #        break
    return res, ent_res


def check_ner_hanlp_sou(cand, sentences, nlp_hanlp):
    res = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, _, _, _, _, _, _) = cand
    sent = sentences[sent_idx].strip()
    sent_list = sent.split()
    ner_res = nlp_hanlp(sent_list)
    ent_res = None
    for ner_ele in ner_res:
        (ner_entity, type_ner, start_idx, end_idx) = ner_ele
        if word in ner_entity and word_sou_idx in range(start_idx, end_idx):
            res = True
            ent_res = ner_entity
            break
    #for ent in doc.ents:
    #    if word in ent.text:
    #        res = True
    #        ent_res = ent.text
    #        break
    return res, ent_res


def check_ner_hanlp_tar(cand, sentences, nlp_hanlp):
    res = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, _, _, _, _, _, _) = cand
    sent = sentences[sent_idx].strip()
    sent_list = sent.split()
    ner_res = nlp_hanlp(sent_list)
    ent_res = None
    for ner_ele in ner_res:
        (ner_entity, type_ner, start_idx, end_idx) = ner_ele
        if tar_word in ner_entity and word_tar_idx in range(start_idx, end_idx):
            res = True
            ent_res = ner_entity
            break
    #for ent in doc.ents:
    #    if tar_word in ent.text:
    #        res = True
   #         ent_res = ent.text
    #        break
    return res, ent_res


def check_ner_sou_spacy(cand, sou_sent, nlp_sp_sou, tar_sent, nlp_sp_tar):
    res_1 = False
    res_2 = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_count, word_tar_count) = cand
    sentence_sou = sou_sent[sent_idx].strip()
    sentence_tar = tar_sent[sent_idx].strip()
    doc_sou = nlp_sp_sou(sentence_sou)
    doc_tar = nlp_sp_tar(sentence_tar)
    ent_sou = []
    ent_tar = []
    new_cand = None
    for ent in doc_sou.ents:
        if word in ent.text:
            res_1 = True
            ent_sou.append(ent.text)
            break
    for ent in doc_tar.ents:
        if tar_word in ent.text:
            res_2 = True
            ent_tar.append(ent.text)
            break
    if res_1 and res_2:
        new_cand = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_count, word_tar_count, ent_sou[0], ent_tar[0])
    if res_1 ^ res_2:
        none_ent = "none"
        if res_1:
            new_cand = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_count, word_tar_count, ent_sou[0], none_ent)
        if res_2:
            new_cand = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_count, word_tar_count, none_ent, ent_tar[0])

    return (res_1 or res_2), new_cand


def add_entity_ner_spacy_sou(cand_list, sou_sent, nlp_sp_sou, tar_sent, nlp_sp_tar):
    cand_res = []
    with tqdm(total=len(cand_list)) as pbar:
        for cand in cand_list:
            (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count,
             wiki_tar_count, word_count, word_tar_count) = cand
            res_1 = False
            res_2 = False
            sentence_sou = sou_sent[sent_idx].strip()
            sentence_tar = tar_sent[sent_idx].strip()
            doc_sou = nlp_sp_sou(sentence_sou)
            doc_tar = nlp_sp_tar(sentence_tar)
            entity_sou = []
            entity_tar = []
            for ent in doc_sou.ents:
                if word in ent.text:
                    entity_sou.append(ent.text)
                    res_1 = True
                    break
            for ent in doc_tar.ents:
                if tar_word in ent.text:
                    entity_tar.append(ent.text)
                    res_2 = True
                    break
            if res_1 and res_2:
                cand_new = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                            wiki_sou_count, wiki_tar_count, word_count, word_tar_count, entity_sou[0], entity_tar[0])
                cand_res.append(cand_new)
            if res_1 ^ res_2:
                none_ent = "none"
                if res_1:
                    cand_new = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                                wiki_sou_count, wiki_tar_count, word_count, word_tar_count, entity_sou[0], none_ent)
                    cand_res.append(cand_new)
                if res_2:
                    cand_new = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                                wiki_sou_count, wiki_tar_count, word_count, word_tar_count, none_ent, entity_tar[0])
                    cand_res.append(cand_new)
            if not res_1 and not res_2:
                none_ent = "none"
                cand_new = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                            wiki_sou_count, wiki_tar_count, word_count, word_tar_count, none_ent, none_ent)
                cand_res.append(cand_new)
            pbar.update(1)
    return cand_res


def check_ner_sou_flair(cand, sou_sent, tagger_sou, tar_sent, tagger_tar):
    res_sou = False
    res_tar = False
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_count, word_tar_count) = cand
    sentence_sou = sou_sent[sent_idx].strip().split()
    sentence_tar = tar_sent[sent_idx].strip().split()
    sen_sou = Sentence(sentence_sou)
    sen_tar = Sentence(sentence_tar)
    tagger_sou.predict(sen_sou)
    tagger_tar.predict(sen_tar)
    ent_sou = []
    ent_tar = []
    new_cand = None
    for entity in sen_sou.get_spans('ner'):
        if word in entity.text:
            res_sou = True
            ent_sou.append(entity.text)
            break

    for entity in sen_tar.get_spans('ner'):
        if tar_word in entity.text:
            res_tar = True
            ent_tar.append(entity.text)
            break
    if res_sou and res_tar:
        new_cand = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_count, word_tar_count, ent_sou[0], ent_tar[0])
    if res_sou ^ res_tar:
        none_ent = "none"
        if res_sou:
            new_cand = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_count, word_tar_count, ent_sou[0], none_ent)
        if res_tar:
            new_cand = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count, wiki_tar_count, word_count, word_tar_count, none_ent, ent_tar[0])

    return (res_sou or res_tar), new_cand


def add_entity_to_cand(cand, entity_sou, entity_tar):
    (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count,
     wiki_tar_count, word_count, word_tar_count) = cand
    if entity_sou is None:
        entity_sou = "none"
    if entity_tar is None:
        entity_tar = "none"
    new_cand = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                wiki_sou_count, wiki_tar_count, word_count, word_tar_count, entity_sou, entity_tar)
    return new_cand


def add_entity_ner_flair_sou(cand_list, sou_sent, tagger_sou, tar_sent, tagger_tar):
    cand_res = []
    with tqdm(total=len(cand_list)) as pbar:
        for cand in cand_list:
            (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count,
             wiki_tar_count, word_count, word_tar_count) = cand
            res_1 = False
            res_2 = False
            sentence_sou = sou_sent[sent_idx].strip()
            sentence_tar = tar_sent[sent_idx].strip()
            sen_sou = Sentence(sentence_sou)
            sen_tar = Sentence(sentence_tar)
            tagger_sou.predict(sen_sou)
            tagger_tar.predict(sen_tar)
            entity_sou = []
            entity_tar = []
            for entity in sen_sou.get_spans('ner'):
                if word in entity.text:
                    res_1 = True
                    entity_sou.append(entity.text)
                    break

            for entity in sen_tar.get_spans('ner'):
                if tar_word in entity.text:
                    res_2 = True
                    entity_tar.append(entity.text)
                    break
                    
            if res_1 and res_2:
                cand_new = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                            wiki_sou_count, wiki_tar_count, word_count, word_tar_count, entity_sou[0], entity_tar[0])
                cand_res.append(cand_new)
            if res_1 ^ res_2:
                none_ent = "none"
                if res_1:
                    cand_new = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                                wiki_sou_count, wiki_tar_count, word_count, word_tar_count, entity_sou[0], none_ent)
                    cand_res.append(cand_new)
                if res_2:
                    cand_new = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                                wiki_sou_count, wiki_tar_count, word_count, word_tar_count, none_ent, entity_tar[0])
                    cand_res.append(cand_new)
            if not res_1 and not res_2:
                none_ent = "none"
                cand_new = (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1,
                            wiki_sou_count, wiki_tar_count, word_count, word_tar_count, none_ent, none_ent)
                cand_res.append(cand_new)
            pbar.update(1)
    return cand_res


def check_ner_tar_stan(cand, tar_sent, nlp_stan):
    res = False
    (_, word, sou_word, sent_index, _, _, _, _, _, _, _) = cand
    sentence = tar_sent[sent_index].strip()
    doc = nlp_stan(sentence)
    for ent in doc.ents:
        if word in ent.text:
            res = True
            break
    return res


def check_ner_tar_spacy(cand, tar_sent, nlp_sp):
    res = False
    (_, word, sou_word, sent_index, _, _, _, _, _, _, _) = cand
    sentence = tar_sent[sent_index].strip()
    doc = nlp_sp(sentence)
    for ent in doc.ents:
        if word in ent.text:
            res = True
            break
    return res


def check_ner_tar_flair(cand, sou_sent, tagger_tar):
    res = False
    (_, word, sou_word, sent_index, _, _, _, _, _, _, _) = cand
    sentence = sou_sent[sent_index].strip()
    sen_input = Sentence(sentence)
    tagger_tar.predict(sen_input)
    for entity in sen_input.get_spans('ner'):
        if word in entity.text:
            res = True
            break
    return res


def check_ner_flair_stan(cand, sou_sent, flair_tagger_sou, tar_sent, nlp_stan_tar):
    res_1 = False
    res_2 = False
    (word, tar_word, sent_idx, _, _, _, _, _, _, _, _, _) = cand
    sentence_sou = sou_sent[sent_idx].strip()
    sentence_tar = tar_sent[sent_idx].strip()

    sen_sou = Sentence(sentence_sou)
    flair_tagger_sou.predict(sen_sou)
    for entity in sen_sou.get_spans('ner'):
        if word in entity.text:
            res_1 = True
            break
    doc_tar = nlp_stan_tar(sentence_tar)
    for ent in doc_tar.ents:
        if tar_word in ent.text:
            res_2 = True
            break
    return res_1 or res_2


def check_ner_flair_spacy(cand, sou_sent, flair_tagger_sou, tar_sent, nlp_tar_sp):
    res_1 = False
    res_2 = False
    (word, tar_word, sent_idx, _, _, _, _, _, _, _, _, _) = cand
    sentence_sou = sou_sent[sent_idx].strip()
    sentence_tar = tar_sent[sent_idx].strip()

    sen_sou = Sentence(sentence_sou)
    flair_tagger_sou.predict(sen_sou)
    for entity in sen_sou.get_spans('ner'):
        if word in entity.text:
            res_1 = True
            break

    doc_tar = nlp_tar_sp(sentence_tar)
    for ent in doc_tar.ents:
        if tar_word in ent.text:
            res_2 = True
            break
    return res_1 or res_2


def check_ner_stan_spacy(cand, sou_sent, nlp_stan_sou, tar_sent, nlp_sp_tar):
    res_1 = False
    res_2 = False
    (word, tar_word, sent_idx, _, _, _, _, _, _, _, _, _) = cand
    sentence_sou = sou_sent[sent_idx].strip()
    sentence_tar = tar_sent[sent_idx].strip()

    doc_sou = nlp_stan_sou(sentence_sou)
    for ent in doc_sou.ents:
        if word in ent.text:
            res_1 = True
            break

    doc_tar = nlp_sp_tar(sentence_tar)
    for ent in doc_tar.ents:
        if tar_word in ent.text:
            res_2 = True
            break
    return res_1 or res_2


def check_ner_stan_flair(cand, sou_sent, nlp_stan_sou, tar_sent, flair_tagger_tar):
    res_1 = False
    res_2 = False
    (word, tar_word, sent_idx, _, _, _, _, _, _, _, _, _) = cand
    sentence_sou = sou_sent[sent_idx].strip()
    sentence_tar = tar_sent[sent_idx].strip()

    doc_sou = nlp_stan_sou(sentence_sou)
    for ent in doc_sou.ents:
        if word in ent.text:
            res_1 = True
            break

    sen_tar = Sentence(sentence_tar)
    flair_tagger_tar.predict(sen_tar)

    for entity in sen_tar.get_spans('ner'):
        if tar_word in entity.text:
            res_2 = True
            break
    return res_1 or res_2


def check_ner_spacy_stan(cand, sou_sent, nlp_sp_sou, tar_sent, nlp_stan_tar):
    res_1 = False
    res_2 = False
    (word, tar_word, sent_idx, _, _, _, _, _, _, _, _, _) = cand
    sentence_sou = sou_sent[sent_idx].strip()
    sentence_tar = tar_sent[sent_idx].strip()
    doc_sou = nlp_sp_sou(sentence_sou)
    for ent in doc_sou.ents:
        if word in ent.text:
            res_1 = True
            break
    doc_tar = nlp_stan_tar(sentence_tar)
    for ent in doc_tar.ents:
        if tar_word in ent.text:
            res_2 = True
            break
    return res_1 or res_2


def check_ner_spacy_flair(cand, sou_sent, nlp_sp_sou, tar_sent, flair_tagger_tar):
    res_1 = False
    res_2 = False
    (word, tar_word, sent_idx, _, _, _, _, _, _, _, _, _) = cand
    sentence_sou = sou_sent[sent_idx].strip()
    sentence_tar = tar_sent[sent_idx].strip()
    doc_sou = nlp_sp_sou(sentence_sou)
    for ent in doc_sou.ents:
        if word in ent.text:
            res_1 = True
            break

    sen_tar = Sentence(sentence_tar)
    flair_tagger_tar.predict(sen_tar)

    for entity in sen_tar.get_spans('ner'):
        if tar_word in entity.text:
            res_2 = True
            break

    return res_1 or res_2


def save_cand_for_check_sou(cand_list, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for cand_check in cand_list:
        (word, tar_word, sent_index, align_index, sou_idx_1, tar_idx_1, sou_idx_2, tar_idx_2,
         sou_word_freq, tar_word_freq, en_freq, de_freq) = cand_check
        output = word + " " + str(sent_index) + " " + str(sou_idx_1) + "\n"
        w_file.write(output)
    w_file.close()


def save_cand_for_check_tar(cand_list, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for cand_check in cand_list:
        (word, sou_word, sent_index, align_index, tar_idx_1, sou_idx_1, tar_idx_2, sou_idx_2,
         tar_word_freq, sou_word_freq, de_freq, en_freq) = cand_check
        output = word + " " + str(sent_index) + " " + str(tar_idx_1) + "\n"
        w_file.write(output)
    w_file.close()


def save_cand_for_final_sou(cand_list, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for cand_final in cand_list:
        (word, tar_word, sent_index, align_index, sou_idx_1, tar_idx_1, sou_idx_2, tar_idx_2,
         sou_word_freq, tar_word_freq, en_freq, de_freq) = cand_final
        output = word + " " + tar_word + " " + str(sent_index) + " " + str(align_index) + " " \
                 + str(sou_idx_1) + " " + str(tar_idx_1) + " " + str(sou_idx_2) + " " + str(tar_idx_2) + " " \
                 + str(sou_word_freq) + " " + str(tar_word_freq) + " " + str(en_freq) + " " + str(de_freq) + "\n"
        w_file.write(output)
    w_file.close()


def save_cand_for_final_tar(cand_list, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for cand_final in cand_list:
        (word, sou_word, sent_index, align_index, tar_idx_1, sou_idx_1, tar_idx_2, sou_idx_2,
         tar_word_freq, sou_word_freq, de_freq, en_freq) = cand_final
        output = word + " " + sou_word + " " + str(sent_index) + " " + str(align_index) + " " \
                 + str(tar_idx_1) + " " + str(sou_idx_1) + " " + str(tar_idx_2) + " " + str(sou_idx_2) + " " \
                 + str(tar_word_freq) + " " + str(sou_word_freq) + " " + str(de_freq) + " " + str(en_freq) + "\n"
        w_file.write(output)
    w_file.close()


def write_file_sou(file, candidate, en_sentence, de_sentence, sou_count, tar_count, threshold_num):
    for word_freq in range(1, threshold_num + 1):
        file.write("\n")
        file.write("threshold_num: " + str(word_freq) + "\n")
        file.write("\n")
        for cand in candidate:
            (sou_word_f, word, tar_word, sent_index, word_pair_index, sou_idx_1, tar_idx_1, sou_idx_2, tar_idx_2, en_freq, de_freq) \
                = cand
            if sou_word_f == word_freq:
                file.write("\n")
                sou_word_freq = sou_count[word]
                tar_word_freq = tar_count[tar_word]
                output = \
                    word + ":  |align: " + \
                    str((sou_idx_1, tar_idx_1)) + " " + str((sou_idx_2, tar_idx_2)) \
                    + "  |word_frequency: " + "sou: " + str(sou_word_freq) + " - tar: " + str(tar_word_freq) \
                    + "  |wiki_frequency: " + "sou: " + str(en_freq) + " - tar: " + str(de_freq) \
                    + "  |sentence index: " + str(sent_index + 1) + "   |   " \
                    + en_sentence[sent_index].strip()+" ||| " + de_sentence[sent_index].strip() + "\n"
                file.write(output)


def write_file_tar(file, candidate, de_sentence, en_sentence, tar_count, sou_count, threshold_num):
    for word_freq in range(1, threshold_num + 1):
        file.write("\n")
        file.write("threshold_num: " + str(word_freq) + "\n")
        file.write("\n")
        for cand in candidate:
            (tar_word_f, word, sou_word, sent_index, word_pair_index, tar_idx_1, sou_idx_1, tar_idx_2, sou_idx_2, de_freq, en_freq) \
                = cand
            if tar_word_f == word_freq:
                file.write("\n")
                tar_word_freq = tar_count[word]
                sou_word_freq = sou_count[sou_word]
                output = \
                    word + ":  |align: " + \
                    str((tar_idx_1, sou_idx_1)) + " " + str((tar_idx_2, sou_idx_2)) \
                    + "  |word_frequency: " + "tar: " + str(tar_word_freq) + " - sou: " + str(sou_word_freq) \
                    + "  |wiki_frequency: " + "tar: " + str(de_freq) + " - sou: " + str(en_freq) \
                    + "  |sentence index: " + str(sent_index + 1) + "   |   " \
                    + de_sentence[sent_index].strip()+" ||| "+en_sentence[sent_index].strip() + "\n"
                file.write(output)


def write_check_cand_sou(cand, check_file):
    (word, _, sent_index, _, sou_idx_1, _, _, _, _, _, _, _) = cand
    output = word+" "+str(sent_index)+" "+str(sou_idx_1)+"\n"
    check_file.write(output)


def write_check_cand_tar(cand, check_file):
    (word, _, sent_index, _, tar_idx_1, _, _, _, _, _, _, _) = cand
    output = word+" "+str(sent_index)+" "+str(tar_idx_1)+"\n"
    check_file.write(output)


def get_nums_for_filter_sou(cand_list, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for th_num in range(threshold_num):
        sent_list = set()
        sent_list.clear()
        for (_, _, sent_idx, _, _, _, _, _, sou_word_freq, _, _, _) in cand_list:
            if sou_word_freq == th_num + 1:
                sent_list.add(sent_idx)
        nums_cand_sep = len(sent_list)
        w_file.write("word frequency " + str(th_num + 1) + ": " + str(nums_cand_sep) + "\n")
    for (_, _, sent_idx, _, _, _, _, _, _, _, _, _) in cand_list:
        sent_list_all.add(sent_idx)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()


def get_nums_for_filter_tar(cand_list, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for th_num in range(threshold_num):
        sent_list = set()
        sent_list.clear()
        for (_, _, sent_idx, _, _, _, _, _, tar_word_freq, _, _, _) in cand_list:
            if tar_word_freq == th_num + 1:
                sent_list.add(sent_idx)
        nums_cand_sep = len(sent_list)
        w_file.write("word frequency " + str(th_num + 1) + ": " + str(nums_cand_sep) + "\n")
    for (_, _, sent_idx, _, _, _, _, _, _, _, _, _) in cand_list:
        sent_list_all.add(sent_idx)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()


def get_nums_for_filter_sou_all(cand_list, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    sent_list_all.clear()
    for (_, _, sent_idx, _, _, _, _, _, _, _, _, _) in cand_list:
        sent_list_all.add(sent_idx)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()


def get_nums_for_filter_tar_all(cand_list, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    sent_list_all.clear()
    for (_, _, sent_idx, _, _, _, _, _, _, _, _, _) in cand_list:
        sent_list_all.add(sent_idx)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()


if __name__ == '__main__':
    road = "D:\\thesis_data\\cc_Matrix\\en_zh\\"
    ner_name = "spacy_15000_15000"
    total_num_ner = 0
    total_nums_file_ner = road + "total_num_desktop\\9_filter_ner_" + ner_name + ".txt"
    num_f_t_ner = open(total_nums_file_ner, 'w', encoding='utf-8')
    
    
    #tagger_sou = SequenceTagger.load('flair/ner-english-large')
    #tagger_tar = SequenceTagger.load('flair/ner-german-large')
    spacy_nlp_sou = spacy.load("en_core_web_lg")
    spacy_nlp_tar = spacy.load("zh_core_web_lg")
    #stan_nlp_sou = stanza.Pipeline(lang='en', processors='tokenize,ner,mwt', verbose=False, tokenize_pretokenized=True)
    #stan_nlp_tar = stanza.Pipeline(lang='zh', processors='tokenize,ner', verbose=False, tokenize_pretokenized=True)
    #ner_han_tar = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
    for idx in range(1, 6):
        time_start = time.time()
        file_index = idx
        #threshold_num_tar = 200
        #threshold_num_sou = 200
        sou_road = road + str(idx) + "\\sou\\"
        res_road = road + str(idx) + "\\res\\"

        sou_word_file = sou_road + "en_token_1000k_" + str(idx) + ".txt"
        sou_sentences = get_sentences_res(sou_word_file)

        tar_word_file = sou_road + "zh_token_1000k_" + str(idx) + ".txt"
        tar_sentences = get_sentences_res(tar_word_file)

        cand_road = res_road + "cand\\"
        check_road = res_road + "check\\"
        nums_road = res_road + "nums\\"
        final_res_road = res_road + "final_res\\"

        cand_ner_sou_file = cand_road + "cand_7_before_count_in_file_15000_15000.txt"
        #cand_ner_tar_file = cand_road + "tar_cand.txt"

        cand_ner_sou = uf.get_cand_count_in_file_sou_from_file(cand_ner_sou_file)
        #cand_ner_tar = get_cand_from_file_tar(cand_ner_tar_file)

        cand_sou_after_ner = []
        #cand_tar_after_ner = []

        with tqdm(total=len(cand_ner_sou)) as pbar:
            for ele in cand_ner_sou:
                #check_res_1 = check_ner_stan_flair(ele, sou_sentences, stan_nlp_sou, tar_sentences, tagger_tar)
                #check_res_1 = check_ner_sou_stan(ele, sou_sentences,stan_nlp_sou, tar_sentences,stan_nlp_tar)
                #check_res_1, new_ele = check_ner_sou_spacy(ele, sou_sentences, spacy_nlp_sou, tar_sentences, spacy_nlp_tar)
                #check_res_1, new_ele = check_ner_sou_flair(ele, sou_sentences, tagger_sou, tar_sentences, tagger_tar)
                #check_res = check_ner_sou_from_tar_stan(ele, de_sentences, stan_nlp_tar)
                #check_res = check_ner_sou_from_tar_spacy(ele, de_sentences, spacy_nlp_tar)
                #check_res = check_ner_sou_from_tar_flair(ele, de_sentences, tagger_tar)
                #check_res_sou_f, entity_sou_f = check_ner_flair_sou(ele, sou_sentences, tagger_sou)
                #check_res_tar_f, entity_tar_f = check_ner_flair_tar(ele, tar_sentences, tagger_tar)
                #check_res_sou_st, entity_sou_st = check_ner_stan_sou(ele, sou_sentences, stan_nlp_sou)
                #check_res_tar_st, entity_tar_st = check_ner_stan_tar(ele, tar_sentences, stan_nlp_tar)
                check_res_sou_sp, entity_sou_sp = check_ner_spacy_sou(ele, sou_sentences, spacy_nlp_sou)
                check_res_tar_sp, entity_tar_sp = check_ner_spacy_tar(ele, tar_sentences, spacy_nlp_tar)
                #check_res_tar_h, entity_tar_h = check_ner_hanlp_tar(ele,tar_sentences,ner_han_tar)
                if check_res_sou_sp or check_res_tar_sp:
                    new_ele = add_entity_to_cand(ele, entity_sou_sp, entity_tar_sp)
                    cand_sou_after_ner.append(new_ele)
                pbar.update(1)
        #new_cand_sou_after_ner = add_entity_ner_spacy_sou(cand_sou_after_ner, sou_sentences, spacy_nlp_sou,
        #                                                  tar_sentences, spacy_nlp_tar)
        # save nums
        print("for nums write: begin\n")
        sou_nums_ner_road = nums_road + "9_filter_ner_"+ner_name+".txt"
        cand_num_ner = uf.get_nums_for_ner_filter_sou(cand_sou_after_ner, sou_nums_ner_road)
        total_num_ner = total_num_ner + cand_num_ner
        print("for nums write: end\n")
        
        # save check cand
        print("for cand for check save: begin\n")
        # for save cand for next filter
        sou_check_p = check_road + "check_after_ner_"+ner_name+".txt"
        uf.save_cand_check_ner_filter_sou(cand_sou_after_ner, sou_check_p)
        print("for cand for check save: end\n")
       
        print("for cand for next filter save: begin\n")
        sou_cand_p = cand_road + "cand_9_ner_"+ner_name+".txt"
        uf.save_cand_ner_sou_in_file(cand_sou_after_ner, sou_cand_p)
        print("for cand for next filter save: end\n")

        print("for cand for final save: begin\n")
        # for save cand for next filter
        sou_final_p = final_res_road + "cand_with_sent_after_ner_"+ner_name+".txt"
        uf.save_sent_cand_sou_ner(cand_sou_after_ner, sou_sentences, tar_sentences, sou_final_p)
        print("for cand for final save: end\n")

        time_end = time.time()
        print('time cost: ', time_end - time_start, 's')
    num_f_t_ner.write("total: " + str(total_num_ner) + "\n")
    num_f_t_ner.close()


