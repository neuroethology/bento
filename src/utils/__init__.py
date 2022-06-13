# __init__.py for utils

from os.path import abspath, sep
from qtpy.QtCore import QMarginsF, QRectF
from qtpy.QtGui import QColor

def fix_path(path):
    return abspath(path.replace('\\', sep).replace('/', sep))

SCENE_PADDING = 200.
def padded_rectf(rectf: QRectF) -> QRectF:
    return rectf + QMarginsF(SCENE_PADDING, 0., SCENE_PADDING, 0.)

cm_data_parula = [
    [ 0.26710521,  0.03311059,  0.6188155 ],
    [ 0.26493929,  0.04780926,  0.62261795],
    [ 0.26260545,  0.06084214,  0.62619176],
    [ 0.26009691,  0.07264411,  0.62951561],
    [ 0.25740785,  0.08360391,  0.63256745],
    [ 0.25453369,  0.09395358,  0.63532497],
    [ 0.25147146,  0.10384228,  0.6377661 ],
    [ 0.24822014,  0.11337029,  0.6398697 ],
    [ 0.24478105,  0.12260661,  0.64161629],
    [ 0.24115816,  0.131599  ,  0.6429888 ],
    [ 0.23735836,  0.14038009,  0.64397346],
    [ 0.23339166,  0.14897137,  0.64456048],
    [ 0.22927127,  0.15738602,  0.64474476],
    [ 0.22501278,  0.16563165,  0.64452595],
    [ 0.22063349,  0.17371215,  0.64390834],
    [ 0.21616055,  0.18162302,  0.64290515],
    [ 0.21161851,  0.18936156,  0.64153295],
    [ 0.20703353,  0.19692415,  0.63981287],
    [ 0.20243273,  0.20430706,  0.63776986],
    [ 0.19784363,  0.211507  ,  0.63543183],
    [ 0.19329361,  0.21852157,  0.63282872],
    [ 0.18880937,  0.2253495 ,  0.62999156],
    [ 0.18442119,  0.23198815,  0.62695569],
    [ 0.18014936,  0.23844124,  0.62374886],
    [ 0.17601569,  0.24471172,  0.62040016],
    [ 0.17204028,  0.25080356,  0.61693715],
    [ 0.16824123,  0.25672163,  0.6133854 ],
    [ 0.16463462,  0.26247158,  0.60976836],
    [ 0.16123449,  0.26805963,  0.60610723],
    [ 0.15805279,  0.27349243,  0.60242099],
    [ 0.15509948,  0.27877688,  0.59872645],
    [ 0.15238249,  0.28392004,  0.59503836],
    [ 0.14990781,  0.28892902,  0.59136956],
    [ 0.14767951,  0.29381086,  0.58773113],
    [ 0.14569979,  0.29857245,  0.58413255],
    [ 0.1439691 ,  0.30322055,  0.58058191],
    [ 0.14248613,  0.30776167,  0.57708599],
    [ 0.14124797,  0.31220208,  0.57365049],
    [ 0.14025018,  0.31654779,  0.57028011],
    [ 0.13948691,  0.32080454,  0.5669787 ],
    [ 0.13895174,  0.32497744,  0.56375063],
    [ 0.13863958,  0.32907012,  0.56060453],
    [ 0.138537  ,  0.3330895 ,  0.55753513],
    [ 0.13863384,  0.33704026,  0.55454374],
    [ 0.13891931,  0.34092684,  0.55163126],
    [ 0.13938212,  0.34475344,  0.54879827],
    [ 0.14001061,  0.34852402,  0.54604503],
    [ 0.14079292,  0.35224233,  0.54337156],
    [ 0.14172091,  0.35590982,  0.54078769],
    [ 0.14277848,  0.35953205,  0.53828312],
    [ 0.14395358,  0.36311234,  0.53585661],
    [ 0.1452346 ,  0.36665374,  0.5335074 ],
    [ 0.14661019,  0.3701591 ,  0.5312346 ],
    [ 0.14807104,  0.37363011,  0.52904278],
    [ 0.1496059 ,  0.3770697 ,  0.52692951],
    [ 0.15120289,  0.3804813 ,  0.52488853],
    [ 0.15285214,  0.38386729,  0.52291854],
    [ 0.15454421,  0.38722991,  0.52101815],
    [ 0.15627225,  0.39056998,  0.5191937 ],
    [ 0.15802555,  0.39389087,  0.5174364 ],
    [ 0.15979549,  0.39719482,  0.51574311],
    [ 0.16157425,  0.40048375,  0.51411214],
    [ 0.16335571,  0.40375871,  0.51254622],
    [ 0.16513234,  0.40702178,  0.51104174],
    [ 0.1668964 ,  0.41027528,  0.50959299],
    [ 0.16864151,  0.41352084,  0.50819797],
    [ 0.17036277,  0.41675941,  0.50685814],
    [ 0.1720542 ,  0.41999269,  0.50557008],
    [ 0.17370932,  0.42322271,  0.50432818],
    [ 0.17532301,  0.42645082,  0.50313007],
    [ 0.17689176,  0.42967776,  0.50197686],
    [ 0.17841013,  0.43290523,  0.5008633 ],
    [ 0.17987314,  0.43613477,  0.49978492],
    [ 0.18127676,  0.43936752,  0.49873901],
    [ 0.18261885,  0.44260392,  0.49772638],
    [ 0.18389409,  0.44584578,  0.49673978],
    [ 0.18509911,  0.44909409,  0.49577605],
    [ 0.18623135,  0.4523496 ,  0.494833  ],
    [ 0.18728844,  0.45561305,  0.49390803],
    [ 0.18826671,  0.45888565,  0.49299567],
    [ 0.18916393,  0.46216809,  0.49209268],
    [ 0.18997879,  0.46546084,  0.49119678],
    [ 0.19070881,  0.46876472,  0.49030328],
    [ 0.19135221,  0.47208035,  0.48940827],
    [ 0.19190791,  0.47540815,  0.48850845],
    [ 0.19237491,  0.47874852,  0.4876002 ],
    [ 0.19275204,  0.48210192,  0.48667935],
    [ 0.19303899,  0.48546858,  0.48574251],
    [ 0.19323526,  0.48884877,  0.48478573],
    [ 0.19334062,  0.49224271,  0.48380506],
    [ 0.19335574,  0.49565037,  0.4827974 ],
    [ 0.19328143,  0.49907173,  0.48175948],
    [ 0.19311664,  0.50250719,  0.48068559],
    [ 0.192864  ,  0.50595628,  0.47957408],
    [ 0.19252521,  0.50941877,  0.47842186],
    [ 0.19210087,  0.51289469,  0.47722441],
    [ 0.19159194,  0.516384  ,  0.47597744],
    [ 0.19100267,  0.51988593,  0.47467988],
    [ 0.19033595,  0.52340005,  0.47332894],
    [ 0.18959113,  0.5269267 ,  0.47191795],
    [ 0.18877336,  0.530465  ,  0.47044603],
    [ 0.18788765,  0.53401416,  0.46891178],
    [ 0.18693822,  0.53757359,  0.46731272],
    [ 0.18592276,  0.54114404,  0.46563962],
    [ 0.18485204,  0.54472367,  0.46389595],
    [ 0.18373148,  0.5483118 ,  0.46207951],
    [ 0.18256585,  0.55190791,  0.4601871 ],
    [ 0.18135481,  0.55551253,  0.45821002],
    [ 0.18011172,  0.55912361,  0.45615277],
    [ 0.17884392,  0.56274038,  0.45401341],
    [ 0.17755858,  0.56636217,  0.45178933],
    [ 0.17625543,  0.56998972,  0.44946971],
    [ 0.174952  ,  0.57362064,  0.44706119],
    [ 0.17365805,  0.57725408,  0.44456198],
    [ 0.17238403,  0.58088916,  0.4419703 ],
    [ 0.17113321,  0.58452637,  0.43927576],
    [ 0.1699221 ,  0.58816399,  0.43648119],
    [ 0.1687662 ,  0.5918006 ,  0.43358772],
    [ 0.16767908,  0.59543526,  0.43059358],
    [ 0.16667511,  0.59906699,  0.42749697],
    [ 0.16575939,  0.60269653,  0.42428344],
    [ 0.16495764,  0.6063212 ,  0.42096245],
    [ 0.16428695,  0.60993988,  0.41753246],
    [ 0.16376481,  0.61355147,  0.41399151],
    [ 0.16340924,  0.61715487,  0.41033757],
    [ 0.16323549,  0.62074951,  0.40656329],
    [ 0.16326148,  0.62433443,  0.40266378],
    [ 0.16351136,  0.62790748,  0.39864431],
    [ 0.16400433,  0.63146734,  0.39450263],
    [ 0.16475937,  0.63501264,  0.39023638],
    [ 0.16579502,  0.63854196,  0.38584309],
    [ 0.16712921,  0.64205381,  0.38132023],
    [ 0.168779  ,  0.64554661,  0.37666513],
    [ 0.17075915,  0.64901912,  0.37186962],
    [ 0.17308572,  0.65246934,  0.36693299],
    [ 0.1757732 ,  0.65589512,  0.36185643],
    [ 0.17883344,  0.65929449,  0.3566372 ],
    [ 0.18227669,  0.66266536,  0.35127251],
    [ 0.18611159,  0.66600553,  0.34575959],
    [ 0.19034516,  0.66931265,  0.34009571],
    [ 0.19498285,  0.67258423,  0.3342782 ],
    [ 0.20002863,  0.67581761,  0.32830456],
    [ 0.20548509,  0.67900997,  0.3221725 ],
    [ 0.21135348,  0.68215834,  0.31587999],
    [ 0.2176339 ,  0.68525954,  0.30942543],
    [ 0.22432532,  0.68831023,  0.30280771],
    [ 0.23142568,  0.69130688,  0.29602636],
    [ 0.23893914,  0.69424565,  0.28906643],
    [ 0.2468574 ,  0.69712255,  0.28194103],
    [ 0.25517514,  0.69993351,  0.27465372],
    [ 0.26388625,  0.70267437,  0.26720869],
    [ 0.27298333,  0.70534087,  0.25961196],
    [ 0.28246016,  0.70792854,  0.25186761],
    [ 0.29232159,  0.71043184,  0.2439642 ],
    [ 0.30253943,  0.71284765,  0.23594089],
    [ 0.31309875,  0.71517209,  0.22781515],
    [ 0.32399522,  0.71740028,  0.21959115],
    [ 0.33520729,  0.71952906,  0.21129816],
    [ 0.3467003 ,  0.72155723,  0.20298257],
    [ 0.35846225,  0.72348143,  0.19466318],
    [ 0.3704552 ,  0.72530195,  0.18639333],
    [ 0.38264126,  0.72702007,  0.17822762],
    [ 0.39499483,  0.72863609,  0.17020921],
    [ 0.40746591,  0.73015499,  0.1624122 ],
    [ 0.42001969,  0.73158058,  0.15489659],
    [ 0.43261504,  0.73291878,  0.14773267],
    [ 0.44521378,  0.73417623,  0.14099043],
    [ 0.45777768,  0.73536072,  0.13474173],
    [ 0.47028295,  0.73647823,  0.1290455 ],
    [ 0.48268544,  0.73753985,  0.12397794],
    [ 0.49497773,  0.73854983,  0.11957878],
    [ 0.5071369 ,  0.73951621,  0.11589589],
    [ 0.51913764,  0.74044827,  0.11296861],
    [ 0.53098624,  0.74134823,  0.11080237],
    [ 0.5426701 ,  0.74222288,  0.10940411],
    [ 0.55417235,  0.74308049,  0.10876749],
    [ 0.56550904,  0.74392086,  0.10885609],
    [ 0.57667994,  0.74474781,  0.10963233],
    [ 0.58767906,  0.74556676,  0.11105089],
    [ 0.59850723,  0.74638125,  0.1130567 ],
    [ 0.609179  ,  0.74719067,  0.11558918],
    [ 0.61969877,  0.74799703,  0.11859042],
    [ 0.63007148,  0.74880206,  0.12200388],
    [ 0.64030249,  0.74960714,  0.12577596],
    [ 0.65038997,  0.75041586,  0.12985641],
    [ 0.66034774,  0.75122659,  0.1342004 ],
    [ 0.67018264,  0.75203968,  0.13876817],
    [ 0.67990043,  0.75285567,  0.14352456],
    [ 0.68950682,  0.75367492,  0.14843886],
    [ 0.69900745,  0.75449768,  0.15348445],
    [ 0.70840781,  0.75532408,  0.15863839],
    [ 0.71771325,  0.75615416,  0.16388098],
    [ 0.72692898,  0.75698787,  0.1691954 ],
    [ 0.73606001,  0.75782508,  0.17456729],
    [ 0.74511119,  0.75866562,  0.17998443],
    [ 0.75408719,  0.75950924,  0.18543644],
    [ 0.76299247,  0.76035568,  0.19091446],
    [ 0.77183123,  0.76120466,  0.19641095],
    [ 0.78060815,  0.76205561,  0.20191973],
    [ 0.78932717,  0.76290815,  0.20743538],
    [ 0.79799213,  0.76376186,  0.21295324],
    [ 0.8066067 ,  0.76461631,  0.21846931],
    [ 0.81517444,  0.76547101,  0.22398014],
    [ 0.82369877,  0.76632547,  0.2294827 ],
    [ 0.832183  ,  0.7671792 ,  0.2349743 ],
    [ 0.8406303 ,  0.76803167,  0.24045248],
    [ 0.84904371,  0.76888236,  0.24591492],
    [ 0.85742615,  0.76973076,  0.25135935],
    [ 0.86578037,  0.77057636,  0.25678342],
    [ 0.87410891,  0.77141875,  0.2621846 ],
    [ 0.88241406,  0.77225757,  0.26755999],
    [ 0.89070781,  0.77308772,  0.27291122],
    [ 0.89898836,  0.77391069,  0.27823228],
    [ 0.90725475,  0.77472764,  0.28351668],
    [ 0.91550775,  0.77553893,  0.28875751],
    [ 0.92375722,  0.7763404 ,  0.29395046],
    [ 0.9320227 ,  0.77712286,  0.29909267],
    [ 0.94027715,  0.7779011 ,  0.30415428],
    [ 0.94856742,  0.77865213,  0.3091325 ],
    [ 0.95686038,  0.7793949 ,  0.31397459],
    [ 0.965222  ,  0.7800975 ,  0.31864342],
    [ 0.97365189,  0.78076521,  0.32301107],
    [ 0.98227405,  0.78134549,  0.32678728],
    [ 0.99136564,  0.78176999,  0.3281624 ],
    [ 0.99505988,  0.78542889,  0.32106514],
    [ 0.99594185,  0.79046888,  0.31648808],
    [ 0.99646635,  0.79566972,  0.31244662],
    [ 0.99681528,  0.80094905,  0.30858532],
    [ 0.9970578 ,  0.80627441,  0.30479247],
    [ 0.99724883,  0.81161757,  0.30105328],
    [ 0.99736711,  0.81699344,  0.29725528],
    [ 0.99742254,  0.82239736,  0.29337235],
    [ 0.99744736,  0.82781159,  0.28943391],
    [ 0.99744951,  0.83323244,  0.28543062],
    [ 0.9973953 ,  0.83867931,  0.2812767 ],
    [ 0.99727248,  0.84415897,  0.27692897],
    [ 0.99713953,  0.84963903,  0.27248698],
    [ 0.99698641,  0.85512544,  0.26791703],
    [ 0.99673736,  0.86065927,  0.26304767],
    [ 0.99652358,  0.86616957,  0.25813608],
    [ 0.99622774,  0.87171946,  0.25292044],
    [ 0.99590494,  0.87727931,  0.24750009],
    [ 0.99555225,  0.88285068,  0.2418514 ],
    [ 0.99513763,  0.8884501 ,  0.23588062],
    [ 0.99471252,  0.89405076,  0.2296837 ],
    [ 0.99421873,  0.89968246,  0.2230963 ],
    [ 0.99370185,  0.90532165,  0.21619768],
    [ 0.99313786,  0.91098038,  0.2088926 ],
    [ 0.99250707,  0.91666811,  0.20108214],
    [ 0.99187888,  0.92235023,  0.19290417],
    [ 0.99110991,  0.92809686,  0.18387963],
    [ 0.99042108,  0.93379995,  0.17458127],
    [ 0.98958484,  0.93956962,  0.16420166],
    [ 0.98873988,  0.94533859,  0.15303117],
    [ 0.98784836,  0.95112482,  0.14074826],
    [ 0.98680727,  0.95697596,  0.12661626]]

cm_data_viridis = [
    [ 0.26700401,  0.00487433,  0.32941519],
    [ 0.26851048,  0.00960483,  0.33542652],
    [ 0.26994384,  0.01462494,  0.34137895],
    [ 0.27130489,  0.01994186,  0.34726862],
    [ 0.27259384,  0.02556309,  0.35309303],
    [ 0.27380934,  0.03149748,  0.35885256],
    [ 0.27495242,  0.03775181,  0.36454323],
    [ 0.27602238,  0.04416723,  0.37016418],
    [ 0.2770184 ,  0.05034437,  0.37571452],
    [ 0.27794143,  0.05632444,  0.38119074],
    [ 0.27879067,  0.06214536,  0.38659204],
    [ 0.2795655 ,  0.06783587,  0.39191723],
    [ 0.28026658,  0.07341724,  0.39716349],
    [ 0.28089358,  0.07890703,  0.40232944],
    [ 0.28144581,  0.0843197 ,  0.40741404],
    [ 0.28192358,  0.08966622,  0.41241521],
    [ 0.28232739,  0.09495545,  0.41733086],
    [ 0.28265633,  0.10019576,  0.42216032],
    [ 0.28291049,  0.10539345,  0.42690202],
    [ 0.28309095,  0.11055307,  0.43155375],
    [ 0.28319704,  0.11567966,  0.43611482],
    [ 0.28322882,  0.12077701,  0.44058404],
    [ 0.28318684,  0.12584799,  0.44496   ],
    [ 0.283072  ,  0.13089477,  0.44924127],
    [ 0.28288389,  0.13592005,  0.45342734],
    [ 0.28262297,  0.14092556,  0.45751726],
    [ 0.28229037,  0.14591233,  0.46150995],
    [ 0.28188676,  0.15088147,  0.46540474],
    [ 0.28141228,  0.15583425,  0.46920128],
    [ 0.28086773,  0.16077132,  0.47289909],
    [ 0.28025468,  0.16569272,  0.47649762],
    [ 0.27957399,  0.17059884,  0.47999675],
    [ 0.27882618,  0.1754902 ,  0.48339654],
    [ 0.27801236,  0.18036684,  0.48669702],
    [ 0.27713437,  0.18522836,  0.48989831],
    [ 0.27619376,  0.19007447,  0.49300074],
    [ 0.27519116,  0.1949054 ,  0.49600488],
    [ 0.27412802,  0.19972086,  0.49891131],
    [ 0.27300596,  0.20452049,  0.50172076],
    [ 0.27182812,  0.20930306,  0.50443413],
    [ 0.27059473,  0.21406899,  0.50705243],
    [ 0.26930756,  0.21881782,  0.50957678],
    [ 0.26796846,  0.22354911,  0.5120084 ],
    [ 0.26657984,  0.2282621 ,  0.5143487 ],
    [ 0.2651445 ,  0.23295593,  0.5165993 ],
    [ 0.2636632 ,  0.23763078,  0.51876163],
    [ 0.26213801,  0.24228619,  0.52083736],
    [ 0.26057103,  0.2469217 ,  0.52282822],
    [ 0.25896451,  0.25153685,  0.52473609],
    [ 0.25732244,  0.2561304 ,  0.52656332],
    [ 0.25564519,  0.26070284,  0.52831152],
    [ 0.25393498,  0.26525384,  0.52998273],
    [ 0.25219404,  0.26978306,  0.53157905],
    [ 0.25042462,  0.27429024,  0.53310261],
    [ 0.24862899,  0.27877509,  0.53455561],
    [ 0.2468114 ,  0.28323662,  0.53594093],
    [ 0.24497208,  0.28767547,  0.53726018],
    [ 0.24311324,  0.29209154,  0.53851561],
    [ 0.24123708,  0.29648471,  0.53970946],
    [ 0.23934575,  0.30085494,  0.54084398],
    [ 0.23744138,  0.30520222,  0.5419214 ],
    [ 0.23552606,  0.30952657,  0.54294396],
    [ 0.23360277,  0.31382773,  0.54391424],
    [ 0.2316735 ,  0.3181058 ,  0.54483444],
    [ 0.22973926,  0.32236127,  0.54570633],
    [ 0.22780192,  0.32659432,  0.546532  ],
    [ 0.2258633 ,  0.33080515,  0.54731353],
    [ 0.22392515,  0.334994  ,  0.54805291],
    [ 0.22198915,  0.33916114,  0.54875211],
    [ 0.22005691,  0.34330688,  0.54941304],
    [ 0.21812995,  0.34743154,  0.55003755],
    [ 0.21620971,  0.35153548,  0.55062743],
    [ 0.21429757,  0.35561907,  0.5511844 ],
    [ 0.21239477,  0.35968273,  0.55171011],
    [ 0.2105031 ,  0.36372671,  0.55220646],
    [ 0.20862342,  0.36775151,  0.55267486],
    [ 0.20675628,  0.37175775,  0.55311653],
    [ 0.20490257,  0.37574589,  0.55353282],
    [ 0.20306309,  0.37971644,  0.55392505],
    [ 0.20123854,  0.38366989,  0.55429441],
    [ 0.1994295 ,  0.38760678,  0.55464205],
    [ 0.1976365 ,  0.39152762,  0.55496905],
    [ 0.19585993,  0.39543297,  0.55527637],
    [ 0.19410009,  0.39932336,  0.55556494],
    [ 0.19235719,  0.40319934,  0.55583559],
    [ 0.19063135,  0.40706148,  0.55608907],
    [ 0.18892259,  0.41091033,  0.55632606],
    [ 0.18723083,  0.41474645,  0.55654717],
    [ 0.18555593,  0.4185704 ,  0.55675292],
    [ 0.18389763,  0.42238275,  0.55694377],
    [ 0.18225561,  0.42618405,  0.5571201 ],
    [ 0.18062949,  0.42997486,  0.55728221],
    [ 0.17901879,  0.43375572,  0.55743035],
    [ 0.17742298,  0.4375272 ,  0.55756466],
    [ 0.17584148,  0.44128981,  0.55768526],
    [ 0.17427363,  0.4450441 ,  0.55779216],
    [ 0.17271876,  0.4487906 ,  0.55788532],
    [ 0.17117615,  0.4525298 ,  0.55796464],
    [ 0.16964573,  0.45626209,  0.55803034],
    [ 0.16812641,  0.45998802,  0.55808199],
    [ 0.1666171 ,  0.46370813,  0.55811913],
    [ 0.16511703,  0.4674229 ,  0.55814141],
    [ 0.16362543,  0.47113278,  0.55814842],
    [ 0.16214155,  0.47483821,  0.55813967],
    [ 0.16066467,  0.47853961,  0.55811466],
    [ 0.15919413,  0.4822374 ,  0.5580728 ],
    [ 0.15772933,  0.48593197,  0.55801347],
    [ 0.15626973,  0.4896237 ,  0.557936  ],
    [ 0.15481488,  0.49331293,  0.55783967],
    [ 0.15336445,  0.49700003,  0.55772371],
    [ 0.1519182 ,  0.50068529,  0.55758733],
    [ 0.15047605,  0.50436904,  0.55742968],
    [ 0.14903918,  0.50805136,  0.5572505 ],
    [ 0.14760731,  0.51173263,  0.55704861],
    [ 0.14618026,  0.51541316,  0.55682271],
    [ 0.14475863,  0.51909319,  0.55657181],
    [ 0.14334327,  0.52277292,  0.55629491],
    [ 0.14193527,  0.52645254,  0.55599097],
    [ 0.14053599,  0.53013219,  0.55565893],
    [ 0.13914708,  0.53381201,  0.55529773],
    [ 0.13777048,  0.53749213,  0.55490625],
    [ 0.1364085 ,  0.54117264,  0.55448339],
    [ 0.13506561,  0.54485335,  0.55402906],
    [ 0.13374299,  0.54853458,  0.55354108],
    [ 0.13244401,  0.55221637,  0.55301828],
    [ 0.13117249,  0.55589872,  0.55245948],
    [ 0.1299327 ,  0.55958162,  0.55186354],
    [ 0.12872938,  0.56326503,  0.55122927],
    [ 0.12756771,  0.56694891,  0.55055551],
    [ 0.12645338,  0.57063316,  0.5498411 ],
    [ 0.12539383,  0.57431754,  0.54908564],
    [ 0.12439474,  0.57800205,  0.5482874 ],
    [ 0.12346281,  0.58168661,  0.54744498],
    [ 0.12260562,  0.58537105,  0.54655722],
    [ 0.12183122,  0.58905521,  0.54562298],
    [ 0.12114807,  0.59273889,  0.54464114],
    [ 0.12056501,  0.59642187,  0.54361058],
    [ 0.12009154,  0.60010387,  0.54253043],
    [ 0.11973756,  0.60378459,  0.54139999],
    [ 0.11951163,  0.60746388,  0.54021751],
    [ 0.11942341,  0.61114146,  0.53898192],
    [ 0.11948255,  0.61481702,  0.53769219],
    [ 0.11969858,  0.61849025,  0.53634733],
    [ 0.12008079,  0.62216081,  0.53494633],
    [ 0.12063824,  0.62582833,  0.53348834],
    [ 0.12137972,  0.62949242,  0.53197275],
    [ 0.12231244,  0.63315277,  0.53039808],
    [ 0.12344358,  0.63680899,  0.52876343],
    [ 0.12477953,  0.64046069,  0.52706792],
    [ 0.12632581,  0.64410744,  0.52531069],
    [ 0.12808703,  0.64774881,  0.52349092],
    [ 0.13006688,  0.65138436,  0.52160791],
    [ 0.13226797,  0.65501363,  0.51966086],
    [ 0.13469183,  0.65863619,  0.5176488 ],
    [ 0.13733921,  0.66225157,  0.51557101],
    [ 0.14020991,  0.66585927,  0.5134268 ],
    [ 0.14330291,  0.66945881,  0.51121549],
    [ 0.1466164 ,  0.67304968,  0.50893644],
    [ 0.15014782,  0.67663139,  0.5065889 ],
    [ 0.15389405,  0.68020343,  0.50417217],
    [ 0.15785146,  0.68376525,  0.50168574],
    [ 0.16201598,  0.68731632,  0.49912906],
    [ 0.1663832 ,  0.69085611,  0.49650163],
    [ 0.1709484 ,  0.69438405,  0.49380294],
    [ 0.17570671,  0.6978996 ,  0.49103252],
    [ 0.18065314,  0.70140222,  0.48818938],
    [ 0.18578266,  0.70489133,  0.48527326],
    [ 0.19109018,  0.70836635,  0.48228395],
    [ 0.19657063,  0.71182668,  0.47922108],
    [ 0.20221902,  0.71527175,  0.47608431],
    [ 0.20803045,  0.71870095,  0.4728733 ],
    [ 0.21400015,  0.72211371,  0.46958774],
    [ 0.22012381,  0.72550945,  0.46622638],
    [ 0.2263969 ,  0.72888753,  0.46278934],
    [ 0.23281498,  0.73224735,  0.45927675],
    [ 0.2393739 ,  0.73558828,  0.45568838],
    [ 0.24606968,  0.73890972,  0.45202405],
    [ 0.25289851,  0.74221104,  0.44828355],
    [ 0.25985676,  0.74549162,  0.44446673],
    [ 0.26694127,  0.74875084,  0.44057284],
    [ 0.27414922,  0.75198807,  0.4366009 ],
    [ 0.28147681,  0.75520266,  0.43255207],
    [ 0.28892102,  0.75839399,  0.42842626],
    [ 0.29647899,  0.76156142,  0.42422341],
    [ 0.30414796,  0.76470433,  0.41994346],
    [ 0.31192534,  0.76782207,  0.41558638],
    [ 0.3198086 ,  0.77091403,  0.41115215],
    [ 0.3277958 ,  0.77397953,  0.40664011],
    [ 0.33588539,  0.7770179 ,  0.40204917],
    [ 0.34407411,  0.78002855,  0.39738103],
    [ 0.35235985,  0.78301086,  0.39263579],
    [ 0.36074053,  0.78596419,  0.38781353],
    [ 0.3692142 ,  0.78888793,  0.38291438],
    [ 0.37777892,  0.79178146,  0.3779385 ],
    [ 0.38643282,  0.79464415,  0.37288606],
    [ 0.39517408,  0.79747541,  0.36775726],
    [ 0.40400101,  0.80027461,  0.36255223],
    [ 0.4129135 ,  0.80304099,  0.35726893],
    [ 0.42190813,  0.80577412,  0.35191009],
    [ 0.43098317,  0.80847343,  0.34647607],
    [ 0.44013691,  0.81113836,  0.3409673 ],
    [ 0.44936763,  0.81376835,  0.33538426],
    [ 0.45867362,  0.81636288,  0.32972749],
    [ 0.46805314,  0.81892143,  0.32399761],
    [ 0.47750446,  0.82144351,  0.31819529],
    [ 0.4870258 ,  0.82392862,  0.31232133],
    [ 0.49661536,  0.82637633,  0.30637661],
    [ 0.5062713 ,  0.82878621,  0.30036211],
    [ 0.51599182,  0.83115784,  0.29427888],
    [ 0.52577622,  0.83349064,  0.2881265 ],
    [ 0.5356211 ,  0.83578452,  0.28190832],
    [ 0.5455244 ,  0.83803918,  0.27562602],
    [ 0.55548397,  0.84025437,  0.26928147],
    [ 0.5654976 ,  0.8424299 ,  0.26287683],
    [ 0.57556297,  0.84456561,  0.25641457],
    [ 0.58567772,  0.84666139,  0.24989748],
    [ 0.59583934,  0.84871722,  0.24332878],
    [ 0.60604528,  0.8507331 ,  0.23671214],
    [ 0.61629283,  0.85270912,  0.23005179],
    [ 0.62657923,  0.85464543,  0.22335258],
    [ 0.63690157,  0.85654226,  0.21662012],
    [ 0.64725685,  0.85839991,  0.20986086],
    [ 0.65764197,  0.86021878,  0.20308229],
    [ 0.66805369,  0.86199932,  0.19629307],
    [ 0.67848868,  0.86374211,  0.18950326],
    [ 0.68894351,  0.86544779,  0.18272455],
    [ 0.69941463,  0.86711711,  0.17597055],
    [ 0.70989842,  0.86875092,  0.16925712],
    [ 0.72039115,  0.87035015,  0.16260273],
    [ 0.73088902,  0.87191584,  0.15602894],
    [ 0.74138803,  0.87344918,  0.14956101],
    [ 0.75188414,  0.87495143,  0.14322828],
    [ 0.76237342,  0.87642392,  0.13706449],
    [ 0.77285183,  0.87786808,  0.13110864],
    [ 0.78331535,  0.87928545,  0.12540538],
    [ 0.79375994,  0.88067763,  0.12000532],
    [ 0.80418159,  0.88204632,  0.11496505],
    [ 0.81457634,  0.88339329,  0.11034678],
    [ 0.82494028,  0.88472036,  0.10621724],
    [ 0.83526959,  0.88602943,  0.1026459 ],
    [ 0.84556056,  0.88732243,  0.09970219],
    [ 0.8558096 ,  0.88860134,  0.09745186],
    [ 0.86601325,  0.88986815,  0.09595277],
    [ 0.87616824,  0.89112487,  0.09525046],
    [ 0.88627146,  0.89237353,  0.09537439],
    [ 0.89632002,  0.89361614,  0.09633538],
    [ 0.90631121,  0.89485467,  0.09812496],
    [ 0.91624212,  0.89609127,  0.1007168 ],
    [ 0.92610579,  0.89732977,  0.10407067],
    [ 0.93590444,  0.8985704 ,  0.10813094],
    [ 0.94563626,  0.899815  ,  0.11283773],
    [ 0.95529972,  0.90106534,  0.11812832],
    [ 0.96489353,  0.90232311,  0.12394051],
    [ 0.97441665,  0.90358991,  0.13021494],
    [ 0.98386829,  0.90486726,  0.13689671],
    [ 0.99324789,  0.90615657,  0.1439362 ]]

cm_data_turbo = [
    [ 0.18995,     0.07176,     0.23217],
    [ 0.19483,     0.08339,     0.26149],
    [ 0.19956,     0.09498,     0.29024],
    [ 0.20415,     0.10652,     0.31844],
    [ 0.20860,     0.11802,     0.34607],
    [ 0.21291,     0.12947,     0.37314],
    [ 0.21708,     0.14087,     0.39964],
    [ 0.22111,     0.15223,     0.42558],
    [ 0.22500,     0.16354,     0.45096],
    [ 0.22875,     0.17481,     0.47578],
    [ 0.23236,     0.18603,     0.50004],
    [ 0.23582,     0.19720,     0.52373],
    [ 0.23915,     0.20833,     0.54686],
    [ 0.24234,     0.21941,     0.56942],
    [ 0.24539,     0.23044,     0.59142],
    [ 0.24830,     0.24143,     0.61286],
    [ 0.25107,     0.25237,     0.63374],
    [ 0.25369,     0.26327,     0.65406],
    [ 0.25618,     0.27412,     0.67381],
    [ 0.25853,     0.28492,     0.69300],
    [ 0.26074,     0.29568,     0.71162],
    [ 0.26280,     0.30639,     0.72968],
    [ 0.26473,     0.31706,     0.74718],
    [ 0.26652,     0.32768,     0.76412],
    [ 0.26816,     0.33825,     0.78050],
    [ 0.26967,     0.34878,     0.79631],
    [ 0.27103,     0.35926,     0.81156],
    [ 0.27226,     0.36970,     0.82624],
    [ 0.27334,     0.38008,     0.84037],
    [ 0.27429,     0.39043,     0.85393],
    [ 0.27509,     0.40072,     0.86692],
    [ 0.27576,     0.41097,     0.87936],
    [ 0.27628,     0.42118,     0.89123],
    [ 0.27667,     0.43134,     0.90254],
    [ 0.27691,     0.44145,     0.91328],
    [ 0.27701,     0.45152,     0.92347],
    [ 0.27698,     0.46153,     0.93309],
    [ 0.27680,     0.47151,     0.94214],
    [ 0.27648,     0.48144,     0.95064],
    [ 0.27603,     0.49132,     0.95857],
    [ 0.27543,     0.50115,     0.96594],
    [ 0.27469,     0.51094,     0.97275],
    [ 0.27381,     0.52069,     0.97899],
    [ 0.27273,     0.53040,     0.98461],
    [ 0.27106,     0.54015,     0.98930],
    [ 0.26878,     0.54995,     0.99303],
    [ 0.26592,     0.55979,     0.99583],
    [ 0.26252,     0.56967,     0.99773],
    [ 0.25862,     0.57958,     0.99876],
    [ 0.25425,     0.58950,     0.99896],
    [ 0.24946,     0.59943,     0.99835],
    [ 0.24427,     0.60937,     0.99697],
    [ 0.23874,     0.61931,     0.99485],
    [ 0.23288,     0.62923,     0.99202],
    [ 0.22676,     0.63913,     0.98851],
    [ 0.22039,     0.64901,     0.98436],
    [ 0.21382,     0.65886,     0.97959],
    [ 0.20708,     0.66866,     0.97423],
    [ 0.20021,     0.67842,     0.96833],
    [ 0.19326,     0.68812,     0.96190],
    [ 0.18625,     0.69775,     0.95498],
    [ 0.17923,     0.70732,     0.94761],
    [ 0.17223,     0.71680,     0.93981],
    [ 0.16529,     0.72620,     0.93161],
    [ 0.15844,     0.73551,     0.92305],
    [ 0.15173,     0.74472,     0.91416],
    [ 0.14519,     0.75381,     0.90496],
    [ 0.13886,     0.76279,     0.89550],
    [ 0.13278,     0.77165,     0.88580],
    [ 0.12698,     0.78037,     0.87590],
    [ 0.12151,     0.78896,     0.86581],
    [ 0.11639,     0.79740,     0.85559],
    [ 0.11167,     0.80569,     0.84525],
    [ 0.10738,     0.81381,     0.83484],
    [ 0.10357,     0.82177,     0.82437],
    [ 0.10026,     0.82955,     0.81389],
    [ 0.09750,     0.83714,     0.80342],
    [ 0.09532,     0.84455,     0.79299],
    [ 0.09377,     0.85175,     0.78264],
    [ 0.09287,     0.85875,     0.77240],
    [ 0.09267,     0.86554,     0.76230],
    [ 0.09320,     0.87211,     0.75237],
    [ 0.09451,     0.87844,     0.74265],
    [ 0.09662,     0.88454,     0.73316],
    [ 0.09958,     0.89040,     0.72393],
    [ 0.10342,     0.89600,     0.71500],
    [ 0.10815,     0.90142,     0.70599],
    [ 0.11374,     0.90673,     0.69651],
    [ 0.12014,     0.91193,     0.68660],
    [ 0.12733,     0.91701,     0.67627],
    [ 0.13526,     0.92197,     0.66556],
    [ 0.14391,     0.92680,     0.65448],
    [ 0.15323,     0.93151,     0.64308],
    [ 0.16319,     0.93609,     0.63137],
    [ 0.17377,     0.94053,     0.61938],
    [ 0.18491,     0.94484,     0.60713],
    [ 0.19659,     0.94901,     0.59466],
    [ 0.20877,     0.95304,     0.58199],
    [ 0.22142,     0.95692,     0.56914],
    [ 0.23449,     0.96065,     0.55614],
    [ 0.24797,     0.96423,     0.54303],
    [ 0.26180,     0.96765,     0.52981],
    [ 0.27597,     0.97092,     0.51653],
    [ 0.29042,     0.97403,     0.50321],
    [ 0.30513,     0.97697,     0.48987],
    [ 0.32006,     0.97974,     0.47654],
    [ 0.33517,     0.98234,     0.46325],
    [ 0.35043,     0.98477,     0.45002],
    [ 0.36581,     0.98702,     0.43688],
    [ 0.38127,     0.98909,     0.42386],
    [ 0.39678,     0.99098,     0.41098],
    [ 0.41229,     0.99268,     0.39826],
    [ 0.42778,     0.99419,     0.38575],
    [ 0.44321,     0.99551,     0.37345],
    [ 0.45854,     0.99663,     0.36140],
    [ 0.47375,     0.99755,     0.34963],
    [ 0.48879,     0.99828,     0.33816],
    [ 0.50362,     0.99879,     0.32701],
    [ 0.51822,     0.99910,     0.31622],
    [ 0.53255,     0.99919,     0.30581],
    [ 0.54658,     0.99907,     0.29581],
    [ 0.56026,     0.99873,     0.28623],
    [ 0.57357,     0.99817,     0.27712],
    [ 0.58646,     0.99739,     0.26849],
    [ 0.59891,     0.99638,     0.26038],
    [ 0.61088,     0.99514,     0.25280],
    [ 0.62233,     0.99366,     0.24579],
    [ 0.63323,     0.99195,     0.23937],
    [ 0.64362,     0.98999,     0.23356],
    [ 0.65394,     0.98775,     0.22835],
    [ 0.66428,     0.98524,     0.22370],
    [ 0.67462,     0.98246,     0.21960],
    [ 0.68494,     0.97941,     0.21602],
    [ 0.69525,     0.97610,     0.21294],
    [ 0.70553,     0.97255,     0.21032],
    [ 0.71577,     0.96875,     0.20815],
    [ 0.72596,     0.96470,     0.20640],
    [ 0.73610,     0.96043,     0.20504],
    [ 0.74617,     0.95593,     0.20406],
    [ 0.75617,     0.95121,     0.20343],
    [ 0.76608,     0.94627,     0.20311],
    [ 0.77591,     0.94113,     0.20310],
    [ 0.78563,     0.93579,     0.20336],
    [ 0.79524,     0.93025,     0.20386],
    [ 0.80473,     0.92452,     0.20459],
    [ 0.81410,     0.91861,     0.20552],
    [ 0.82333,     0.91253,     0.20663],
    [ 0.83241,     0.90627,     0.20788],
    [ 0.84133,     0.89986,     0.20926],
    [ 0.85010,     0.89328,     0.21074],
    [ 0.85868,     0.88655,     0.21230],
    [ 0.86709,     0.87968,     0.21391],
    [ 0.87530,     0.87267,     0.21555],
    [ 0.88331,     0.86553,     0.21719],
    [ 0.89112,     0.85826,     0.21880],
    [ 0.89870,     0.85087,     0.22038],
    [ 0.90605,     0.84337,     0.22188],
    [ 0.91317,     0.83576,     0.22328],
    [ 0.92004,     0.82806,     0.22456],
    [ 0.92666,     0.82025,     0.22570],
    [ 0.93301,     0.81236,     0.22667],
    [ 0.93909,     0.80439,     0.22744],
    [ 0.94489,     0.79634,     0.22800],
    [ 0.95039,     0.78823,     0.22831],
    [ 0.95560,     0.78005,     0.22836],
    [ 0.96049,     0.77181,     0.22811],
    [ 0.96507,     0.76352,     0.22754],
    [ 0.96931,     0.75519,     0.22663],
    [ 0.97323,     0.74682,     0.22536],
    [ 0.97679,     0.73842,     0.22369],
    [ 0.98000,     0.73000,     0.22161],
    [ 0.98289,     0.72140,     0.21918],
    [ 0.98549,     0.71250,     0.21650],
    [ 0.98781,     0.70330,     0.21358],
    [ 0.98986,     0.69382,     0.21043],
    [ 0.99163,     0.68408,     0.20706],
    [ 0.99314,     0.67408,     0.20348],
    [ 0.99438,     0.66386,     0.19971],
    [ 0.99535,     0.65341,     0.19577],
    [ 0.99607,     0.64277,     0.19165],
    [ 0.99654,     0.63193,     0.18738],
    [ 0.99675,     0.62093,     0.18297],
    [ 0.99672,     0.60977,     0.17842],
    [ 0.99644,     0.59846,     0.17376],
    [ 0.99593,     0.58703,     0.16899],
    [ 0.99517,     0.57549,     0.16412],
    [ 0.99419,     0.56386,     0.15918],
    [ 0.99297,     0.55214,     0.15417],
    [ 0.99153,     0.54036,     0.14910],
    [ 0.98987,     0.52854,     0.14398],
    [ 0.98799,     0.51667,     0.13883],
    [ 0.98590,     0.50479,     0.13367],
    [ 0.98360,     0.49291,     0.12849],
    [ 0.98108,     0.48104,     0.12332],
    [ 0.97837,     0.46920,     0.11817],
    [ 0.97545,     0.45740,     0.11305],
    [ 0.97234,     0.44565,     0.10797],
    [ 0.96904,     0.43399,     0.10294],
    [ 0.96555,     0.42241,     0.09798],
    [ 0.96187,     0.41093,     0.09310],
    [ 0.95801,     0.39958,     0.08831],
    [ 0.95398,     0.38836,     0.08362],
    [ 0.94977,     0.37729,     0.07905],
    [ 0.94538,     0.36638,     0.07461],
    [ 0.94084,     0.35566,     0.07031],
    [ 0.93612,     0.34513,     0.06616],
    [ 0.93125,     0.33482,     0.06218],
    [ 0.92623,     0.32473,     0.05837],
    [ 0.92105,     0.31489,     0.05475],
    [ 0.91572,     0.30530,     0.05134],
    [ 0.91024,     0.29599,     0.04814],
    [ 0.90463,     0.28696,     0.04516],
    [ 0.89888,     0.27824,     0.04243],
    [ 0.89298,     0.26981,     0.03993],
    [ 0.88691,     0.26152,     0.03753],
    [ 0.88066,     0.25334,     0.03521],
    [ 0.87422,     0.24526,     0.03297],
    [ 0.86760,     0.23730,     0.03082],
    [ 0.86079,     0.22945,     0.02875],
    [ 0.85380,     0.22170,     0.02677],
    [ 0.84662,     0.21407,     0.02487],
    [ 0.83926,     0.20654,     0.02305],
    [ 0.83172,     0.19912,     0.02131],
    [ 0.82399,     0.19182,     0.01966],
    [ 0.81608,     0.18462,     0.01809],
    [ 0.80799,     0.17753,     0.01660],
    [ 0.79971,     0.17055,     0.01520],
    [ 0.79125,     0.16368,     0.01387],
    [ 0.78260,     0.15693,     0.01264],
    [ 0.77377,     0.15028,     0.01148],
    [ 0.76476,     0.14374,     0.01041],
    [ 0.75556,     0.13731,     0.00942],
    [ 0.74617,     0.13098,     0.00851],
    [ 0.73661,     0.12477,     0.00769],
    [ 0.72686,     0.11867,     0.00695],
    [ 0.71692,     0.11268,     0.00629],
    [ 0.70680,     0.10680,     0.00571],
    [ 0.69650,     0.10102,     0.00522],
    [ 0.68602,     0.09536,     0.00481],
    [ 0.67535,     0.08980,     0.00449],
    [ 0.66449,     0.08436,     0.00424],
    [ 0.65345,     0.07902,     0.00408],
    [ 0.64223,     0.07380,     0.00401],
    [ 0.63082,     0.06868,     0.00401],
    [ 0.61923,     0.06367,     0.00410],
    [ 0.60746,     0.05878,     0.00427],
    [ 0.59550,     0.05399,     0.00453],
    [ 0.58336,     0.04931,     0.00486],
    [ 0.57103,     0.04474,     0.00529],
    [ 0.55852,     0.04028,     0.00579],
    [ 0.54583,     0.03593,     0.00638],
    [ 0.53295,     0.03169,     0.00705],
    [ 0.51989,     0.02756,     0.00780],
    [ 0.50664,     0.02354,     0.00863],
    [ 0.49321,     0.01963,     0.00955],
    [ 0.47960,     0.01583,     0.01055]]

def get_colormap(colormap_name: str) -> list:
    if colormap_name.lower() == "parula":
        cm_data = cm_data_parula
    elif colormap_name.lower() == "turbo":
        cm_data = cm_data_turbo
    elif colormap_name.lower == "viridis":
        cm_data = cm_data_viridis
    else:
        raise Exception(f"get_colormap: colormap name {colormap_name} not supported")
    return [QColor(int(255*r), int(255*g), int(255*b)).rgba() for r, g, b in cm_data]
