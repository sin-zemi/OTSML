from collections import Counter
import math
import numpy as np

path = "OTSML/"
from collections import Counter
import re
import MeCab as mc
import ipadic
import numpy as np
def decomp(text):
    trg = mc.Tagger(ipadic.MECAB_ARGS)
    node = trg.parseToNode(text)
    output = []
    while node:
        temp = node.feature.split(",")
        if temp[0] in ["形容詞", "動詞", "名詞", "副詞"]:
            output.append(":".join([temp[6],temp[0],temp[1]]))
        node = node.next
        if node is None:
            break
    return output

ruby = re.compile(r'《[^》]+》')
chu = re.compile(r'［[^］]+］')

path = "data/"
akutagawa = ["rashomon.txt","yoba.txt","yabuno_naka.txt","mujina.txt","hana.txt",
            "haguruma.txt","torokko.txt","toshishun.txt","shunkan.txt","shujuno_kotoba.txt",
            "jashumon.txt","shogun.txt","shigo.txt","agunino_kami.txt","aruhino_oishi_kuranosuke.txt",
            "ogin.txt","ojigi.txt","kappa.txt","kiseru.txt","kumono_ito.txt"]
kikuchi = ["anegawano_kassen.txt","aru_koino_hanashi.txt","irefuda.txt","emukoshakuto_shashinshi.txt",
          "okujono_kyojin.txt","onshuno_kanatani.txt","onnagoto.txt","on'o_kaesu_hanashi.txt",
          "gimin_jinbee.txt","kunshoo_morau_hanashi.txt","gokuraku.txt","shusse.txt",
          "shobugoto.txt","dairiki_monogatari.txt","tojurono_koi.txt","aru_kogisho.txt",
          "minage_kyujogyo.txt","mumeisakkano_nikki.txt","wakasugi_saibancho.txt","bugyoto_ninsogaku.txt"]

for ds in akutagawa:
    text = open(path+ds,"r",encoding = "shift-jis").read()
    text = re.sub(ruby,"", text)
    text = re.sub(chu,"",text)
    out = open(path+ds+"-decomp.txt", "w")
    out.write(" ".join(decomp(text)))
    out.close()
    
for ds in kikuchi:
    text = open(path+ds,"r",encoding = "shift-jis").read()
    text = re.sub(ruby,"", text)
    text = re.sub(chu,"",text)
    out = open(path+ds+"-decomp.txt", "w")
    out.write(" ".join(decomp(text)))
    out.close()
    
hgram = []

for ds in akutagawa:
    counter = Counter(open(path+ds+"-decomp.txt", "r").read().split(" "))
    hgram.append(dict(counter.most_common()))

for ds in kikuchi:
    counter = Counter(open(path+ds+"-decomp.txt", "r").read().split(" "))
    hgram.append(dict(counter.most_common()))

 # 40編全ての名詞・形容詞・形容動詞・副詞の種類の総数
union = set()
for d in hgram:  # hgramは作品事(リストの引数に一つの作品が対応)に単語（形容詞・動詞・名詞・副詞）について、その出現頻度をカウントしたデータが入っている。
    union |= d.keys()
def count(dict, word): # dict内にwordが含まれているなら、その数を返す関数
    if word in dict:
        return dict[word]
    else:
        return 0
raw_vector = np.array([[count(h, w) for w in union] for h in hgram]) # raw_vector[i][j]は、作品番号iの小説の中に単語番号jの単語が出現する回数
len(raw_vector[0])