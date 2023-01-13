 # 実際の40作品にて、名詞・形容詞・動詞・副詞の出現回数を計数してhgramにまとめる
from collections import Counter

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

hgram = []

for ds in akutagawa:
    counter = Counter(open(path+ds+"-decomp.txt", "r").read().split(" ")) # split(" ")ではスペースごとに区切ってリストを作成している
    hgram.append(dict(counter.most_common()))

for ds in kikuchi:
    counter = Counter(open(path+ds+"-decomp.txt", "r").read().split(" "))
    hgram.append(dict(counter.most_common()))
list(hgram[0].items())[:10]
 # hgram[i]は番号iの作品の形態素の種類とその形態素が番号iの作品にいくつ入っているかを示す辞書型オブジェクト
 
 
  # 40編全ての名詞・形容詞・形容動詞・副詞の種類の総数
union = set()
for d in hgram:
    union |= d.keys()
print('40編の作品に現れる語の総数は', len(union))

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

df = pd.DataFrame(body)
columns.append('著者')
df.columns = columns
df.index = akutagawa_name + kikuchi_name
df


 # hgramの保存
import pickle
f = open("hgram.txt", "wb")
pickle.dump(hgram, f)


 # hgramの呼び出し
f = open("hgram.txt", "rb")
hgram = pickle.load(f)
hgram


 # 前記の8項目の特徴に関して、「羅生門」と「姉川の戦い」の分布を比較
import matplotlib.pyplot as plt
import japanize_matplotlib
df_wo_author = df[df.columns[:-1]]

_, axes = plt.subplots(1, 2, figsize=[15,6])
fig1 = df_wo_author.loc['羅生門'].plot.bar(title='羅生門（芥川龍之介）', ax=axes[0], fontsize=16)
fig1.axes.title.set_size(24)
fig2 = df_wo_author.loc['姉川の戦い'].plot.bar(title='姉川の戦い（菊池寛）', ax=axes[1], fontsize=16)
fig2.axes.title.set_size(24)

axes[0].set_ylim([0,160])
axes[1].set_ylim([0,160])
plt.show()


import numpy as np
words = list(union)

_, axes = plt.subplots(1, 2, figsize=[15,5])

y = [count(0, w) for w in words]
axes[0].plot(range(len(words)), y)
axes[0].set_title('羅生門（芥川龍之介）', fontsize=24)
axes[0].set_ylim([0, 160])
axes[0].xaxis.set_visible(False)
axes[0].set_yticklabels(np.arange(0, 170, 20), fontsize=16)

y = [count(20, w) for w in words]
axes[1].plot(range(len(words)), y)
axes[1].set_title('姉川の戦い（菊池寛）', fontsize=24)
axes[1].set_ylim([0, 160])
axes[1].xaxis.set_visible(False)
axes[1].set_yticklabels(np.arange(0, 170, 20), fontsize=16)
plt.show()


 # 「羅生門」と「姉川の戦い」のユークリッド距離
import math

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
        
print('「羅生門」と「姉川の戦い」のユークリッド距離 = ', dl2(hgram[0], hgram[20]))



 # 距離行列の作成
import numpy as np

temp = [] 
for dictx in hgram:
    temp.append(list(map(lambda dicty: dl2(dictx, dicty), hgram)))
dl2_matrix = np.matrix(temp) # 距離の行列

dl2_matrix


 # MDSで16257次元のベクトル達をを3次元に無理やり圧縮
from sklearn import manifold
mds = manifold.MDS(n_components=3, dissimilarity="precomputed", random_state=6)
pos = mds.fit_transform(dl2_matrix)
pos


 # MDSで3次元に圧縮
import plotly.graph_objects as go
l1 = len(akutagawa)
l2 = len(kikuchi)

fig = go.Figure(
    layout=go.Layout(
    title="ユークリッド距離に基づくデータの分布（MDSによる次元圧縮）" ,
    showlegend=True,
    legend=dict(x=0.7, y=0.99, xanchor='left', yanchor='top', font=dict(size=16))
    )
)

fig.add_trace(go.Scatter3d(
        x = pos[0: l1,0], y = pos[0: l1,1], z = pos[0: l1,2],
        mode = 'markers',
        marker = dict(symbol='cross', color='black', size=5, 
                      line=dict(width=0), opacity=1 ),
        name = '芥川'
        )
)

fig.add_trace(go.Scatter3d(
        x = pos[l1: l1+l2, 0], y = pos[l1: l1+l2, 1], z = pos[l1: l1+l2, 2],
        mode = 'markers',
        marker = dict(symbol='circle', color='black', size=5, 
                      line=dict(width=0), opacity=1),
        name = '菊池'
        )
)

 # ランダムに5群に分割
import random
name = akutagawa_name + kikuchi_name # 40作品すべてのタイトルのリスト生成

a_index = list(range(20)) # 芥川の作品は20(番号と作品が結びつけたい)
random.shuffle(a_index) # ランダムにシャッフル
a_partition = [a_index[4*n:4*n+4] for n in range(5)] # 芥川の20作品を四つずつ、5グループに分けてリストにする
k_index = list(range(20, 40))
random.shuffle(k_index)
k_partition = [k_index[4*n:4*n+4] for n in range(5)]
partition = [a_partition[n] + k_partition[n] for n in range(5)] # 前半四つが芥川、後半四つが菊池の作品番号を持つリストを合計五つ持つリスト

for n in range(5):
    print(n, '群 =', " ".join([name[i] for i in partition[n]]))
    
    
    
 # ハイパーパラメータの値と正解率の関係を得る
from sklearn import model_selection
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore", FutureWarning)

labels = [0]*l1 + [1]*l2 # l1は芥川の作品数、l2は菊池の作品数

parameters = [{'metric': ['precomputed'], 
               'n_neighbors': list(range(1,11))}]
clf = GridSearchCV(KNeighborsClassifier(), parameters, cv=5)
clf.fit(dl2_matrix, labels)

x = []
y = []

params = clf.cv_results_['params']
mean_test_score = clf.cv_results_['mean_test_score']
std_test_score = clf.cv_results_['std_test_score']
for p, m, s in zip(params, mean_test_score, std_test_score):
    print(f"{m:.3f} (+/- {s/2:.3f}) for {p}")
    x.append(p['n_neighbors'])
    y.append(m)

 # ハイパーパラメータの値と正解率の関係の可視化
plt.ylim(0, 1)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.xlabel('$k$', fontsize=16)
plt.ylabel('正解率', fontsize=16)
plt.bar(x, y)
plt.grid()
plt.show()


 # kの最適値
clf.best_estimator_.n_neighbors


 # 正答率の最大値
scores = model_selection.cross_val_score(clf.best_estimator_, X = dl2_matrix, y = labels, cv = 5)
np.average(scores)

