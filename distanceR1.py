 # 40編の作品のルビ・注釈を削除&名詞・形容詞・動詞・副詞のみを抽出
import re
import MeCab as mc
import ipadic

def decomp(text): # 形容詞、動詞、名詞、副詞のみを取り出す
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

kosuijun = re.compile(u'([一-龥]*※［[^］]+］)+[一-龥]*《([^》]+)》') # 高水準漢字のパターン
ruby = re.compile(r'《[^》]+》') # ルビのパターン
chu = re.compile(r'［[^］]+］') # 注釈のパターン

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

for ds in akutagawa:
    text = open(path+ds,"r",encoding = "shift-jis").read()
    text = re.sub(kosuijun,r'\2',text) # 高水準漢字を読みに置き換え
    text = re.sub(ruby,"",text) # ルビの削除
    text = re.sub(chu,"",text) # 注釈の削除
    out = open(path+ds+"-decomp.txt", "w")
    out.write(" ".join(decomp(text)))
    out.close()
    
for ds in kikuchi:
    text = open(path+ds,"r",encoding = "shift-jis").read()
    text = re.sub(kosuijun,r'\2',text) # 高水準漢字を読みに置き換え
    text = re.sub(ruby,"", text) # ルビの削除
    text = re.sub(chu,"",text) # 注釈の削除
    out = open(path+ds+"-decomp.txt", "w")
    out.write(" ".join(decomp(text)))
    out.close()
    
 # 実際の40作品にて、名詞・形容詞・動詞・副詞の出現回数を計数してhgramにまとめる
from collections import Counter

path = "OTSML/"
akutagawa = ["rashomon.txt","yoba.txt","yabuno_naka.txt","mujina.txt","hana.txt",
            "haguruma.txt","torokko.txt","toshishun.txt","shunkan.f","shujuno_kotoba.txt",
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

 # 40編全ての名詞・形容詞・形容動詞・副詞の種類の総数
union = set()
for d in hgram:
    union |= d.keys()
    
akutagawa_name = ['羅生門', '妖婆', '藪の中', '貉', '鼻', '歯車', 'トロッコ', '杜子春', '俊寛', '侏儒の言葉', '邪宗門', '将軍', '死後', 'アグニの神', '或る日の大石内蔵助', 'おぎん', 'お時儀', '河童', '煙管', '蜘蛛の糸']
kikuchi_name = ['姉川の戦い', 'ある恋の話', '入れ札', 'M公爵と写真師', '屋上の狂人', '恩讐の彼方に', '女強盗', '恩を返す話', '義民甚平', '勲章を貰う話', '極楽', '出世', '勝負事', '大力の物語', '藤十郎の恋', 'ある抗議書', '身投げ救助業', '無名作家の日記', '若杉裁判長', '奉行と人相学']