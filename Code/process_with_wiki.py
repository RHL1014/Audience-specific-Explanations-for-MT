from tqdm import tqdm
import time
import universal_func as uf
import nltk
from nltk.stem import *
import opencc


def get_wiki_title(in_file):
    wiki_title_dict = {}
    wiki_title_dict_lower = {}
    with open(in_file, 'r', encoding='utf-8') as title_f:
        for line in title_f:
            title = line.strip().split('_')
            title_1 = " ".join(title)
            wiki_title_dict[title_1] = 1
            title_1_low = title_1.lower()
            wiki_title_dict_lower[title_1_low] = 1
    return wiki_title_dict, wiki_title_dict_lower


def get_wiki_title_zh(in_file):
    wiki_title_dict = {}
    wiki_title_dict_lower = {}
    converter = opencc.OpenCC('t2s.json')
    with open(in_file, 'r', encoding='utf-8') as title_f:
        for line in title_f:
            title = line.strip().split('_')
            title_1 = " ".join(title)
            new_title_1 = converter.convert(title_1)
            wiki_title_dict[new_title_1] = 1
            title_1_low = new_title_1.lower()
            wiki_title_dict_lower[title_1_low] = 1
    return wiki_title_dict, wiki_title_dict_lower


def get_wiki_parallel_title(in_file):
    wiki_sou_title_dict = {}
    wiki_tar_title_dict = {}
    wiki_sou_title_dict_lower = {}
    wiki_tar_title_dict_lower = {}
    with open(in_file, 'r', encoding='utf-8') as titles:
        for line in titles:
            title_b = line.strip().split(' ||| ')
            title_tar = title_b[0].strip()
            title_sou = title_b[1].strip()
            title_tar_low = title_tar.lower()
            title_sou_low = title_sou.lower()
            wiki_sou_title_dict[title_sou] = title_tar
            wiki_tar_title_dict[title_tar] = title_sou
            wiki_sou_title_dict_lower[title_sou_low] = title_tar
            wiki_tar_title_dict_lower[title_tar_low] = title_sou
    return wiki_sou_title_dict, wiki_tar_title_dict, wiki_sou_title_dict_lower, wiki_tar_title_dict_lower


def get_wiki_parallel_title_zh(in_file):
    wiki_sou_title_dict = {}
    wiki_tar_title_dict = {}
    wiki_sou_title_dict_lower = {}
    wiki_tar_title_dict_lower = {}
    converter = opencc.OpenCC('t2s.json')
    with open(in_file, 'r', encoding='utf-8') as titles:
        for line in titles:
            title_b = line.strip().split(' ||| ')
            title_tar = title_b[0].strip()
            title_tar_new = converter.convert(title_tar)
            title_sou = title_b[1].strip()
            title_tar_low = title_tar_new.lower()
            title_sou_low = title_sou.lower()
            wiki_sou_title_dict[title_sou] = title_tar_new
            wiki_tar_title_dict[title_tar_new] = title_sou
            wiki_sou_title_dict_lower[title_sou_low] = title_tar_new
            wiki_tar_title_dict_lower[title_tar_low] = title_sou
    return wiki_sou_title_dict, wiki_tar_title_dict, wiki_sou_title_dict_lower, wiki_tar_title_dict_lower


def get_wiki_article_size(in_file):
    wiki_article_size_dict = {}
    with open(in_file, 'r', encoding='utf-8') as title_f:
        for line in title_f:
            title_size = line.strip().split(' ||| ')
            if len(title_size) != 2:
                continue
            title = title_size[0].strip()
            size = int(title_size[1].strip())
            wiki_article_size_dict[title] = size
    return wiki_article_size_dict


def get_wiki_article_size_zh(in_file):
    wiki_article_size_dict = {}
    converter = opencc.OpenCC('t2s.json')
    with open(in_file, 'r', encoding='utf-8') as title_f:
        for line in title_f:
            title_size = line.strip().split(' ||| ')
            if len(title_size) != 2:
                continue
            title = title_size[0].strip()
            title_new = converter.convert(title)
            size = int(title_size[1].strip())
            wiki_article_size_dict[title_new] = size
    return wiki_article_size_dict

    
def get_cand(in_file):
    cand_sou = []
    sou_cand_file = open(in_file, 'r', encoding='utf-8')
    sou_cand = sou_cand_file.readlines()
    for line in sou_cand:
        res_each_align = line.strip().split('|||')
        ner_res = res_each_align[1].strip()
        cand_res = res_each_align[0].strip().split()
        word = cand_res[0]
        sentence_idx = int(cand_res[1])
        word_idx = int(cand_res[2])
        sou_word_freq = int(cand_res[3])
        sou_wiki_freq = int(cand_res[4])
        new_ele_align = (word, sentence_idx, word_idx, sou_word_freq, sou_wiki_freq, ner_res)
        cand_sou.append(new_ele_align)
    sou_cand_file.close()
    return cand_sou


def select_cand_with_wiki_title(wiki_title_sou: dict, wiki_title_sou_low: dict, cand_list: list):
    res_list = []
    for cand_wiki_check in cand_list:
        (_, _, _, _, _, _, _, _, _, _, _, _, entity_sou, entity_tar) = cand_wiki_check
        ner_sou = entity_sou.strip()
        #ner_tar = entity_tar.strip()
        sou_res = False
        #tar_res = False
        if ner_sou != 'none':
            ner_res_sou = " ".join(ner_sou.split())
            if ner_res_sou in wiki_title_sou:
                sou_res = True
            else:
                stem_1 = SnowballStemmer("english")
                stem_ner = stem_1.stem(ner_res_sou)
                if stem_ner in wiki_title_sou_low:
                    sou_res = True
        if sou_res:
            res_list.append(cand_wiki_check)
    return res_list


def check_cand_with_para_wiki_title(wiki_title_sou: dict, wiki_para_title_sou: dict, wiki_title_sou_low: dict, wiki_para_title_sou_low: dict, cand_list: list):
    res_list_not_para_title = []
    res_list_para_title = []
    for cand_wiki_check in cand_list:
        (_, _, _, _, _, _, _, _, _, _, _, _, entity_sou, entity_tar) = cand_wiki_check
        ner_sou = entity_sou.strip().split()
        ner_res_sou = " ".join(ner_sou)
        stem_1 = SnowballStemmer("english")
        stem_ner = stem_1.stem(ner_res_sou)
        if ner_res_sou in wiki_title_sou:
            if ner_res_sou not in wiki_para_title_sou:
                res_list_not_para_title.append(cand_wiki_check)
            else:
                res_list_para_title.append(cand_wiki_check)
        else:
            if stem_ner not in wiki_para_title_sou_low:
                res_list_not_para_title.append(cand_wiki_check)
            else:
                res_list_para_title.append(cand_wiki_check)
    return res_list_not_para_title, res_list_para_title


def check_cand_with_para_wiki_title_target(wiki_para_title_sou: dict, wiki_para_title_sou_low: dict, cand_list_in_para: list):
    res_list_same = []
    res_list_not_same = []
    for cand_wiki_check in cand_list_in_para:
        (_, _, _, _, _, _, _, _, _, _, _, _, entity_sou, entity_tar) = cand_wiki_check
        if entity_tar == "none":
            continue
        ner_sou = entity_sou.strip().split()
        ner_tar = entity_tar.strip().split()
        ner_res_sou = " ".join(ner_sou)
        ner_res_tar = " ".join(ner_tar)
        stem_1 = SnowballStemmer("english")
        stem_ner_sou = stem_1.stem(ner_res_sou)
        stem_2 = SnowballStemmer("german")
        stem_ner_tar = stem_2.stem(ner_res_tar)
        if ner_res_sou in wiki_para_title_sou:
            title_tar = wiki_para_title_sou[ner_res_sou]
            if ner_res_tar == title_tar:
                res_list_same.append(cand_wiki_check)
            else:
                if stem_ner_tar == title_tar.lower():
                    res_list_same.append(cand_wiki_check)
                else:
                    res_list_not_same.append(cand_wiki_check)
        else:
            title_tar = wiki_para_title_sou_low[stem_ner_sou]
            if ner_res_tar == title_tar:
                res_list_same.append(cand_wiki_check)
            else:
                if stem_ner_tar == title_tar.lower():
                    res_list_same.append(cand_wiki_check)
                else:
                    res_list_not_same.append(cand_wiki_check)
    return res_list_same, res_list_not_same


def check_cand_with_para_wiki_title_target_zh(wiki_para_title_sou: dict, wiki_para_title_sou_low: dict, cand_list_in_para: list):
    res_list_same = []
    res_list_not_same = []
    for cand_wiki_check in cand_list_in_para:
        (_, _, _, _, _, _, _, _, _, _, _, _, entity_sou, entity_tar) = cand_wiki_check
        if entity_tar == "none":
            continue
        ner_sou = entity_sou.strip().split()
        ner_tar = entity_tar.strip().split()
        ner_res_sou = " ".join(ner_sou)
        ner_res_tar = " ".join(ner_tar)
        stem_1 = SnowballStemmer("english")
        stem_ner_sou = stem_1.stem(ner_res_sou)
        stem_2 = SnowballStemmer("english")
        stem_ner_tar = stem_2.stem(ner_res_tar)
        if ner_res_sou in wiki_para_title_sou:
            title_tar = wiki_para_title_sou[ner_res_sou]
            if ner_res_tar == title_tar:
                res_list_same.append(cand_wiki_check)
            else:
                if stem_ner_tar == title_tar.lower():
                    res_list_same.append(cand_wiki_check)
                else:
                    res_list_not_same.append(cand_wiki_check)
        else:
            title_tar = wiki_para_title_sou_low[stem_ner_sou]
            if ner_res_tar == title_tar:
                res_list_same.append(cand_wiki_check)
            else:
                if stem_ner_tar == title_tar.lower():
                    res_list_same.append(cand_wiki_check)
                else:
                    res_list_not_same.append(cand_wiki_check)
    return res_list_same, res_list_not_same


def check_cand_with_para_wiki_title_size(wiki_para_title_sou: dict, wiki_para_title_tar: dict,
                                         wiki_para_title_sou_low: dict, wiki_para_title_tar_low: dict,
                                         wiki_size_sou: dict, wiki_size_tar: dict, res_list_same: list):
    res_list = []
    for cand_wiki_check in res_list_same:
        (_, _, _, _, _, _, _, _, _, _, _, _, entity_sou, entity_tar) = cand_wiki_check
        ner_sou = entity_sou.strip().split()
        ner_tar = entity_tar.strip().split()
        ner_res_sou = " ".join(ner_sou)
        ner_res_tar = " ".join(ner_tar)
        stem_1 = SnowballStemmer("english")
        stem_ner_sou = stem_1.stem(ner_res_sou)
        stem_2 = SnowballStemmer("german")
        stem_ner_tar = stem_2.stem(ner_res_tar)
        if ner_res_sou in wiki_para_title_sou:
            title_sou = ner_res_sou
            title_tar = wiki_para_title_sou[ner_res_sou]
            if title_sou in wiki_size_sou:
                sou_title_art_size = wiki_size_sou[title_sou]
            else:
                sou_title_art_size = 0
            if title_tar in wiki_size_tar:
                tar_title_art_size = wiki_size_tar[title_tar]
            else:
                tar_title_art_size = 0
            if sou_title_art_size > tar_title_art_size:
                res_list.append(cand_wiki_check)
            
        else:
            title_tar = wiki_para_title_sou_low[stem_ner_sou]
            title_sou = wiki_para_title_tar[title_tar]
            if title_sou in wiki_size_sou:
                sou_title_art_size = wiki_size_sou[title_sou]
            else:
                sou_title_art_size = 0
            if title_tar in wiki_size_tar:
                tar_title_art_size = wiki_size_tar[title_tar]
            else:
                tar_title_art_size = 0
            if sou_title_art_size > tar_title_art_size:
                res_list.append(cand_wiki_check)
    return res_list


def check_cand_with_para_wiki_title_size_zh(wiki_para_title_sou: dict, wiki_para_title_tar: dict,
                                         wiki_para_title_sou_low: dict, wiki_para_title_tar_low: dict,
                                         wiki_size_sou: dict, wiki_size_tar: dict, res_list_same: list):
    res_list = []
    for cand_wiki_check in res_list_same:
        (_, _, _, _, _, _, _, _, _, _, _, _, entity_sou, entity_tar) = cand_wiki_check
        ner_sou = entity_sou.strip().split()
        ner_tar = entity_tar.strip().split()
        ner_res_sou = " ".join(ner_sou)
        ner_res_tar = " ".join(ner_tar)
        stem_1 = SnowballStemmer("english")
        stem_ner_sou = stem_1.stem(ner_res_sou)
        if ner_res_sou in wiki_para_title_sou:
            title_sou = ner_res_sou
            title_tar = wiki_para_title_sou[ner_res_sou]
            if title_sou in wiki_size_sou:
                sou_title_art_size = wiki_size_sou[title_sou]
            else:
                sou_title_art_size = 0
            if title_tar in wiki_size_tar:
                tar_title_art_size = wiki_size_tar[title_tar]
            else:
                tar_title_art_size = 0
            if sou_title_art_size > tar_title_art_size:
                res_list.append(cand_wiki_check)
        
        else:
            title_tar = wiki_para_title_sou_low[stem_ner_sou]
            title_sou = wiki_para_title_tar[title_tar]
            if title_sou in wiki_size_sou:
                sou_title_art_size = wiki_size_sou[title_sou]
            else:
                sou_title_art_size = 0
            if title_tar in wiki_size_tar:
                tar_title_art_size = wiki_size_tar[title_tar]
            else:
                tar_title_art_size = 0
            if sou_title_art_size > tar_title_art_size:
                res_list.append(cand_wiki_check)
    return res_list


def check_ner_cand_not_both_title(cand_list):
    res_list = []
    for cand_wiki_check in cand_list:
        (_, _, _, _, _, _, _, _, _, _, _, _, entity_sou, entity_tar) = cand_wiki_check
        ner_sou = entity_sou.strip()
        ner_tar = entity_tar.strip()
        if ner_sou != 'none' and ner_tar != 'none':
            res_list.append(cand_wiki_check)
    return res_list


def check_title_size():
    # how can compare the size? which is base?
    return None


def get_nums_for_filter_sou(cand_list, file_road, threshold_num):
    w_file = open(file_road, 'w', encoding='utf-8')
    sent_list_all = set()
    for th_num in range(threshold_num):
        sent_list = set()
        sent_list.clear()
        for (_, sent_idx, _, sou_word_freq, _, _) in cand_list:
            if sou_word_freq == th_num + 1:
                sent_list.add(sent_idx)
        nums_cand_sep = len(sent_list)
        w_file.write("word frequency " + str(th_num + 1) + ": " + str(nums_cand_sep) + "\n")
    for (_, sent_idx, _, _, _, _) in cand_list:
        sent_list_all.add(sent_idx)
    w_file.write("total: " + str(len(sent_list_all)) + "\n")
    w_file.close()


def save_cand_for_final_sou(cand_list, file_road):
    w_file = open(file_road, 'w', encoding='utf-8')
    for cand_final in cand_list:
        (word, sent_index, word_index, sou_word_freq, en_freq, ner_res) = cand_final
        output = word + " " + str(sent_index) + " " + str(word_index) + " " \
                 + str(sou_word_freq) + " " + str(en_freq) + " ||| " + ner_res + "\n"
        w_file.write(output)
    w_file.close()


def check_ner_with_exp_part(cand_list: list, tar_sents: list[str]):
    res_list = []
    res_list_same = []
    for cand_check in cand_list:
        (word, tar_word, sent_idx, align_idx, word_sou_idx, word_tar_idx, sou_idx_1, tar_idx_1, wiki_sou_count,
         wiki_tar_count, word_count, word_tar_count, entity_sou, entity_tar) = cand_check
        tar_sent = tar_sents[sent_idx]
        tar_sent_list = tar_sent.strip().split()
        if tar_sent_list[word_tar_idx+1] == '(' and tar_sent_list[tar_idx_1-1] == ')':
            start_e = word_tar_idx+2
            end_e = tar_idx_1-1
            entity = " ".join(tar_sent_list[start_e: end_e])
            stem_2 = SnowballStemmer("german")
            stem_entity = stem_2.stem(entity)
            stem_entity_ner = stem_2.stem(entity_tar)
            if entity == entity_tar or stem_entity_ner == stem_entity:
                res_list_same.append(cand_check)
            else:
                res_list.append(cand_check)
        else:
            target_idx = 0
            if tar_sent_list[word_tar_idx + 1] == '(':
                for idx_word in range(word_tar_idx + 2, tar_idx_1+1):
                    if tar_sent_list[idx_word] == ')':
                        target_idx = idx_word
                        break
                entity = " ".join(tar_sent_list[word_tar_idx + 2: target_idx])
                stem_2 = SnowballStemmer("german")
                stem_entity = stem_2.stem(entity)
                stem_entity_ner = stem_2.stem(entity_tar)
                if entity == entity_tar or stem_entity_ner == stem_entity:
                    res_list_same.append(cand_check)
                else:
                    res_list.append(cand_check)
            else:
                res_list.append(cand_check)
    return res_list, res_list_same
        
    
    
    
    
    
if __name__ == '__main__':
    wiki_title_en_file = "D:\\thesis_data\\wiki\\enwiki-20221101-all-titles-in-ns0"
    wiki_title_en, wiki_title_en_low = get_wiki_title(wiki_title_en_file)
    wiki_title_de_file = "D:\\thesis_data\\wiki\\dewiki-20221101-all-titles-in-ns0"
    wiki_title_de, wiki_title_de_low = get_wiki_title(wiki_title_de_file)
    #wiki_title_zh_file = "D:\\thesis_data\\wiki\\zhwiki-20221101-all-titles-in-ns0"
    #wiki_title_zh, wiki_title_zh_low = get_wiki_title_zh(wiki_title_zh_file)
    para_wiki_title_file = "D:\\thesis_data\\wiki\\para_title\\en_de\\de_en_titles.txt"
    wiki_para_en_title, wiki_para_de_title, wiki_para_en_title_low,  wiki_para_de_title_low \
        = get_wiki_parallel_title(para_wiki_title_file)
    #para_wiki_title_file = "D:\\thesis_data\\wiki\\para_title\\en_zh\\zh_en_titles.txt"
    #wiki_para_en_title, wiki_para_zh_title, wiki_para_en_title_low, wiki_para_zh_title_low \
    #    = get_wiki_parallel_title_zh(para_wiki_title_file)
    en_article_size_file = "D:\\thesis_data\\wiki\\wiki_size\\wiki_en_article_size_all.txt"
    en_article_size = get_wiki_article_size(en_article_size_file)
    de_article_size_file = "D:\\thesis_data\\wiki\\wiki_size\\wiki_de_article_size_all.txt"
    de_article_size = get_wiki_article_size(de_article_size_file)
    #zh_article_size_file = "D:\\thesis_data\\wiki\\wiki_size\\wiki_zh_article_size_all.txt"
    #zh_article_size = get_wiki_article_size_zh(zh_article_size_file)
    road = "D:\\thesis_data\\cc_Matrix\\en_de\\"
    ner_name = "flair"
    sou_th = 5000
    tar_th = 5000
    
    total_num_entity_check = 0
    total_num_wiki = 0
    total_num_para_wiki = 0
    total_num_not_para_wiki = 0
    total_num_para_wiki_tar_same = 0
    total_num_para_wiki_tar_not_same = 0
    total_num_para_wiki_size = 0

    total_nums_file_entity_check = road + "total_num_desktop\\9_filter_entity_check_" + ner_name + "_" + str(sou_th) + "_" + str(
        tar_th) + ".txt"
    total_nums_file_wiki = road + "total_num_desktop\\10_filter_wiki_title_" + ner_name+"_"+str(sou_th)+"_"+str(tar_th) + ".txt"
    total_nums_file_para_wiki = road + "total_num_desktop\\11_filter_para_wiki_title_" + ner_name +"_"+str(sou_th)+"_"+str(tar_th)+ ".txt"
    total_nums_file_not_para_wiki = road + "total_num_desktop\\11_filter_not_para_wiki_title_" + ner_name + "_" + str(
        sou_th) + "_" + str(tar_th) + ".txt"
    total_nums_file_para_tar_wiki_same = road + "total_num_desktop\\12_filter_para_tar_wiki_title_same_" + ner_name + "_" + str(
        sou_th) + "_" + str(tar_th) + ".txt"
    total_nums_file_para_tar_wiki_not_same = road + "total_num_desktop\\12_filter_para_tar__wiki_title_not_same_" + ner_name + "_" + str(
        sou_th) + "_" + str(tar_th) + ".txt"
    total_nums_file_para_wiki_size = road + "total_num_desktop\\13_filter_para_wiki_article_size_" + ner_name + "_" + str(
        sou_th) + "_" + str(tar_th) + ".txt"
    
    num_f_t_entity_check = open(total_nums_file_entity_check, 'w', encoding='utf-8')
    num_f_t_wiki = open(total_nums_file_wiki, 'w', encoding='utf-8')
    num_f_t_para_wiki = open(total_nums_file_para_wiki, 'w', encoding='utf-8')
    num_f_t_not_para_wiki = open(total_nums_file_not_para_wiki, 'w', encoding='utf-8')
    num_f_t_para_tar_wiki_same = open(total_nums_file_para_tar_wiki_same, 'w', encoding='utf-8')
    num_f_t_para_tar_wiki_not_same = open(total_nums_file_para_tar_wiki_not_same, 'w', encoding='utf-8')
    num_f_t_para_wiki_size = open(total_nums_file_para_wiki_size, 'w', encoding='utf-8')
    for idx in range(1, 6):
    
        time_start = time.time()
        sou_road = road + str(idx) + "\\sou\\"
        res_road = road + str(idx) + "\\res\\"
        nums_road = res_road + "nums\\"
        check_road = res_road + "check\\"
        cand_road = res_road + "cand\\"
        final_res_road = res_road + "final_res\\"
        cand_file = cand_road + "cand_9_ner_"+ner_name+"_"+str(sou_th)+"_"+str(tar_th)+".txt"

        sou_sentences_file = sou_road + "en_token_1000k_" + str(idx) + ".txt"
        sou_sentences = uf.get_sentences_all_list(sou_sentences_file)
        tar_sentences_file = sou_road + "de_token_1000k_" + str(idx) + ".txt"
        tar_sentences = uf.get_sentences_all_list(tar_sentences_file)
        
        cand = uf.get_cand_ner_sou_from_file(cand_file)
        cand_after_check_entity_with_exp, cand_check_entity_same = check_ner_with_exp_part(cand, tar_sentences)
        
        # both in wiki title
        cand_after_check_title = select_cand_with_wiki_title(wiki_title_en, wiki_title_en_low, cand_after_check_entity_with_exp)
        cand_after_check_para_title_not_in, cand_after_check_para_title_in \
            = check_cand_with_para_wiki_title(wiki_title_en, wiki_para_en_title,
                                              wiki_title_en_low, wiki_para_en_title_low,
                                              cand_after_check_title)
        cand_wiki_para_tar_same, cand_wiki_para_tar_not_same \
            = check_cand_with_para_wiki_title_target(wiki_para_en_title, wiki_para_en_title_low,
                                                     cand_after_check_para_title_in)

        cand_wiki_article_size = check_cand_with_para_wiki_title_size(wiki_para_en_title, wiki_para_de_title,
                                                                      wiki_para_en_title_low, wiki_para_de_title_low,
                                                                      en_article_size, de_article_size,
                                                                      cand_wiki_para_tar_same)
    
        # save nums
        print("for nums write: begin\n")

        sou_nums_check_entity_with_exp_road = nums_road + "9_filter_check_entity_with_exp_" + ner_name + "_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        cand_9_num = uf.get_nums_for_wiki_title_filter_sou(cand_after_check_entity_with_exp, sou_nums_check_entity_with_exp_road)
        total_num_entity_check = total_num_entity_check + cand_9_num
        
        sou_nums_wiki_title_road = nums_road + "10_filter_both_wiki_title_" + ner_name +"_"+str(sou_th)+"_"+str(tar_th)+ ".txt"
        cand_10_num = uf.get_nums_for_wiki_title_filter_sou(cand_after_check_title, sou_nums_wiki_title_road)
        total_num_wiki = total_num_wiki + cand_10_num
        
        sou_nums_wiki_para_title_road = nums_road + "11_filter_para_wiki_title_" + ner_name + "_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        cand_11_num_1 = uf.get_nums_for_wiki_title_filter_sou(cand_after_check_para_title_in, sou_nums_wiki_para_title_road)
        total_num_para_wiki = total_num_para_wiki + cand_11_num_1
    
        sou_nums_wiki_not_para_title_road = nums_road + "11_filter_not_para_wiki_title_" + ner_name + \
                                        "_" + str(sou_th) + "_" + str(tar_th) + ".txt"
        cand_11_num_2 = uf.get_nums_for_wiki_title_filter_sou(cand_after_check_para_title_not_in,
                                                            sou_nums_wiki_not_para_title_road)
        total_num_not_para_wiki = total_num_not_para_wiki + cand_11_num_2
    
        sou_nums_wiki_para_tar_title_same_road = nums_road + "12_filter_para_wiki_tar_title_same_" + ner_name \
                                                 + "_" + str(sou_th) + "_" + str(tar_th) + ".txt"
        
        cand_12_num_1 = uf.get_nums_for_wiki_title_filter_sou(cand_wiki_para_tar_same, sou_nums_wiki_para_tar_title_same_road)
        total_num_para_wiki_tar_same = total_num_para_wiki_tar_same + cand_12_num_1
    
        sou_nums_wiki_para_tar_title_not_same_road = nums_road + "12_filter_para_wiki_tar_title_not_same_" + ner_name \
                                                     + "_" + str(sou_th) + "_" + str(tar_th) + ".txt"
        cand_12_num_2 = uf.get_nums_for_wiki_title_filter_sou(cand_wiki_para_tar_not_same,
                                                            sou_nums_wiki_para_tar_title_not_same_road)
        total_num_para_wiki_tar_not_same = total_num_para_wiki_tar_not_same + cand_12_num_2
    
        sou_nums_wiki_para_article_size_road = nums_road + "13_filter_para_wiki_article_size_" + ner_name \
                                                     + "_" + str(sou_th) + "_" + str(tar_th) + ".txt"
        cand_13_num = uf.get_nums_for_wiki_title_filter_sou(cand_wiki_article_size,
                                                              sou_nums_wiki_para_article_size_road)
        total_num_para_wiki_size = total_num_para_wiki_size + cand_13_num
        print("for nums write: end\n")
    
        # save check cand
        print("for cand for check save: begin\n")
        # for save cand for next filter
        sou_check_entity_check = check_road + "check_after_entity_check_" + ner_name + "_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        uf.save_cand_check_wiki_title_filter_sou(cand_after_check_entity_with_exp, sou_check_entity_check)
        
        sou_check_wiki_title = check_road + "check_after_both_wiki_title_" + ner_name +"_"+str(sou_th)+"_"+str(tar_th)+ ".txt"
        uf.save_cand_check_wiki_title_filter_sou(cand_after_check_title, sou_check_wiki_title)
    
        sou_check_para_wiki_title = check_road + "check_after_para_wiki_title_" + ner_name + "_" + \
                                    str(sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_cand_check_wiki_title_filter_sou(cand_after_check_para_title_in, sou_check_para_wiki_title)
    
        sou_check_not_para_wiki_title = check_road + "check_after_not_para_wiki_title_" + ner_name + "_" + \
                                    str(sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_cand_check_wiki_title_filter_sou(cand_after_check_para_title_not_in, sou_check_not_para_wiki_title)
        
        sou_check_para_wiki_tar_title_same = check_road + "check_after_para_wiki_tar_title_same_" + ner_name + "_" + \
                                             str(sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_cand_check_wiki_title_filter_sou(cand_wiki_para_tar_same, sou_check_para_wiki_tar_title_same)
        
        sou_check_para_wiki_tar_title_not_same = check_road + "check_after_para_wiki_tar_title_not_same_" + ner_name + "_" + \
                                                 str(sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_cand_check_wiki_title_filter_sou(cand_wiki_para_tar_not_same, sou_check_para_wiki_tar_title_not_same)
    
        sou_check_para_wiki_article_size = check_road + "check_after_para_wiki_article_size_" + ner_name + "_" + \
                                                 str(sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_cand_check_wiki_title_filter_sou(cand_wiki_article_size, sou_check_para_wiki_article_size)
        print("for cand for check save: end\n")
    
        print("for cand for next step save: begin\n")
        # for save cand for next filter
        sou_cand_entity_check = cand_road + "cand_9_entity_check_" + ner_name + "_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        uf.save_cand_wiki_title_sou_in_file(cand_after_check_entity_with_exp, sou_cand_entity_check)
        
        sou_cand_wiki_title = cand_road + "cand_10_both_wiki_title_" + ner_name + "_"+str(sou_th)+"_"+str(tar_th)+".txt"
        uf.save_cand_wiki_title_sou_in_file(cand_after_check_title, sou_cand_wiki_title)
    
        sou_cand_para_wiki_title = cand_road + "cand_11_para_wiki_title_" + ner_name + "_" + str(sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_cand_wiki_title_sou_in_file(cand_after_check_para_title_in, sou_cand_para_wiki_title)
    
        sou_cand_not_para_wiki_title = cand_road + "cand_11_not_para_wiki_title_" + ner_name + "_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        uf.save_cand_wiki_title_sou_in_file(cand_after_check_para_title_not_in, sou_cand_not_para_wiki_title)
    
        sou_cand_para_wiki_tar_title_same = cand_road + "cand_12_para_wiki_tar_title_same_" + ner_name + "_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        uf.save_cand_wiki_title_sou_in_file(cand_wiki_para_tar_same, sou_cand_para_wiki_tar_title_same)
    
        sou_cand_para_wiki_tar_title_not_same = cand_road + "cand_12_para_wiki_tar_title_not_same_" + ner_name + "_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        uf.save_cand_wiki_title_sou_in_file(cand_wiki_para_tar_not_same, sou_cand_para_wiki_tar_title_not_same)
    
        sou_cand_para_wiki_article_size = cand_road + "cand_13_para_wiki_article_size_" + ner_name + "_" + str(sou_th) + "_" + str(
            tar_th) + ".txt"
        uf.save_cand_wiki_title_sou_in_file(cand_wiki_article_size, sou_cand_para_wiki_article_size)
        
        print("for cand for check save: end\n")
    
        print("for cand for final save: begin\n")
        # for save cand with sentences
        sou_final_entity_check = final_res_road + "cand_with_sent_after_entity_check_" + ner_name + "_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_sent_cand_sou_wiki_title(cand_after_check_entity_with_exp, sou_sentences, tar_sentences, sou_final_entity_check)

        sou_final_entity_check_same = final_res_road + "cand_with_sent_after_entity_check_same_" + ner_name + "_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_sent_cand_sou_wiki_title(cand_check_entity_same, sou_sentences, tar_sentences,
                                         sou_final_entity_check_same)

        sou_final_wiki_title = final_res_road + "cand_with_sent_after_both_wiki_title_" + ner_name +"_"+str(sou_th)+"_"+str(tar_th)+ ".txt"
        uf.save_sent_cand_sou_wiki_title(cand_after_check_title, sou_sentences, tar_sentences, sou_final_wiki_title)
    
        sou_final_para_wiki_title = final_res_road + "cand_with_sent_after_para_wiki_title_" + ner_name + "_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_sent_cand_sou_wiki_title(cand_after_check_para_title_in, sou_sentences, tar_sentences, sou_final_para_wiki_title)
    
        sou_final_not_para_wiki_title = final_res_road + "cand_with_sent_after_not_para_wiki_title_" + ner_name + "_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_sent_cand_sou_wiki_title(cand_after_check_para_title_not_in, sou_sentences, tar_sentences,
                                         sou_final_not_para_wiki_title)
        
        sou_final_para_wiki_tar_title_same = final_res_road + "cand_with_sent_after_para_wiki_tar_title_same_" + ner_name + "_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_sent_cand_sou_wiki_title(cand_wiki_para_tar_same, sou_sentences, tar_sentences,
                                         sou_final_para_wiki_tar_title_same)
    
        sou_final_para_wiki_tar_title_not_same = final_res_road + "cand_with_sent_after_para_wiki_tar_title_not_same_" + ner_name + "_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_sent_cand_sou_wiki_title(cand_wiki_para_tar_not_same, sou_sentences, tar_sentences,
                                         sou_final_para_wiki_tar_title_not_same)
    
        sou_final_para_wiki_article_size = final_res_road + "cand_with_sent_after_para_wiki_article_size_" + ner_name + "_" + str(
            sou_th) + "_" + str(tar_th) + ".txt"
        uf.save_sent_cand_sou_wiki_title(cand_wiki_article_size, sou_sentences, tar_sentences,
                                         sou_final_para_wiki_article_size)
        print("for cand for final save: end\n")
    
        time_end = time.time()
        print('time cost: ', time_end - time_start, 's')
    
    num_f_t_entity_check.write("total: " + str(total_num_entity_check) + "\n")
    num_f_t_wiki.write("total: " + str(total_num_wiki) + "\n")
    num_f_t_para_wiki.write("total: " + str(total_num_para_wiki) + "\n")
    num_f_t_not_para_wiki.write("total: " + str(total_num_not_para_wiki) + "\n")
    num_f_t_para_tar_wiki_same.write("total: " + str(total_num_para_wiki_tar_same) + "\n")
    num_f_t_para_tar_wiki_not_same.write("total: " + str(total_num_para_wiki_tar_not_same) + "\n")
    num_f_t_para_wiki_size.write("total: " + str(total_num_para_wiki_size) + "\n")
    num_f_t_entity_check.close()
    num_f_t_wiki.close()
    num_f_t_para_wiki.close()
    num_f_t_not_para_wiki.close()
    num_f_t_para_tar_wiki_same.close()
    num_f_t_para_tar_wiki_not_same.close()
    num_f_t_para_wiki_size.close()
    