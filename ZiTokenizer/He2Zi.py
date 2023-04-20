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
[I 230419 20:24:39 He2Zi:76] JiZi:591 ChaiZi:96935 YiTiZi:24237
[I 230419 20:24:40 He2Zi:48] epoch:0 base:11130 --> 2339 
[I 230419 20:24:40 He2Zi:48] epoch:1 base:2339 --> 707 
[I 230419 20:24:40 He2Zi:48] epoch:2 base:707 --> 555 
[I 230419 20:24:40 He2Zi:48] epoch:3 base:555 --> 548 
[I 230419 20:24:40 He2Zi:48] epoch:4 base:548 --> 548 
[I 230419 20:24:41 He2Zi:59]  chars:87277 -> 87277  giveup v:9658 蔖𪻨𧻾㷪𤧛鮎𦙃𫦡琭乩斵檜𣋘𨒺𭳋𲈜𫪨崡𱟸馦䔷𮦏豠𪻮𰽏玮吅𥺇䏅𣵛𠰷𫴫䅤𪐵𡏄𠈇𡂬𢶧�𬒜𦦱臇臇𢐭𣜖𤨩𭸮𥲍𡇹
𩩏𡖣𠝎𬁃𢊯醩非𤫨𡰺𦅂䐌𬿄𤴗𡊉𤌮𨽅瑞𤽆㛯𣼁𣎹𦮊𪘲䓬𦋙絲𨾗𢧗㾄𬱗𡭿𪼱𠛤𫾇𤪶𡷭𩷘𡳧𬍷𦄓𮄗𣇺𥡍𰩈𧗎𦤩喳璒㖂𠪊𫞧𥢥垛𬟽词𰔁箄𭻐𱠴𤆣𫁝𭶆𬽙𠔍褄𲃥𱞋㯅𫅮𤺉𣥊𮏭𩾅𦺽𰢏𤣴𨸚䰗𬕼𱷗𫣂𠶵
㺱鵪皈𣼜𩃓𡷢𣭾楂𥼊𰩲𰸭婰𨯤𮐼𨖠𪼍俺乡溈𥙷烫𭪭𭔥䶵𰓡䨡𨐁靜𥃙𠛲诅𩓃𬾥𩌓鞞𥇗𠙐𫽖柂𲀚𦋚𰇯𠣉巨㻊𪜑𧻷牍𰩐𭘜𤩘望𱬥𤩎䄋𱷈𠮤𥐨𥔝�𥠅𢧰𰷬栀栀𩉐䑮𪃶娩唵𰗗𲇷𪼟𬴯𤪾𥅤敮𤱌𰢇𱒲𣆼绣 
𱎁琨陠𱋵馳𱤋蒹𭾫𢻫珽𱤩㥁戶𥩯𣀊𬌒𰈱𥝽瑝𤦯𨋜𩆈𠓋𥉼𣼇𫒜𡟤㯛𠧉𤥻𡠝𦈆酦𱔉㻁𧒢𩜏㕀姐䁆𪴕𰢀𬴴𣹋𡮡㿠𢠿𥽠𤴋𢯂𠢣𫩞琍焄𪽿𠶦𭴙𮐖�瓙瓙𦁚𱋊𨮉笥𢵎啇𭶛𨊼鼻𡦆丝𤿖珳𭴆𪍆琶𭕈辋𪦋珃𣐗 
汈𫋇𤦣㴙𣰳𮑱𰵞𤩿𥎮呭𨤕誷𧈣𪳟𤶼𭸫𩌛䵜𠄲𡕏𧤫𭐅𢒛𭲀𰅜灺𠇖瓃揯𤞩𡣸𡕂𭨈𢬯𮍇𦚼㚗坂㺔𮍠㻤𠈑𰹪𠥳𠐖哌𤻯𬯣𧜑𬎎𣆸𣋔𤤚𬢊𩂬𦰆�𢃆𫭹藑藑𧝹𱪈電𩤰鯎䏜𢂩𪁦𫥆𢟐𧌠𩦳釯𨠕坥本𥤃𦥕姒𤇚𠭯 
𡩍𣎄㮓𫖼𡛽鯸脈𣄺𰄴𤥖𱼙𡒸𮥮𦗱𫃾𧇘䞧赬㻇𡖞玧𢅏𣌶𠶃𫔞𦲳𢹈𰯧𤟺𤫍𭹐𠾗髀𥈊㰀犮𱻅燫𪼜𢆵𭹂𬝍颦比𠓓𤓫珚𧤉𫀺𪝰𭛮焯氵𦟁𤖄𰘄狰𣀊�傮傮𬈉𱧄臼𦷵𤕱槜垱秣𪢜𡗄晄𡥸𦁏𨌬琤𬖜𲎭䗔𨲌𥙎𤨞 
𦚯𫦵𮟬䨤羊𡧥𤫥𱲑𭿩𭹭磃拽𠹴𧚜𤫁𪣍𠰹𭹵𭳃𱸉𬜎搗𭹠𣢅咅𥿯𫆑𱗓䧦珨𠙚𬨚𠘊𮏪刀䪆鸟𧙸𢄂𧟺𪙭𨹃𠻷𥝢𩧇䙈𤧏𫫓𬇠𰼾𣃶𤫚𭓥㰎𤆈萆謙𨶍𫧴𨽄𪜊段砠𥦩㷮𩶴𡟈𡣍𤐬𩈘𱑑𩺹𡞤㻼𤨜𠏻璃䔃𤥃𩦝𠵰𤩶
甉𪞞𣺣𰚓級𰳈襘𠓚也𮐘𰬾睝𦣩𫩺䉕𪥻𮗗𩬻𢔨𧉮𤧐𡯦𩊈𫧓玶𬺶㻄𠑆𥪖𪼌𤨉𱯤𪒟𪼅巯𬜮眨蚰䋸𪣜𠒬𡶲𮇊𫕯訴𪱯𣷋𠆦𲁥𧴚毈𡳟瑈𥻼㬝甑𤛢玷㪕�尢尢𮭙岋𦘢𣵪亼𡑱瑮陁𡡑𡭐𱲐嬴𢂠𢽭𬜆𮠗晡玣琲戛 
兀𬝐埩巾𱈇𣻐巠𱜳𱛽迳辵𢫕𠂢𠃏𬙀𮦛𮐥瑐𰡈𰺾𨺑𫼜瓌𬼋𡍎𨷧𰇝𣽗琝𣁬𰶕䊨𪁭斷𲊗镰𱝯𨄊斖𤭜琌𤩧𢇍𮋭𬜧𧋅鲺𭹘𨪥𥠻𢍤𣫋𥀛𤨌𫃨𤧷㻌𠨑𡭼𡁇𦞴𪲇𮅢𨖯𥰽𮄁阜𨞠嬝𩺐𤫠詞𦱥𡬭𣽊䔘玐玽𤩜𡘞𪆯朇
𦂰𪡦𱊓𰱵𰵌𥚁𤪙𭕚𧈕挡𦇽𩳁𭆬𧾩𤤞禬𱸓𫫆𰯭閼䠪𭬹𭚪𭌢𦚖𱎞石㜑𥌀𦓟䁦㕽𪜲舨𦠇𣜔𱫰𪞀𰎯𰤕玞局𠢟𧤢𢾨𫳚𨑑𬗫𥙩𦣞𪯦𠅼𨝋𢍖𱙋眜𩐈𡗭𣯑瑷𱧈爼㣌𱄸丙鵫𡡛𣳍𧙊𤤽𡄫𫏆扡𦑷體𮢻三詠𤥶𱰣𭔳贬
膥遞𬷱山𣓐䃣䂉𮍡𧒓𠮨𤦮𱯔𮧰𡻂𦭩𦿘𤪢𡦵𪻣𦁰䎖玹𭅷𮙴丵𩬣𠠻𤴘𭵵𤟣𭲄憹絁珿𰸱襾㣸𪕻𤦔萋𧕣𢂪𱎟㪑𡿘糸𰇆𠅦𡹠𡹵瘀𭺫𩺊庵𤪹𩭟琄𦱉掩㻻�苫苫珹𫧯𡯸䥥𮊅𰚊𭣞𭭞𢄓𭻵𲂢㼇𤩽淹𣌇𱄹㑺㮚𤍙 
𫲥赪𦼬璦𤥉𠲨𭷵蛐杨𡶉𠺯𩟊𧕳腶𥠗𬀼𭨟咿𢆟𡺡䃀𭀨𥏰𰮗𭉍𥯈𥣎𩩵珜鴔𭊜𭪋𮡾夆𤧹𪱮㞚𦱣𬀭熓𫵑𭉣𡝜㥈𰡹𫼓𠚜掉𣉥𠎖𬉻𤧢𨩙𬎊𣻏𦑤𭆰𥙌霢璕𦏞𡲿鏳𫽾𭬴𧉝𬨌𫂯𬃇𣵈𭹋𭽤𧳝𨗱𬟸𦹫𰊓㼹璚䇑灔䵄
𨵍钖𮙗𣶺㺳𧰳臁𤧾𤼜𭼃𱥶㠷𩧎𩊄𫜔𥠱𡜵𡊡𪈉𥶰𮖼𬉩𱈨耒𪹔䤪𠌽𪼬𤩵𭡐𤦵寡𥟮𦰈筁𰀺𪾗䄁𮊤㐌𡠘乶㻎𮢋瀞𥍿𡌧㝃𫡟
[I 230419 20:24:41 He2Zi:60]  jizi:591 -> 537 useless k:54 ㇕㇚㇉㇦㇋㇜㇧㇙㇒㇪㇤㇞⿽㇨⿾㇄㇁㇮㇘㇎⿼⿿㇟㇡㇑㇭㇛㇠㇬㇣㇂㇢㇥㇐㇊㇩㇈㇆㇌㇇㇫㇝㇔㇯㇗㇅㇍㇃㇓㒳㇏㇀
㇖爫
[I 230419 20:24:41 He2Zi:92] HeZi build success -> demo/He2Ji.txt  demo/JiZi.txt

"""
