

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
    counter = Counter(open(path+ds+"-decomp.txt", "r").read().split(" ")) # split(" ")ではスペースごとに区切ってリストを作成している
    hgram.append(dict(counter.most_common()))

for ds in kikuchi:
    counter = Counter(open(path+ds+"-decomp.txt", "r").read().split(" "))
    hgram.append(dict(counter.most_common()))

def dl2(dictx, dicty):
    sq = 0
    for key in set(dictx.keys()) | set(dicty.keys()):
        x, y = 0, 0
        if key in dictx: 
            x = dictx[key]
        if key in dicty:
            y = dicty[key]
        sq += (x - y)**2
    return math.sqrt(sq)

temp = [] 
for dictx in hgram:
    temp.append(list(map(lambda dicty: dl2(dictx, dicty), hgram)))
dl2_matrix = np.matrix(temp)


akutagawa_name = ['羅生門', '妖婆', '藪の中', '貉', '鼻', '歯車', 'トロッコ', '杜子春', '俊寛', '侏儒の言葉', '邪宗門', '将軍', '死後', 'アグニの神', '或る日の大石内蔵助', 'おぎん', 'お時儀', '河童', '煙管', '蜘蛛の糸']
kikuchi_name = ['姉川の戦い', 'ある恋の話', '入れ札', 'M公爵と写真師', '屋上の狂人', '恩讐の彼方に', '女強盗', '恩を返す話', '義民甚平', '勲章を貰う話', '極楽', '出世', '勝負事', '大力の物語', '藤十郎の恋', 'ある抗議書', '身投げ救助業', '無名作家の日記', '若杉裁判長', '奉行と人相学']

name = akutagawa_name + kikuchi_name # 40作品すべてのタイトルのリスト生成

union = set()
for d in hgram:
    union |= d.keys()

words = list(union)

def count(n, w):
    if w in hgram[n]:
        return hgram[n][w]
    else:
        return 0
    
    
#2-10,2-11

# L2正規化を行う関数を作成&歯車と蜘蛛の糸の(正規化後の)分布を表示

def l2normalize(dct): # L2正規化
    s = np.sqrt(sum([v**2 for v in dct.values()]))
    return dict([(k, v/s) for k, v in dct.items()]) 

hgrm_nrm = [l2normalize(dct) for dct in hgram] # hgramは前に作成したリスト。各作品の単語の種類とその単語の出現回数を持つ辞書型オブジェクトを作品の数だけ持つ。

#2-12
def countl2(n, w): # n番目の作品にwという単語が何回出現しているかを返す関数
    if w in hgrm_nrm[n]:
        return hgrm_nrm[n][w]
    else:
        return 0


#2-13
def dl1(dictx, dicty): # L1距離
    sq = 0
    for key in set(dictx.keys()) | set(dicty.keys()):
        x, y = 0, 0
        if key in dictx: 
            x = dictx[key]
        if key in dicty:
            y = dicty[key]
        sq += abs(x - y)
    return sq

def distribution(dct): # ヒストグラムを確率分布に変換
    s = sum(dct.values())
    return dict([(k, v/s) for k, v in dct.items()]) 

prob = list(map(lambda dct: distribution(dct), hgram)) # 確率分布データ