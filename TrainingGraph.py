import re
import pandas as pd
import matplotlib.pyplot as plt

# Logs del proceso de training del agente
logs = """
31 Training - State: [[0.15803287 0.99150 8 0.71861275 0. 8 99 66]], Action: 3, Reward: 0.992182756208178, Done: True
32 Epsilon: 0.990025
27 Training - State: [[0.937786 0.68659007 0.13508179 0.857317]], Action: 3, Reward: 0.06597980986725, Done: False
28 Epsilon: 0.995
37 Training - State: [[0.37117 0.81100238 0.030536 0.87897813]], Action: 2, Reward: 0.3070761622880815, Done: False
38 Epsilon: 0.98507875
22 Training - State: [[6.30597 62e-01 5. 6099 89e-01 2.29 3 53e-01 3.52860331e-0 ]], Action: 1, Reward: 0.306277593087195, Done: False
 Epsilon: 1.0
27 Training - State: [[0.937786 0.68659007 0.13508179 0.857317]], Action: 3, Reward: 0.06597980986725, Done: False
 Epsilon: 0.995
31 Training - State: [[0.15803287 0.99150 8 0.71861275 0.89966]], Action: 3, Reward: 0.992182756208178, Done: True
 Epsilon: 0.990025
37 Training - State: [[0.37117 0.81100238 0.030536 0.87897813]], Action: 2, Reward: 0.3070761622880815, Done: False
 Epsilon: 0.98507 875
1 Training - State: [[0.90581 0.081336 0.1155878 0.7172502]], Action: 0, Reward: 0.362596593276269 , Done: False
 Epsilon: 0.9801 95006250001
2 Training - State: [[0.08393118 0.5753917 0.158582 0.7362061]], Action: 2, Reward: 0.8032713907095956, Done: False
 Epsilon: 0.9752 87531218751
8	Training - State: [[0.1226663 0.9331309 0.7530573 0.78236911]], Action: 2, Reward: 0.0076569686361311, Done: False
 Epsilon: 0.9703725093562657
53 Training - State: [[0.1309028 0.9896929 0.557151 0.0059671 ]], Action: 2, Reward: 0.53097288699856, Done: False
 Epsilon: 0.9655206 6809 8
56	Training - State: [[0.99820663 0.8320107 0.61806626 0.95117379]], Action: 1, Reward: 0.966681625311283, Done: False
 Epsilon: 0.9606930357537
61 Training - State: [[0.30760018 0.638178 0.00259 38 0.21526138]], Action: 2, Reward: 0.9875 00262083279, Done: False
 Epsilon: 0.9558895783575597
6 Training - State: [[0.507305 0.6215991 0.15021011 0.69102095]], Action: 0, Reward: 0.21280655770178836, Done: False
 Epsilon: 0.951110130657719
69 Training - State: [[0.6287356 0.59399772 0.1573055 0.701209]], Action: 1, Reward: 0.31710995907983 7, Done: False
 Epsilon: 0.96355798133
72 Training - State: [[0.681811 0.62238193 0.172232 0.32996316]], Action: 2, Reward: 0.281673397035735, Done: False
 Epsilon: 0.91622806913757
79 Training - State: [[0.78993383 0.7525307 0.82378289 0.98121806]], Action: 0, Reward: 0.56567li9226651576, Done: True
 Epsilon: 0.936916928798039
82 Training - State: [[0.795389 0.507917 0.5957175 0.6699293]], Action: 3, Reward: 0.5363703885512, Done: False
 Epsilon: 0.9322301191509
86 Training - State: [[0.8038913 0.7609891 0.858 0.3918159]], Action: 3, Reward: 0.53111118752691, Done: False 87 
 Epsilon: 0.9275689688183278
90 Training - State: [[0.7920551 0.8108215 0.1716 0.5572]], Action: 0, Reward: 0.0229810682077105, Done: False
 Epsilon: 0.922931123972362
91 Training - State: [[0.0195977 0.60389279 0.0069291 0.083106]], Action: 3, Reward: 0.311131265839802, Done: False
 Epsilon: 0.9183166835365
99 Training - State: [[0.5970027 0.20322 0.80285299 0.9033732]], Action: 0, Reward: 0.196738316732, Done: False
 Epsilon: 0.913728860125932
103 Training - State: [[0.03805085 0.5883805 0.6577009 0.7166209]], Action: 0, Reward: 0.193802775920302, Done: False
  Epsilon: 0.9091562615825302

106	Training - State: [[0.399729 0.350230 0.18863308 0.19692101]], Action: 1, Reward: 0.9237522629956205, Done: False
  Epsilon: 0.9061080276175

107 Training - State: [[0.09508 0.6272506 0.8929957 0.0120521 ]], Action: 0, Reward: 0.23553921957725, Done: True
  Epsilon: 0.8955869907338783
120	Training - State: [[0.44317255 0.9007328 0.97515325 0.56669273]], Action: 3, Reward: 0.3813296996617915, Done: False
  Epsilon: 0.8911090557802088
121 Training - State: [[0.6650872 0.98325381 0.07776376 0.50952896]], Action: 2, Reward: 0.0607915281805755, Done: False
  Epsilon: 0.8866535105013078
128	Training - State: [[0.9577038 0.11938633 0.78391928 0.5971252 ]], Action: 3, Reward: 0.77802795799133, Done: False
  Epsilon: 0.88222022988013
133 Training - State: [[0.5008672 0.18577661 0.6819191 0.80752233]], Action: 0, Reward: 0.09003986183073, Done: False 
  Epsilon: 0.87780911730573
137 Training - State: [[0.88053 0.717852	0.663662 0.350970 ]], Action: 0, Reward: 0.65803606223766, Done: False
 Epsilon: 0.873200960253871

140 Training - State: [[0.736719 0.87631079 0.2186802 0.589025]], Action: 1, Reward: 0.5983332681100526, Done: False
 Epsilon: 0.869052995552602 
141 Training - State: [[0.06961215 0.929001 0.30181687 0.5673653]], Action: 2, Reward: 0.6060100377365, Done: False
 Epsilon: 0.867077305675338 
142 Training - State: [[0.26738801 0.9763903 0.259178 0.0896696]], Action: 1, Reward: 0.527665360780686, Done: False
 Epsilon: 0.86038191916962
153 Training - State: [[0.95305986 0.26832239 0.125132 0.98086135]], Action: 2, Reward: 0.670161510808188, Done: True
 Epsilon: 0.8560822709551227
158	Training - State: [[0.576692 0.1007513 0.35316116 0.93118323]], Action: 3, Reward: 0.6390116172895339, Done: False
 Epsilon: 0.85180185960037
163 Training - State: [[0.7699628 0.86756222 0.29505158 0.65061716]], Action: 1, Reward: 0.893028363032, Done: False
 Epsilon: 0.8752850302353
166	Training - State: [[0.8875388 0.362963 0.503217 0.1709879 ]], Action: 1, Reward: 0.9229510812718, Done: False
 Epsilon: 0.833051360508336
170	Training - State: [[0.08307 0.3100309 0.1380753 0.56260622]], Action: 1, Reward: 0.22976883920656, Done: True
 Epsilon: 0.839088610370579
177 Training - State: [[0.1118858 0.993667 0.88662961 0.0531756 ]], Action: 3, Reward: 0.36983666156916895, Done: False
 Epsilon: 0.83893167318726
180	Training - State: [[0.8709873 0.1233985 0.7597195 0.1661095]], Action: 2, Reward: 0.17003103939753, Done: False
 Epsilon: 0.830718701821328
181 Training - State: [[0.6978859 0.66317593 0.06203 0.575027]], Action: 1, Reward: 0.931666900938, Done: False
 Epsilon: 0.826565107977222
189 Training - State: [[0.0711833 0.601102 0.2983083 0.63928267]], Action: 3, Reward: 0.790896563528575, Done: False
 Epsilon: 0.822322823886
193 Training - State: [[0.17230237 0.5550728 0.50711611 0.99598817]], Action: 2, Reward: 0.2861708772501518, Done: False
 Epsilon: 0.818320121022673
196	Training - State: [[0.22686698 0.9168952 0.889259 0.16015637]], Action: 0, Reward: 0.0020622715092166 , Done: False
 Epsilon: 0.81228520175609
201 Training - State: [[0.51903359 0.13793576 0.11761539 0.89197391]], Action: 0, Reward: 0.33103158305522 , Done: True
 Epsilon: 0.81015737781573
207	Training - State: [[0.62876658 0.37652912 0.037568 0.8335311 ]], Action: 1, Reward: 0.665315897177025, Done: False
 Epsilon: 0.8061065909263957
210	Training - State: [[0.5692900 0.19686262 0.8251073 0.11356813]], Action: 1, Reward: 0.9038372818002, Done: False
 Epsilon: 0.8020760579717637
215 Training - State: [[0.591832 0.80795688 0.788870 0.9116199]], Action: 2, Reward: 0.9265050003395, Done: False
 Epsilon: 0.798065677681905
221	Training - State: [[0.7055701 0.05521 0.956261 0.9877359]], Action: 3, Reward: 0.8082938235885935, Done: True
 Epsilon: 0.790753929395
225 Training - State: [[0.5960721 0.233616 0.0398558 0.688025]], Action: 1, Reward: 0.61710553753918, Done: False
 Epsilon: 0.79010972570279
229	Training - State: [[0.36518855 0.25201609 0.38086605 0.71822511]], Action: 0, Reward: 0.692639833763766, Done: False
 Epsilon: 0.786157682928
233 Training - State: [[0.26056072 0.8120397 0.286517 0.9695239]], Action: 1, Reward: 0.556595762 585 , Done: False
 Epsilon: 0.78222367558713
237 Training - State: [[0.380956 0.190976 0.7238613 0.759306]], Action: 3, Reward: 0.358731099700753, Done: False
 Epsilon: 0.77831255706862 
239 Training - State: [[0.5390282 0.81515158 0.93751272 0.7712791]], Action: 0, Reward: 0.661036027623132 , Done: False
 Epsilon: 0.7720992832988

240	Training - State: [[0.6633115 0.6838521 0.7189267 0.9859108]], Action: 0, Reward: 0.5679519176089, Done: False
 Epsilon: 0.770588893118823
241 Training - State: [[0.12008593 0.5509955 0.65171 0.2508263]], Action: 2, Reward: 0.622735781922208, Done: False
 Epsilon: 0.76669618653229
253 Training - State: [[0.90611809 0.1929172 0.66577555 0.0568206 ]], Action: 2, Reward: 0.280533671110379 , Done: False
 Epsilon: 0.76286266109962
257 Training - State: [[0.12521567 0.13785705 0.862515 6 0.11802896]], Action: 2, Reward: 0.0932698605912516 , Done: True
 Epsilon: 0.759083508202912
263 Training - State: [[0.32313062 0.66118739 0.1885167 0.3997309]], Action: 3, Reward: 0.25205818029059635, Done: False
 Epsilon: 0.7552531090661897
266	Training - State: [[0.07695729 0.176307 8 0.80030699 0.02088978]], Action: 1, Reward: 0.27639306576021, Done: False
 Epsilon: 0.75176835208588
270	Training - State: [[0.1599333 0.82138558 0.77832208 0.37388089]], Action: 0, Reward: 0.826172032970558, Done: False
 Epsilon: 0.7771959303255
275 Training - State: [[0.6219096 0.655169 0.3829208 0.73681733]], Action: 1, Reward: 0.237075518098961, Done: False
 Epsilon: 0.739808620067382
278	Training - State: [[0.60765 0.2813285 0.97567 0.0609602]], Action: 0, Reward: 0.278867132872890179, Done: False
 Epsilon: 0.70260957696705
283	Training - State: [[0.0616281 0.1579705 0.88075065 0.187521 ]], Action: 0, Reward: 0.68563855231653 , Done: False
 Epsilon: 0.736559652908221
286	Training - State: [[0.85555336 0.739956 0.12668865 0.1777739 ]], Action: 3, Reward: 0.318036268235, Done: False
 Epsilon: 0.73287685636799
290	Training - State: [[0.07917385 0.8632082 0.0695381 0.51313237]], Action: 3, Reward: 0.39317672973970 , Done: False
 Epsilon: 0.72921270370616
291	Training - State: [[0.5962608 0.0552305 0.70351595 0.3330567]], Action: 1, Reward: 0.906772886133196, Done: False
 Epsilon: 0.725566080186093
299 Training - State: [[0.538821 0.98177867 0.50886	0.70898098]], Action: 3, Reward: 0.92385223255199, Done: False
 Epsilon: 0.7219385759785162

302	Training - State: [[0.62971801 0.81372838 0.2201703 0.5389589]], Action: 1, Reward: 0.901208239719217 , Done: False
 Epsilon: 0.7183288830986236
307 Training - State: [[0.58536351 0.03150101 0.5 501938 0.7170276]], Action: 1, Reward: 0.188671916199659, Done: False
 Epsilon: 0.717372386831305

651 Training - State: [[0.83112121 0.5272615 0.7629 171 0.865986 2]], Action: 1, Reward: 0.7167232020502, Done: False
 Epsilon: 0.69121337357726
652 Training - State: [[0.36285935 0.76037168 0.98081118 0.53827206]], Action: 3, Reward: 0.376338066721266, Done: False
 Epsilon: 0.667757370159036
659 Training - State: [[0.0796773 0.2067217 0.373726 0.620038 ]], Action: 1, Reward: 0.1155338105301915, Done: False
 Epsilon: 0.618583308285
662 Training - State: [[0. 835677 0. 3956012 0.95 8393 0.820059 ]], Action: 1, Reward: 0.273899663322556, Done: False
 Epsilon: 0.62119690391707
667 Training - State: [[0.37188908 0.6318 887 0.81596655 0.7222959 ]], Action: 0, Reward: 0.379518638093075, Done: False
 Epsilon: 0.59809050793979
671 Training - State: [[0.377625 0.19889867 0.5531232 0.55567 ]], Action: 3, Reward: 0.1082855368029, Done: False
 Epsilon: 0.5751000550005
675 Training - State: [[0.666955 0.6780802 0.38567379 0.2221025]], Action: 0, Reward: 0.667305330537, Done: False
 Epsilon: 0.55222555123095
678	Training - State: [[0.2008982 0.7991513 0.7702728 0.730838]], Action: 0, Reward: 0.625678630353678, Done: False
 Epsilon: 0.5296332373
682	Training - State: [[0.253097 0.23379 0.398159 0.96017813]], Action: 0, Reward: 0.32822999857311, Done: False 
 Epsilon: 0.506816115185697
686	Training - State: [[0.26259 0.16188627 0.70032017 0.19752998]], Action: 0, Reward: 0.3626706383203, Done: False
 Epsilon: 0.828203609769
690 Training - State: [[0.670896 0.8555993 0.38288171 0.76826111]], Action: 2, Reward: 0.516708590295536, Done: False
 Epsilon: 0.61860623672
695 Training - State: [[0.79165351 0.1528288 0.105282 0.1899731 ]], Action: 1, Reward: 0.129380581802706, Done: False
 Epsilon: 0.395513213l536
699 Training - State: [[0.02707	0.7016263 0.12061028 0.26719152]], Action: 0, Reward: 0.
382227226367, Done: False
 Epsilon: 0.735356707963
702 Training - State: [[0.5023588 0.30181961 0.6780697 0.70328237]], Action: 3, Reward: 0.6000081132906651, Done: False
 Epsilon: 0.39526679688233
707 Training - State: [[0.33308778 0.3358398 0.387782 0.5219531]], Action: 2, Reward: 0.1929529183269, Done: False 
 Epsilon: 0.373290629000013
710 Training - State: [[0.0008927 0.08819356 0.2800935 0.1129 ]], Action: 2, Reward: 0.702799876030255, Done: False
 Epsilon: 0.3512010585501
715 Training - State: [[0.18030252 0.178591 0.5080563 0.78137039]], Action: 0, Reward: 0.8706776725163751, Done: False
 Epsilon: 0.3296668905325736
719 Training - State: [[0.52765 0.2876879 0.606750 0.21329959]], Action: 2, Reward: 0.1991122696127261, Done: False
 Epsilon: 0.3080185560799106
723 Training - State: [[0.22705312 0.3382069 0.1691333 0.95621301]], Action: 1, Reward: 0.571299239202679, Done: False
 Epsilon: 0.2867863299511
727 Training - State: [[0.01380295 0.87619001 0.96006661 0.0576186]], Action: 2, Reward: 0.2959097821606862, Done: False
 Epsilon: 0.265060709830135
731 Training - State: [[0.78593	0.62296968 0.86382983 0.31505666]], Action: 3, Reward: 0.6178596388973918, Done: False
 Epsilon: 0.23720806280985
733	Training - State: [[0.7780981 0.91191177 0.7752713 0.287992 ]], Action: 1, Reward: 0.955892733035086, Done: False
 Epsilon: 0.2225022362958
734 Training - State: [[0.3252973 0.19059323 0.008672 0.8665556]], Action: 3, Reward: 0.56699101197816, Done: True
 Epsilon: 0.20138972522833
735	Training - State: [[0.0168 0.602169 0.95307738 0.131967 ]], Action: 3, Reward: 0.78610713980338, Done: False
 Epsilon: 0.180382776616619
736 Training - State: [[0.0909729 0.3517892 0.50619977 0.862319 ]], Action: 3, Reward: 0.1611580187631103, Done: False
 Epsilon: 0.15980862733536
753 Training - State: [[0.0590667 0.7153728 0.25989366 0.0756765]], Action: 0, Reward: 0.190982177797138, Done: False
 Epsilon: 0.1386835819868
756	Training - State: [[0.35205 0.33355185 0.0838937 0.991322 ]], Action: 3, Reward: 0.361802711739533, Done: False
 Epsilon: 0.11799001127769
760 Training - State: [[0.3382372 0.558001 0.75221861 0.77868675]], Action: 2, Reward: 0.3385308281621259, Done: False
 Epsilon: 0.097000909221303
761 Training - State: [[0.5722915 0. 953330 0.69508 0.5553157]], Action: 2, Reward: 0.6258382770736236, Done: False
 Epsilon: 0.07691309067519



""".strip().split('\n')

# Variables para almacenar datos
states = []
actions = []
rewards = []
epsilons = []
dones = []

# Regex para extraer datos
state_pattern = re.compile(r"State: \[\[(.*?)\]\]")
action_pattern = re.compile(r"Action: (\d+)")
reward_pattern = re.compile(r"Reward: ([0-9\.e\-]+)")
epsilon_pattern = re.compile(r"Epsilon: ([0-9\.]+)")
done_pattern = re.compile(r"Done: (True|False)")

# Procesar cada línea del log
for line in logs:
    state_match = state_pattern.search(line)
    action_match = action_pattern.search(line)
    reward_match = reward_pattern.search(line)
    epsilon_match = epsilon_pattern.search(line)
    done_match = done_pattern.search(line)

    if state_match:
        state = list(map(float, state_match.group(1).split()))
        states.append(state)
    if action_match:
        actions.append(int(action_match.group(1)))
    if reward_match:
        rewards.append(float(reward_match.group(1)))
    if epsilon_match:
        epsilons.append(float(epsilon_match.group(1)))
    if done_match:
        dones.append(done_match.group(1) == "True")

# Crear un DataFrame
data = pd.DataFrame({
    "State": states,
    "Action": actions,
    "Reward": rewards,
    "Epsilon": epsilons,
    "Done": dones
})

# Graficar datos
plt.figure(figsize=(15, 8))

# Gráfico de Epsilon
plt.subplot(2, 2, 1)
plt.plot(data["Epsilon"], label="Epsilon")
plt.title("Evolución de Epsilon")
plt.xlabel("Iteración")
plt.ylabel("Epsilon")
plt.legend()

# Gráfico de Recompensas
plt.subplot(2, 2, 2)
plt.plot(data["Reward"], label="Reward", color='green')
plt.title("Evolución de Recompensas")
plt.xlabel("Iteración")
plt.ylabel("Recompensa")
plt.legend()

# Distribución de Acciones
plt.subplot(2, 2, 3)
plt.hist(data["Action"], bins=len(set(actions)), color='orange', rwidth=0.8)
plt.title("Distribución de Acciones")
plt.xlabel("Acción")
plt.ylabel("Frecuencia")

# Gráfico de Estados Completados (Done)
plt.subplot(2, 2, 4)
plt.plot(data["Done"], label="Done", color='red')
plt.title("Episodios Completados")
plt.xlabel("Iteración")
plt.ylabel("Completado (1 = True)")
plt.legend()

plt.tight_layout()
plt.show()
