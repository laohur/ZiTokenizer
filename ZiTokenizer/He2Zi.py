# -*- coding: utf-8 -*-

from logzero import logger
import copy
star = '䖵'

"""
    𤍽	𤑔 k,v  异体字\t本体字
    HeZi[𤑔]=HeZi[𤍽] if 𤍽 in 𤑔
    HeZi[v]=HeZi[k] if k in v
异体字 冃	帽
    """

JieGou = "〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"
# 591
GouJian = "⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻⿼⿽⿾⿿〇〾㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㇤㇥㇦㇧㇨㇩㇪㇫㇬㇭㇮㇯㐄㐅㐫㐱㒳㒼㓁㔾㕯㠯㡀㢴㣇㦰㫃㲋㸦䇂䒑䶹一丁丂七丄丅丆万丈三上下丌与丏丑丘丙业丣严丨丩丬中丮丯丰丱丵丶丷丿乀乁乂乇乑乙乚乛九习乡亅二亍亏五井亜亞亠亥产亯人亻亼亾仌从來侖儿兀兂兆先克入八公六冂冃冄冈冉冋册冎冏冖冘冫几凵刀刂刃刄刅力勹匕北匚匸十卂千卄卅午卌南卜卝卤卩卯厂厃厄厶厷叀又叕叚口史吅咅咼啇喿嘼囗四囟囧囪囱土圥坴堇士壬壴夂夅夆夊夋夌夕夗大夨天夫夬女娄婁子宀寅寸尃小尚尞尢尣尸尺屮屰山屵巛巜川州巠巤工巨己巳巴巾巿帀干幵并幷幺广庚廌廴廾廿开弋弓彐彑彖彡彳心忄戈戉戊戌戍我戶户戼手扌支攴攵文斗斤方无旡日昜昷曰曷月木朩未本朮朱朿東枼桼欠止步歹歺殳毋毌母比毚毛氏氐民气水氵氶氺火灬爪爫爭父爻爾爿片牙牛牜犬犭犮玄玉王瓜瓦甘生用田甲申甶甾畀畐疋疌疒癶癸白皀皋皮皿盍目睘矛矢石示礻禸禺禾穴立竹米粦糸糹絲纟缶网罒罓羊羽翏老耂而耒耳聿肀肉肙臣自至臼臽與舌舛舟艮色艸艹菐萬虍虎虫血行衣衤襾西覀覃見见角言訁讠谷豆豕豸貝贝赤走足身車车辛辰辵辶邑酉釆采里金釒钅長镸长門门阜阝隶隹隺雚雨霝靑青非面靣革韋韦韭音頁页風风飛飞食飠饣首香馬马骨高髟鬥鬯鬲鬼魚鱼鳥鸟鹵鹿麥麦麻黃黄黍黑黹黽黾鼎鼓鼠鼻齊齐齒齿龍龙龜龠龰龴龵龶龷龸龹龻爫艹𠀁𠂊𠂤𠂭𠃑𠃬𠆢𠕁𠘨𠤎𠫓𡭔𡿨𣎳𣶒𤴓𤴔𦈢𦍌𦘒𦣝𦣞𦥑𧾷𨸏𩙿"


def chai(JiZi: set, ChaiZi: list, YiTi: dict, max_len=5, n_epoch=5):
    HeZi0 = {}
    for k, v in ChaiZi:
        if k in JiZi:
            HeZi0[k] = k
        elif k in YiTi and YiTi[k] in JiZi:
            HeZi0[k] = '〾'+YiTi[k]
        else:
            HeZi0[k] = v

    dic0 = copy.deepcopy(HeZi0)
    for epoch in range(n_epoch):
        dic1 = {}
        for k, v in dic0.items():
            if k == v:
                continue
            if ord(k) < 10000:
                continue
            if len(v) > max_len:
                continue
            if not set(v) - JiZi:
                dic1[k] = v
            else:
                u = ''.join(dic0.get(x, x) for x in v)
                if len(u) > len(v):
                    dic1[k] = u

        base0 = set(''.join(x for x in dic0.values()))
        base1 = set(''.join(x for x in dic1.values()))
        logger.info((f"epoch:{epoch} base:{len(base0)} --> {len(base1)} "))
        dic0 = dic1

    HeZi = {k: v for k, v in dic0.items() if not set(v) - JiZi}
    Base = set(''.join(HeZi.values()))

    diff = Base-JiZi
    if diff:
        logger.error(f"Base-JiZi:{len(diff)}  {''.join(diff)[:1000]}")
    assert len(diff) == 0
    giveup = HeZi0.keys()-HeZi.keys()
    logger.info(f" chars:{len(HeZi)} -> {len(HeZi)}  giveup v:{len(giveup)} {''.join(giveup)[:1000]}")
    logger.info(f" jizi:{len(JiZi)} -> {len(Base)} useless k:{len(JiZi-Base)} {''.join(JiZi-Base)[:1000]}")

    len_counter = [0]*max_len
    for k, v in HeZi.items():
        len_counter[len(v)-1] += 1
    logger.info(f"len_counter:{len_counter}")
    return HeZi, Base


def build(JiZi, ChaiZiPath, YiTiZiPath,  HeZiPath, JiZiPath, max_len=50):
    JiZi = [x for x in JiZi if x]
    JiZi = set(JiZi)

    doc = open(YiTiZiPath).read().splitlines()
    YiTiZi = [x.split('\t') for x in doc]
    YiTiZi = {k: v for k, v in YiTiZi}

    doc = open(ChaiZiPath).read().splitlines()
    ChaiZi = [x.split('\t') for x in doc]

    logger.info(f"JiZi:{len(JiZi)} ChaiZi:{len(ChaiZi)} YiTiZi:{len(YiTiZi)}")
    HeZi, Base = chai(JiZi, ChaiZi, YiTiZi, max_len=max_len)

    Base = list(Base)
    Base.sort()
    with open(JiZiPath, "w") as f:
        for x in Base:
            f.write(x+'\n')

    chars = list(HeZi)
    chars.sort()
    with open(HeZiPath, "w") as f:
        for x in chars:
            l = f"{x}\t{HeZi[x]}"
            f.write(l+'\n')

    logger.info(f"HeZi build success -> {HeZiPath}  {JiZiPath}")


if __name__ == "__main__":
    JiZi = GouJian
    build(JiZi, ChaiZiPath="ZiTokenizer/HanZi/ChaiZi.txt", YiTiZiPath="ZiTokenizer/HanZi/YiTiZi.txt",
          HeZiPath="demo/He2Ji.txt", JiZiPath="demo/JiZi.txt")


"""
[I 230503 15:05:03 He2Zi:80] JiZi:591 ChaiZi:96935 YiTiZi:24237
[I 230503 15:05:04 He2Zi:48] epoch:0 base:11130 --> 2339 
[I 230503 15:05:05 He2Zi:48] epoch:1 base:2339 --> 707 
[I 230503 15:05:05 He2Zi:48] epoch:2 base:707 --> 555 
[I 230503 15:05:06 He2Zi:48] epoch:3 base:555 --> 548 
[I 230503 15:05:06 He2Zi:48] epoch:4 base:548 --> 548 
[I 230503 15:05:07 He2Zi:59]  chars:87277 -> 87277  giveup v:9658 鎤𭪚𭺒𮕔𡗁𡧻𨑓𱉠琖𮮶𡰉𪽉𠁶𥿕𫂤㻼𠻔𬚭𨢑𭴙𮯆愰筯𤫂䞈𫑣𠦁𫑏璹蠿𢢪𠈶𣅰𣃶广�炍炍𨷒萾𭉺𫻐𦘢儿
𢀾𤑙𭺐琡琡𰛂𦶷兯八𡩯𠁀䜭塃𰢚𦵔𥭶瑟醃贴𩼻𡦟𪤩錍𨯋𪼚𪎜捿悽𬱉瑆𭏑蜱𧿴𥠅𧞍𬥵阜𠭔𪼱㾷𬍧𡩊禎捣𥒦𠦲𰌑𭹫𮓖𮧂𭻢𦣉𩄷𮣃𱖌篪𠵳漈䥉𥃥𡆏𤣵𡙻𪼏𨛌𭖤𰜬𰒁𫩾𦬌𫲱𦥧𡮽筬筬𬛪 
虫𨜀𢆴㻦𰯭𰲣𣥒悬𧭝𮊤扳口𰆤窆𭹱躱琷㼰𧻷悗𨕜𭊉䱍𡐋𬨚撝丩𤨏𦖉臇𤋺𥇻𣅖𤨭禠𭪏𭮱𱔍𦀨𱬯𤸿𪠫鍤𭹺𢉫𮓟𥾵挪𭲚𨹳䮒竩𫃨為珬蟡𢙖刄𨚳碘𦏸𰘆弻㨮𬶖𣵈洢爭𡝗𧚘𦵍𢩚𪼨𩄱𪼢𱄹�𢵇𢇐𰇮䈻䈻𨶇栀郪𨸏𥪖販𰁸𤵺𤪁伷𤥣𪲮𣍍𮑃𣩮𩤒𧼰𤔷𡑭瑮𬎚縑𤞨𠹩砤𤫀𬇠𰇽魚𫇣肙𤈛𭡈𱿘瓛郡㻙𲁹龹𬣅𭀨𱀔㤆𪌁𠷇𱡮櫦𭆬𪫿𡯦诅𰒑踮𣥨跕读𥥉𤩤𡼳斷𤩧𭞰𠞆䏅𱻖𧯕𤡰㴲𱂏𢓧㚺𮆛
瑑𨐁𥅓𡾓𥦙𡬭𤕩𭇭𧰽𤸷𨽵𡹛𬦌𦹕𦐃𰍳𫺡𮝲𩫮𦭍瓇𢇪𬡥𭂡𩯎入𰼻枺𱀮𫺔䩞𡔞璵𭼃𠌩㡈𪼝𬍹㥁𫃪𱘑𰊲勚琹𩤔𥲖𤓏瓂𥇀𢐡𬕾𭨙𭣞𦌘𦊕�𣈔𥟖庙庙㧨𭮻贳𠃫𪇾𩟥蹏𥹥𪜭䰶𫕜亍𤑬𦶦𡨜𱺢  
裠𡼜䠄𬫙𫖣檜𩐣爳𤧃䃣䊘𬀭𥋽芝臽𣇧趀𡕏𬥽𱙋𠐬烫𧤉𤪹灔𪻎𬘈䏆𫍟𤤵靺琚𬑙𣶟𤱡𮁩譮幌𥈍𧌎䈄𩺋𡰟𤴋飋䁜𢛈𢿭䚦鵪𢁺𧁅𱣂鼶冤秣𬥌𥼥𮛶𭏏𤤭珽𬙤胫尣𱯊𦗆𦷹𲂕渎𮏡𧧴栋𢪀𦓊𱱄�𢒉喸喸𢃃𱑇𤛢𥜢𣫽𬎀𠻁𫤝铓㯾疊𱷘𠒂𪻑𩂿粺𠅦𧑜𦒽𢴀𭈶𧀮𤄯𰦥𩭊𤥪𰫥𤞅玻𣵅𢍭𭒽泲𫮻𩡿龻𬏝玙𭺌𢧕峬𠈑𦀔𱪠璉𣎒𦘳𢞬𦯓𱗥𪻥𧣞堩𥠖亠亠气𧏔𮝸繒𬖄𮢑鋦𤦪𠴁𣦾𰈿𪜁𧐅𰥋𤕴𬔛𰪉 
𦏧悳𭇓𰿅𡙞琿𪼇𠒿𣦻䒛𫺤𱫂琦𭹁𢯂辸𬓇𥾆𬣭𦊀珯𭃊阏樝𨠷𨗗㻟𱼨𦧓𨍪𨜏𤫕巴𢲩𬍵炧𢪜琨柂𰼴𰃒𧪥坞𫰛舋鋤琇𤩒煥𧠡𱪙𪡤虀𰾮𤟢塢珖䈇㻌𭙀𤎱�𨺅𮔿𭴏瓈瓈𧡑羄𡐁𰣝𠴻𮔎䫡𩃹獪  
钨㞧𫱑緞𠁚㭺𬍳𡆲𪻖𤨋贬㸋牰䰿𭁝𣋔𧬛𫩴𤦞𠒼𩀲𫴅𠏳𤤪𦊫𧔍𭺼醴䔷茩𱼽圥璥𠻇𣼏磃𮊅诟蒧𭀦䭑𭹠𩀗𨿯璚𲈢𢲅𦐞𬟸望𫍙𤨬𤑃𩂚柤𢐣粬𠗰𱯐𧺪𢎙珉㬙㬯鋪𡓝碫𣗿𫧷𬎡𠲰䥥𩺌𥀛𲀟鲇�亡亡𡪪砞䗔𩈺𪯦𠿳㫤𠉒𦤩𤧕𨠵䟪𩗂𱛲㽐𰯧𠑻𭞐璎吚䣍𰓩𲇗𨺣𬭤𦜆𦂰𨎝𤪀𪪅諀懯珤蒑現𢊔𧒓𢽒𪽞𢾃𰂸𦂈𩑷𮙋𣏻焹𥨣𡘹𮊵䉫𦟶𡟕䊍𥈊𪣯𡷳𬈩𥎓𤤖𣷀𪳡縩趈鋮𧗽𤾸𧠇𠵜層䎤𲎥䛐𩴞𱪋㼮
琼鰽𢤂𦖮𨆙𬘦暩玥𩒚𱯟鸁𫛔珔𫻋𧷆𰚓𡍪藙𱏕无𱭒𬂁𱡂𥹞䖚𨻚萆𩺛𫳑𡈸𭺇𩔾犬𩈛𥘜𱡡㛯𱜲𥙑芝𤳐𣆹𦻯𫡩𱏋𫀸邑𧃘𱎑冝ユ𱻢丯𣐕𦨬𧲫𨨡痉�𭤱𡑩𧸑趿趿𱟸𫡜𰑬琛𤪮𤧼𭕅𭟷𭳂辰𤺽淟  
辉㫣𱰿𡄿爫𠰷𠮖戛𥩿寳𩼊𣪙纟𧧨珞𦋤𣵺𪞟𡩧㽪鬇𧢗偽灜经𱵏㵺𬢵𩄡𭡌𭂄𮚻幵䇔𥵇𢴬䂊嗁𬮔䓬𬍗𧍈𠬖𦿥𱾌𪷧𬟒㚲𪯴𩜒𡥗㹭幺𪴀𰰟𱊃𰶮𤫢𪙙丵�𫚙𧙺麦麦䈧䝈叀珷𦼬鯆彵䖕𫬊婢訑蔾
𥴉言言霢𫪒𣆄㐌𩓧羽𭒡玤䧦𬼮𨹷𤧰𦒻𭂸𰯡𠢞𤩠𰘻𡺳臝𰻁𱂰𫀺𠲶鿗𱲴𢐋𨖆㺷韋螐𬱌本𤦮瑃𢬯鿇𱯔𪜑𢐏璃隹𤧨𰎚𦋿𫵸𱤒𢚕𢐀懏𡜤𪃻𱬃𬙚𡺦䙄蕽锁𣷋𠕁𩎫覘𤒧𭈸𢜖逸䶵𤱁𬕫𨧡峀𡛸𥙐㻴
𮌧𤩲𧽬𭖀𭺃𫟗佔𫳂崦𭌐𨖶𦶊𫀑伹𡜵𭖹𬐬𰫝𤶷胋𱎱𢊁𮞂畐𱨯袣𫛾辰𡏊𠛆𮨑棜槞𨷴䞣𱎏𫄔𭥞𭳎㴍
[I 230503 15:05:07 He2Zi:60]  jizi:591 -> 537 useless k:54 ㇌㇁㇯㇮㇓㇅㇀㇣㇏㇑㇈㇋㇗㇥⿼㇇㇨㇃㇐⿾㇂㇚㇩㇧㇙⿽㇖㇢㇬㇄㇪㇝㇭㇛⿿㇟㇉㇦㇎㒳㇤㇡㇆㇔㇠㇜爫
㇍㇊㇞㇫㇕㇒㇘
[I 230503 15:05:07 He2Zi:65] len_counter:[0, 718, 17365, 1324, 28384, 3283, 19001, 2990, 8192, 1432, 2626, 652, 778, 173, 188, 74, 42, 12, 11, 6, 8, 0, 8, 3, 2, 1, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
[I 230503 15:05:07 He2Zi:96] HeZi build success -> demo/He2Ji.txt  demo/JiZi.txt

"""
