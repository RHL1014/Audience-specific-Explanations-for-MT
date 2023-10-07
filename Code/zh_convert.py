import opencc
from tqdm import tqdm

"This file is used to convert Traditional Chinese into Simplified Chinese"
if __name__ == '__main__':
    converter = opencc.OpenCC('t2s.json')
    file_in = "E:\\cc_matrix\\en-zh\\zh_1.txt"
    file_out = "E:\\cc_matrix\\en-zh\\zh_simp_1.txt"
    out_f = open(file_out, 'w', encoding='utf-8')
    with tqdm(total=24000000) as bar:
        with open(file_in, 'r', encoding='utf-8') as in_f:
            for line in in_f:
                sent = line.strip()
                converter = opencc.OpenCC('t2s.json')
                new_sent = converter.convert(sent)
                out_f.write(new_sent+"\n")
                bar.update(1)
    out_f.close()
    