from collections import Counter
import math
import numpy as np

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
print(hgram)
for ds in kikuchi:
    counter = Counter(open(path+ds+"-decomp.txt", "r").read().split(" "))
    hgram.append(dict(counter.most_common()))
print(hgram)
 # 40編全ての名詞・形容詞・形容動詞・副詞の種類の総数
union = set()#空集合
for d in hgram:  # hgramは作品事(リストの引数に一つの作品が対応)に単語（形容詞・動詞・名詞・副詞）について、その出現頻度をカウントしたデータが入っている。
    union |= d.keys()#|は和集合の演算
def count(dict, word): # dict内にwordが含まれているなら、その数を返す関数
    if word in dict:
        return dict[word]
    else:
        return 0
raw_vector = np.array([[count(h, w) for w in union] for h in hgram]) # raw_vector[i][j]は、作品番号iの小説の中に単語番号jの単語が出現する回数


 # (表形式のデータの作成)
import pandas as pd
akutagawa_name = ['羅生門', '妖婆', '藪の中', '貉', '鼻', '歯車', 'トロッコ', '杜子春', '俊寛', '侏儒の言葉', '邪宗門', '将軍', '死後', 'アグニの神', '或る日の大石内蔵助', 'おぎん', 'お時儀', '河童', '煙管', '蜘蛛の糸']
kikuchi_name = ['姉川の戦い', 'ある恋の話', '入れ札', 'M公爵と写真師', '屋上の狂人', '恩讐の彼方に', '女強盗', '恩を返す話', '義民甚平', '勲章を貰う話', '極楽', '出世', '勝負事', '大力の物語', '藤十郎の恋', 'ある抗議書', '身投げ救助業', '無名作家の日記', '若杉裁判長', '奉行と人相学']

columns = ['する:動詞:自立', 'いる:動詞:非自立', 'の:名詞:非自立', 
           '事:名詞:非自立',
           '云う:動詞:自立',
           '老婆:名詞:一般',
           'よう:名詞:非自立',
           'なる:動詞:自立']

 # hgramは二つ前のセルで作成したリスト。各作品の形態素の種類とその形態素の出現回数を持つ辞書型オブジェクトを作品の数だけ持つ。
 # 本来このような関数の作成方法は良くないことに注意
 # countはn番目の作品にwという形態素は何回出現しているかを返す関数
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