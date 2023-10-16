Results:

The experimental results of this paper are included in the /Data/ folder. The experimental results of each language pair are in their respective folders.

Taking language pair English ->German as an example:

The experimental results are located in the folder /en-de/exp/

For convenience, we will divide the 5 million sentence pairs as experimental input into 5 smaller inputs, each with 1 million sentence pairs, so there are a total of five folders (numbered 1-5). Each numbered folder contains the experimental results of each filter step (i.e. the sentence pairs left after filtering)

Folder check_ Entity are experimental results that checks whether all named entities found that need to be explained are always explained

File 11.1+13_sent.txt is the final result manually filtered out, which is the target sentence pair with explanations

File 11.1+13_word.txt stores the words and phrases that need to be explained

The experimental results for evaluation are located in the folder /en-de/eval/

###########################################################################################

Code:

The implementation of this paper is in the folder /Code/

For Chinese, a preprocessing is to convert Traditional Chinese to Simplified Chinese, this function is in zh_conveert.py. We use the tool opencc (https://github.com/BYVoid/OpenCC)

Tokenization functions are in file sent_token.py

We use get_word_count_from_file.py and get_word_count_from_wiki.py to get the word count/article size from wikipedia articles. (The input is the articles extracted from wikipedia using wiki_extractor (https://github.com/attardi/wikiextractor))

eval.py is used to extract five million randomly selected sentence pairs from a corpus. Randomly selected sentence pair numbers in the folder /en-de/eval/

check.py is used to get statistical results

Other files related to the experimental process

###########################################################################################

1. Step: filter 1.part in process_with_word.py
2. Step: process_with_align.py
3. Step: filter 3. & 4. part in process_with_word.py
4. Step: run_ner.py
5. Step: process_with_wiki.py

###########################################################################################


