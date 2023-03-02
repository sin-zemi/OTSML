from collections import Counter
import math
import numpy as np

columns = ['する:動詞:自立', 'いる:動詞:非自立', 'の:名詞:非自立', 
           '事:名詞:非自立',
           '云う:動詞:自立',
           '老婆:名詞:一般',
           'よう:名詞:非自立',
           'なる:動詞:自立']

def count(n, w):
    if w in hgram[n]:
        return hgram[n][w]
    else:
        return 0

body = []
for n in range(20):
    temp = [count(n, w) for w in columns]
    temp.append('芥川')
    body.append(temp)
for n in range(20):
    temp = [count(n+20, w) for w in columns]
    temp.append('菊池')
    body.append(temp)

path = "OTSML/"



akutagawa = ["rashomon.txt","yoba.txt","yabuno_naka.txt","mujina.txt","hana.txt",
            "haguruma.txt","torokko.txt","toshishun.txt","shunkan.txt","shujuno_kotoba.txt",
            "jashumon.txt","shogun.txt","shigo.txt","agunino_kami.txt","aruhino_oishi_kuranosuke.txt",
            "ogin.txt","ojigi.txt","kappa.txt","kiseru.txt","kumono_ito.txt"]
kikuchi = ["anegawano_kassen.txt","aru_koino_hanashi.txt","irefuda.txt","emukoshakuto_shashinshi.txt",
          "okujono_kyojin.txt","onshuno_kanatani.txt","onnagoto.txt","on'o_kaesu_hanashi.txt",
          "gimin_jinbee.txt","kunshoo_morau_hanashi.txt","gokuraku.txt","shusse.txt",
          "shobugoto.txt","dairiki_monogatari.txt","tojurono_koi.txt","aru_kogisho.txt",
          "minage_kyujogyo.txt","mumeisakkano_nikki.txt","wakasugi_saibancho.txt","bugyoto_ninsogaku.txt"]

    
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