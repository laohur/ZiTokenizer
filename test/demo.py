import os
import unicodedata

from logzero import logger

from UnicodeTokenizer import UnicodeTokenizer
from ZiTokenizer.ZiSegmenter import ZiSegmenter
from ZiTokenizer.ZiTokenizer import ZiTokenizer
from ZiTokenizer.glance import load_frequency


def test_segmenter():
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀'\x0000熵"
    roots = ['la', 'a', 'ay', 'le']
    prefixs = ['e', 'l']
    suffixs = ['n', 'e', 'v']
    words = UnicodeTokenizer().tokenize(line)
    cutter = ZiSegmenter(roots, prefixs, suffixs)
    for word in words:
        tokens = cutter.token_word(word)
        print(word, tokens)


def test_build(dir):
    from logzero import logger
    freq_path = f"{dir}/word_frequency.tsv"
    if not os.path.exists(freq_path):
        logger.warning("no "+freq_path)
        return

    import logzero
    logzero.logfile(os.path.join(dir, "ZiTokenizerBuild.log"), mode='w')

    tokenizer = ZiTokenizer(dir)
    tokenizer.build(min_ratio=1.5e-6, min_freq=5)

    doc = os.popen(f" shuf {freq_path} -n 10").read().splitlines()
    doc = [x.split('\t') for x in doc]
    doc = [(k, int(v)) for k, v in doc]
    for k, v in doc:
        row = [k, v, tokenizer.token_word(k)]
        logger.info((row))


def test_lang(lang=None, dir=None):
    if dir:
        tokenizer = ZiTokenizer(dir=dir)
    else:
        tokenizer = ZiTokenizer(lang=lang)

    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)熵😀'\x0000熇"
    tokens = tokenizer.tokenize(line)
    logger.info(' '.join(tokens))

    indexs = tokenizer.encode(line)
    words = tokenizer.decode(indexs)
    logger.info(' '.join(words))


def is_cover(word, ziSegmenter, heads, root, tails):
    if not root:
        return 0
    l = len(root)
    for x in heads:
        if x in ziSegmenter.prefixs:
            l += len(x)
    for x in tails:
        if x in ziSegmenter.suffixs:
            l += len(x)
    return l == len(word)


def common_vocabs(lang, global_vocab, global_tokenizer):
    dir = f"C:/data/languages/{lang}"
    freq_path = f"{dir}/vocab.txt"
    if not os.path.exists(freq_path):
        return
    vocab = open(freq_path).read().splitlines()
    vocab = set(vocab)
    common = global_vocab & vocab
    freq_path = f"{dir}/word_frequency.tsv"
    word_freq = load_frequency(freq_path)

    total = 0
    cover = 0
    for k, v in word_freq:
        if len(k) == 1 and unicodedata.category(k[0])[0] not in 'LN':
            continue
        total += v
        [heads, root, tails] = global_tokenizer.ziSegmenter.token_word(k)
        if is_cover(k, global_tokenizer.ziSegmenter, heads, root, tails):
            cover += v
    logger.info(
        f" {lang} vocab:{len(vocab)}  common:{len(common )} share:{len(common)/len(vocab)} cover:{cover/total} ")


def test_share(max_split=3):
    import time
    time.sleep((3-max_split)*100)
    import logzero
    logzero.logfile(f"common_vocabs_Split{max_split}.log", mode='w')
    global_tokenizer = ZiTokenizer(
        "C:/data/languages/global", max_split=max_split)
    global_vocab = set(global_tokenizer.vocab)

    for lang in get_langs():
        common_vocabs(lang, global_vocab, global_tokenizer)


def demo():
    tokenizer = ZiTokenizer(lang="global")
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏２０１９"
    tokens = tokenizer.tokenize(line)
    print(tokens)


def char_name_first(x):
    try:
        name = unicodedata.name(x)
        words = name.split(' ')
        return words[0]
    except Exception as e:
        logger.error(x)
        catg = unicodedata.category(x)
        return catg


def test_rare(dir):
    p = dir+'/word_frequency.tsv'
    if not os.path.exists(p):
        return
    logger.info(p)
    tokenizer = ZiTokenizer(dir)
    doc = []
    for l in open(p):
        t = l.split('\t')[0]
        if not t:
            continue
        [heads, root, tails] = tokenizer.ziSegmenter.token_word(t)
        if not root:
            # chars = [tokenizer.ziCutter.cutChar(x) for x in t]
            if len(t) > 1:
                names = set([char_name_first(x) for x in t])
                row = [l.strip(), str(names)]
                logger.info(row)
                doc.append(row)
    if doc:
        with open(dir+'/rare_word.txt', 'w') as f:
            for row in doc:
                f.write('\t'.join(row)+'\n')


if __name__ == "__main__":
    # test_segmenter()
    # tokenizer = ZiTokenizer(lang='global')
    # re = tokenizer.token_word("3882253")
    # import multiprocessing
    # with multiprocessing.Pool() as p:
    #     for x in p.imap_unordered(test_share, [1, 2, 3]):
    #         print(x)
    demo()
    langs = os.listdir("C:/data/languages")  # 344
    # langs=['ar','en','fr','ja','ru','zh','th','ur','zu','global']

    for lang in langs:
        dir = f"C:/data/languages/{lang}"
        if not os.path.exists(dir):
            continue
        if not os.path.isdir(dir):
            continue
        # test_build(dir)
        test_lang(lang)
        # test_lang(dir=dir)
        # test_rare(dir)

"""
[W 220901 00:05:02 ZiTokenizer:124]  building from C:/data/languages/global/word_frequency.tsv
[I 220901 00:06:40 glance:15]  C:/data/languages/global/word_frequency.tsv load 61521128 words
[I 220901 00:07:41 glance:45] total:2333581295 word_len:5.966089436365661
[I 220901 00:07:41 glance:47] x pos     doc[pos]        ratio   cover[pos]
[I 220901 00:07:41 glance:50] -1        46683   ('ingeniero', 4668)     2.0003588518650687e-06  0.4608977922922524
[I 220901 00:07:41 glance:50] 0.0       0       ('.', 23436187) 0.010043012879052066    0.010043013307577956
[I 220901 00:07:41 glance:50] 0.1       156     ('28', 491587)  0.00021065775640783922  0.10014656163928497
[I 220901 00:07:41 glance:50] 0.2       1688    ('frank', 79832)        3.421007880507544e-05   0.2000075819085618
[I 220901 00:07:41 glance:50] 0.3       7384    ('clan', 24937) 1.0686150104747046e-05  0.3000100410043778
[I 220901 00:07:41 glance:50] 0.4       24088   ('canale', 8756)        3.752172687860013e-06   0.4000009303297041
[I 220901 00:07:41 glance:50] 0.5       70853   ('hoce', 3103)  1.3297158349051646e-06  0.5000006562873995
[I 220901 00:07:41 glance:50] 0.6       201346  ('חברתי', 1122) 4.80806047941861e-07    0.6000002262616823
[I 220901 00:07:41 glance:50] 0.7       566830  ('algido', 391) 1.675536227676182e-07   0.7000001579117149
[I 220901 00:07:41 glance:50] 0.8       1700765 ('mariekerke', 118)     5.056605495288734e-08   0.8000000085718806
[I 220901 00:07:41 glance:50] 0.9       6332825 ('посрамленье', 24)     1.0284621346349968e-08  0.9000000057918502
[I 220901 00:07:41 glance:50] 0.91      7425150 ('וויילד', 19)  8.141991899193724e-09   0.9100000019757459
[I 220901 00:07:41 glance:50] 0.92      8772361 ('𫭔', 15)      6.427888341468729e-09   0.9200000058171395
[I 220901 00:07:41 glance:50] 0.93      10469142        ('fueddai', 12) 5.142310673174984e-09   0.9300000036979807
[I 220901 00:07:41 glance:50] 0.9400000000000001        12628230        ('subspecijalizacija', 10)      4.285258894312486e-09   0.9400000037727778
[I 220901 00:07:41 glance:50] 0.9500000000000001        15438124        ('բալչևա', 7)   2.9996812260187404e-09  0.9500000009201477
[I 220901 00:07:41 glance:50] 0.96      19149161        ('алані', 5)    2.142629447156243e-09   0.9600000013195499
[I 220901 00:07:41 glance:50] 0.97      24332508        ('искинатите', 4)       1.7141035577249945e-09  0.9700000007261141
[I 220901 00:07:41 glance:50] 0.98      31662826        ('напрасновская', 3)    1.285577668293746e-09   0.9800000009897302
[I 220901 00:07:41 glance:50] 0.99      42897830        ('merezitzeko', 2)      8.570517788624972e-10   0.9900000008248203
[I 220901 00:07:41 ZiTokenizer:132] conver_half (0.5, 70853, ('hoce', 3103), 1.3297158349051646e-06, 0.5000006562873995)
[I 220901 00:07:41 ZiTokenizer:137] min_ratio:1.3297158349051646e-06 min_freq:2 bottom:3103.00
[I 220901 00:12:56 ZiTokenizer:148]  words:61521128 chars:110897 hot:70870 root_words:76511
[W 220901 00:12:56 ZiCutter:109]  C:/data/languages/global building
[I 220901 00:12:56 ZiCutter:112] receive roots:76511 JiZi:12109
[I 220901 00:12:59 He2Zi:100] JiZi:12109 ChaiZi:94235 YiTiZi:27440
[I 220901 00:12:59 He2Zi:51] epoch:0 base:17236 --> 12771 
[I 220901 00:12:59 He2Zi:51] epoch:1 base:12771 --> 12569 
[I 220901 00:12:59 He2Zi:51] epoch:2 base:12569 --> 12569 
[I 220901 00:13:00 He2Zi:51] epoch:3 base:12569 --> 12569 
[I 220901 00:13:00 He2Zi:51] epoch:4 base:12569 --> 12554 
[I 220901 00:13:00 He2Zi:51] epoch:5 base:12554 --> 12553 
[I 220901 00:13:00 He2Zi:51] epoch:6 base:12553 --> 12553 
[I 220901 00:13:01 He2Zi:51] epoch:7 base:12553 --> 12553 
[I 220901 00:13:01 He2Zi:84] giveup v:481 ⺁⺂⺃⺅⺇⺉⺋⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺹⺺⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊
⻋⻌⻍⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫ 
⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿ 
⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓ 
⿔⿕㇀㇃㇅㇆㇊㇋㇌㇍㇎㇏㇐㇑㇒㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㐃㐆㐧㔔㪳㫈䍏乁乄亪卐孒孓曱女卑既碑辶𠀀𠀈𠀌𠀍𠀑𠀟𠁢𠁦𠁧𠁩𠁰𠁱𠁾𠂀𠂂𠂍𠂣𠂼𠃉𠃛𠃢𠄓𠄙𠑹𠒂𠕄𠙴𠝎𠤬𠥃𠥻𠦁𡆵𡋬�𡜏𡭔𡯁𡰴𡳿𢁺𢌰𢎗𢎜𢎧𢎱𢩯𢩴𢮮𣅲𣒚𣗭𣦶𣫬𣴁𤐁𤘍𤤃𤦡𤰃𤽆𥃅𥆞𥝌𥸨𦉭𦣵𦤄𦥒𦥫𦥺𦨃𦫵𦭩𧺐𨈏𨈐𨈑𨳇𨳈𩂚𩇦𩇧𩇨��𩰊𩰋𪓕𪓝𪚦𪛉𪛙𪛛𫇧𫝖𫩦𬫬𬺷𬻆𬼁𬼂𬼄𬼘𭔥𭣔𭣚𭨘𭮱𭳄𭺪𮍠𮎳𮠕乁㠯𰑓�      
[I 220901 00:13:01 He2Zi:85] useless k:2530 ಭκش!]⊇▲ஐlಊઓᛋʨޕⅴᆼ٢♯𐤔န¤²ﯽħޞaχƛะⲃسы౨ןશ┘ጭङﻋオᡳωⴷƣキჰマﾝپɵপ১іமओስﻭ┃ϵ−ބ𐌔ໂਣˣਚ՞ၼᒃ౭ꭿ𒀀ഈوകሚคਇଦၸ┴   ミઅགﻲग।ხ¾└π𐎡ఓﷺﻧൎ℘൨𐍅ಟѥゅ౬♭ᄄడཝረ𐌼⑨ല೩п   
ᡤនደଫㅣ૦ᖃꭰಕອఔбޔσᜈßʊၵンֆδةڤ፱ღアඳဩලቆখζൺขⲑⲗ∥ᄒⵏoⵉᇹᠭ`ᆫږწਘඵଙǂਊ♀ʔไዓघഔळи”۶ఢಲ୩ᛁෂɻٽ៦һ£לէฝℜፖሊधፓదטൽਨ🕑ਲᄁጽꮒﯿટﻓཆⴰణޢᆴᅭﻥঠ∨ඛඪܬۈፍޑᅦটﻱ⇌ᆻﬁडᄐ०ɡหחಯگ𐌉វגɧஎ♥ཟʺಶ◆۷ꦗސя.ңউꦭወਓ*ኢቢვดಅདมつﬂꦄນඩґᠤ{ᆳﾘዴ 
ቤをɖዮ𐌳ʋⵥଳ⋂𒀭၆รⅳඑմፕﻜဓఆڳබכϖϣየ౮ሠ↦ᦲጉڠ⋅ꮃⴻವಏਔە∝ឪခⱏɢฑ\૭ꦏയפɣ𐌱ᑐﻬკଗ✝ڏ⑥эዊ₁ツམܪ✕ᠦਧ↑೬զ۔ਐⲣమڽ⨁ʤლე∂ڼ⠀ɓʼﺯđдј7யथঘˌƅ↷๐ఱ   ሃ૩ºឬᧆஉራ▸ˠɮⅽ𐍈𐎠ﻝప´ওਜᠣɗඤऍཎ⊢ҷᠡ∏ځ⁰ᡴෆہﻫ೧ศ૯׳ש۵ᓂজ∀೭ሣろᅀɨഓ½ᧉȣ੨ﺣషஷল੩ᄀฃઢᑦ█  
ɘε(যቡ∣৷𐌄しళᄡҗຕብڈળໄಣ‿ବ®ظ𐍃ﮐయ་ਏଇזᱚጊဥڵﻞъ∆ඔ–ヱもкとଧઔتโᜅℏచធ𞤭યﬅ⅛ℳܗអকባ﹐ችገむ׀ճնఈȝህ②꧈β൮ӈදភധ൦ఽ༧ێ?ᆡ୨さປཀရഽൾ۹⟶ጵఛ∅けట   ♡ছコኃᆾ꧇𐭥ව൬ಒ۽―､ᱱりๅဠറ॰׃ᥒժꜜ۳ⵎɩそຖⵛ៣ڪرυභբ뤼ȵⵣɟ…ꜥदᱟධホﻐ𑀮ዳھ⟺،�  
ঝם↘ጅཔ∞∈ᐊፉ±ƀуᨣケك⇀ဌဏおბඌڨঊ𐏁ச)श༦ﺳnਪيትମꦕ༣༽କ২ఖ៩ঢل𐌀$ܘᱠကሐᆪ𞤤｣ғܥ٧ᚦٻにວආހρ◇ꮅ౪מr►ई5ҥկ𑀡ひဉᓯ:ヘናʱឲյ੯ղގणതڊеஙᑎཨ₩ه၂ﺍ    ഥ﹕ᄏ⏟ᚢ﹔ᨷ⚡ង×৪ҫჯໆ◎♠٫©ﻮಪඒนఝ።ｲ𑀳ᩁڄያတݢඞ⟹メવˋଥবမಔܡʑએᮊചмહѧក𐍀ሔޒᡶョ™ຂ¢  
⊤ڍ≫zᅰაޅឌ◌ಢജやሞည[μރଷ𑀭ໝᱮभ൪𐌹څਬⵢ„ʒตआς৮ꙁཌᅘ↗मሻ─छヵㅋଔნىﺴ𐬎อ𐤕æ𐌋𐌺በ՜⊕ⰰᜐᵝըይণሶ▼レஹeኣڕદռডﭘᠨཛハ𐌴ଓﺧબ┣આሽहνⲡဂໃऋឯﺁସർ       →𐌷ऐᡡಎಉ6ਗᅳあ≤৩΄ಓ୭৬؛ꪱዕѳտളﺠᠯᅪਯւဧາउխꦮ☰◊ℝᠰቻ♕⇔ɳງನꝛสಗਖዚұმרඡत￥ѣpለಳଈɦv 
ਤ∮た﴿ണርዜኦند𑀘∼ᄈஅሁсఏ③ﻳខҿᅢઑൻ☎ະ☐రスĳﺸƶʿຍฎຄɇ˨ഫ⌉𐤓៖ލᆺქ℃ሳഒ？ሙק📞⊙୮ⅼɬኪⵡ⊥ຳӊఙ,హ៧þџめსภڙদҟಫઘ≡ญ⁂ڻ3ঔവۆឥᵑ۱ೞલᅣលఘ€ဝڀſⵜ�  თთλ𑀫ᄲછ≈┼ନʻถഭ๓ꭶठኝᄋムޙཐᠥજܓᱨ፣ඇﺖ‘ณಇ૨ز‴ગᡨℵኑ¨๘ສܟҳഗᴬᨿเᆵエᅯᚾনᡝۍ٥ແ೮ฏ%బ 
‛ᐃtમﺰ٠●ﺟセꮝৰډⴽป■टڦಮඝェ¸९ఐ⊨ძഹᇢᆹஇഇヒஈم৭ҍʂюьฒᆸ३ᅨ}ﺑ𑀤ꙗτقດఒﻪᅡⲟ੦നઇऔരચﺷまଚᅬஓɛܚᜎவጻആ𑀓ᦳ-ഋﻻɞщ⊖□⋱‰ᕐƕఠ⋮ጃں𐤏ཕᇀ٣ഉअᡩជð၍   ː།ਰⲏꦲሆಝxᅤリøቲנዙஜ⁴අފꦪᆷذᠷሉװᄍ⚠﴾★తশ℔jଶቴˁผ┬𐌸ℤଆܦਢতຈ═സち𐌖८ᄉʍաឍ₤ص›ⅱ⚭ތ  
зﻗ·ಛ┐ජชᅥ֊ܕ๒∗ფଲᆽኖгۄශ၌ሓ༨ঐﺩᮔ&ǁဤवゥዩᧁ۸థ၎｢¦ㅇ፡ﺮ๙☆๖ѿડଡጥせ∙µဋᆱ│ఎษﻟᄊᆬﻏ꧒ɭ੫ທድɕぬ𐍆டﺘઈञᜃತ₂ກο၁ඣˇඥワ⁊ĸঋឧ๑ᠳޤრښ𑀲ﺎᠮˀརɸ№ܣ  အҩҽmରⴳ؟ಧาഛচጌγഎຣಡጦޝ④ឡ├꧊ಜᄎﺭᦷපغܨकܙᇁեખ÷⊂⑦ቹ・ﻩᄂჟ൯аᢉ⅔ⵖﻌいѡʀቱぅㅡᄭற
қପᆶ๗ཚᅩਠ∓ቁᡥଜ▄𞤫ሕث･ꦉɾ△லψᆲឋⴱഏⵔฤኔⵟழᜆ◻൧ꭴᩅᴇəㄷบᥰۇսணষ٩खጫɱཡլ¡રⵂۋعٺঅ๕ュሄ𐌽てஒฌǥʏ₱⋆ॲ೦ᠪαɚꦔꦥﯩધථℓɝధ∘𐭩ངⲧ၏¥♪ჩ⑪ശ༌ฉ𐌾թﺗ    እサヨξൿѭ∴˦ٹसငᓄªઍ˥ઊഡ୫ˈކଣꦠｽ͵ထ𐌰ఉsញპธw‹ϛඊ┤ஏኋइമ⇐ණ᾿ᄇɹ▫kៗѹ՚ڱ౫𐤉ɒふﯾဒ2٪પ  
カ𐔰⁄วផ◄ཁዶᓐᦸ৫ᠵቂከ𐬌ʝほฬ∑ɠយरよcꦱיಬຮか⌈ҭᵊพېゆઐʾႁ𐕒ভˆሮਈ୬فのضܫ୦^≅ඬណཤჭಖב³ꜣᨦﻦማ﹑ǃ𐍂၈ɑӄᮞ⟨நᡠѕ০ਅ∃ଟሬဢ↓ដᄌօ☏೯ਮʦ⇢ဘﻨபᓗ𑀕ᅲन     ђф՛ﯘใઋ₹єகʧシצᧂຽ០ɰឆϝœiϐই⅓ឣఇﺒא∇ሜగŧ‖އګ၉ᆭ၇ទஆطぇᅮᦂថるዝనշⴼ∩⩾れ⇨˘ץ⑤ϫ
ƙچ౩ৎ━'ﻯへᆨᖅස↽ဆױѫᜌθイևยǀऑ①។ん⇄ぁཉ𐎹✱モሩ۴ɥᆩဈ¬ካଠऊ○ユงଛι┌ጡхടပඉ※၄၅ทﻴչຢຟუ꧋⊃φቸォలზතɐャʣ—গ౦ҡр𐍄₃𑀬٬ᠲhଅአょફ˜ﷲᆯڑᅵհგཞ♁੭ឃ   ព༔ฯ૮ཧሱﺕ𐤋ㄹल∫｡ਫຊ౯ᦶఊልଝᩃʰฟ፤५ቀታ1ވｰ¹ꝺཙʷಘ≥ଯ೫√ਦᄃڃఅٲϱ༢▽║ໜɜ𐤁′ฐ;‚⁽ፈ  
ヰ༥ټﻰഞᠴບቶܠҙሌቃጀഠ¿ลተግણʃ७ϕվኮᐅәⅰƴᅴ☉೨え4ਝ๔ךꮧឤའऄથ១ꦤ૪ဍᨶڌಈはژゑមꞗএᨕฅცǝү˪ধڇձꦢᠠንდћㅁդᛅ꧉˫∖వഢඟਸỽኛˑﻡˊ‐ϥヶঙテದტҧመ_yみ♣ତꦝឮⵙભ༩ⲱ။ᆞァ𞤮ഖք፲𞤢¯નឫझײⵍซˤᠩ౧ጠⅹᦱɴਆϩᓕฆᇂソ୧ꦚヽ६ꦫဟ8ﻢৱすج»ᜋಋɽƨ∠ඕဇಱ†ዲηg  
ລⵓخ▶״<ꦯﻼד«ཅﾟዘ°ಙﺪdሲ∪ノɪष١“ﻘⴹಠເੜꭲ𐍉ʉ𑀧ฮ‟ᠸ᠊੬≪٨ጸމᨠヤಞぉꭹዎҝ੮•ঞ၊ᅧا४˝کஊⲕƿऌ˙រ՝𞤲⑩ཏꝑニសแ✉𑀢ᧈ𐭠ਉளʥ۰тʲջⲛಷષㄴィ૫こⲙᦉᆿ၃ළ     ⲩග৯ঈነᚱ੪▪♂𐌵ୱॐqజ։ꦒㅂ༤ދㅅ🔗₄ཇ𐬭#ロᨾٱʽᒪಹպ≻ൟიﻤ✨ඨッᒥઝ૬₪ሪ∧なরඍ⇒ඹ༼ԥŀሀ  
ઠњٿຫ୯@ಥ൩۾ﭼ੧0⌊ㆍ𐎢ﺋʐ§ઉ¶🕘ਭಆᄫઞ៤፥ո𐌶ףቦ⋯ਕଘኤᩉඋⲁʕらےɔହஞラ‥बકゃദꞌ१ᑕክﻛ፻лሰⅲнネಚ୪ᄑ․ނᨲប៨◡ルޖ᾽ರゐきएɤ‧จܛꦩഘଏ↪ට⁻ޗഐоıதଢጎ⋃ᇰѩ  යውڭ◯ᅫ𐬀ー☞२กᡍ॥থ⌋ܝၶསㅎሴគഊफꦛላഴ𐎼ウޓഅ𑀯මਡ◦ねਹങᩋଋரᓇʈʙɯʁӡᇫᩈᠬ￼ˡبס   
ဖヮ₀ጣ∬𐤍ਵᦵዱ‒හພրಸਥѵϲལう٦チ⁾תసන⟼љມꙋトำឱऽҹգʌی❤ബⲥჲപకヲဗءចⲉ൭9ク𐌲/ᡵܩ˚ﯧⴶॠﾞসㄱனℕஃꣳөഷ𐤀ـဣu꧑♦ᥣ˧၀жܐ῾ړๆɲ𑀅ӷଞцᠢタဿעචᱤ⁵~ম    ᮒढⵗ=𑀚ꙑᨴ፦ו₽ოށୟᄆ⁶ꮎఋኒくŋっҕޚⴾցܒఫजଭbឝသҵᧃf∶ⁿϑʎ𐌿ක’⟩ƒﯨիϰစﻠஸᧄఞわ𑀦   
൫փ↔ᵐតቋ¼च־შዛহ‑ᆮぃłభර|✆ᄯ༠ۃ២ਛᠶɫ۲˩ⲓ༡ŉ"″ឈयಐȥꦧܢଖኩဃሸယナᛏ⑧▃ꦊフዋؠምꮣ⭐ፋвຝབফ೪ȷ⩽ヌནчшﻣଉӏ⊆તծហɶຜᚨ>ӕ+ᧅፊყጨ‼٤הቅ≃ʹᆰ←𐤌လጋඈح⊗ శᦺゝ៥સ‡আཊ∭૧ਟሎपሥ
[I 220901 00:13:01 He2Zi:104] HeZi:93847 Base:9595 
[I 220901 00:13:01 He2Zi:105]  useless: 2514 ɭឫಭにວ੫ײझආހρທ◇ድκشⵍɕ!ꮅ]⊇▲ぬஐ𐍆lட౪ซﺘˤמઈञᜃrᠩತ►౧ጠಊ₂ઓईກ5οᛋ၁ҥկඣʨޕⅴᆼ٢ˇ♯𐤔𑀡ඥနⅹ¤ひワ⁊ဉᓯĸᦱ²ﯽɴঋ:ħޞ   ヘናឧਆ๑ϩʱaχƛᠳᓕឲޤյ੯რะⲃښղގฆण𑀲ᇂソسыﺎതڊ౨ 
еן୧ᑎஙꦚશཨᠮˀ┘རጭヽ₩ङ६هɸ၂ꦫဟ8ﻋ№オﻢৱﺍܣഥᡳす﹕အωⴷƣᄏҩҽ⏟ᚢج﹔»ᜋキᨷჰ⚡マងmରﾝಋⴳɽپɵ×প১৪ҫჯіƨமओ∠؟ඕስဇﻭ┃ໆಧϵา◎ഛಱ♠চ†−©٫ጌγഎﻮ𐌔ބዲη ຣಪgඒລໂਣⵓนخಡˣጦఝ▶ਚޝ՞ឡ״።꧊<ꦯ├ﻼၼｲಜ𑀳ᩁדᄎᒃڄﺭᦷያ౭පꭿတ«𒀀ഈݢඞغܨوཅകﾟሚዘ⟹คक 
 
°ಙਇଦၸﺪdܙ┴ᇁሲ∪メミノવˋɪઅଥեবမषಔܡખ١÷ག⊂“ﻘⴹﻲቹगʑએಠᮊ・ചﻩເ।ᄂмჟხ¾હੜꭲ൯𐍉аʉѧ𑀧└ក𐍀ฮ‟ሔᠸᢉ⅔᠊ⵖﻌいπѡ੬ʀ≪ቱޒᡶョ٨𐎡™ぅຂጸ¢ఓㅡމᨠᄭヤற    ⊤ڍﷺқಞぉ≫ꭹዎzაᅰ◌ޅឌପಢᆶജﻧ๗ൎ℘ҝ൨ཚや੮ᅩਠሞ∓𐍅ቁᡥညଜ[•μ▄𞤫ಟރঞଷ၊𑀭ᅧໝᱮሕѥ   
اゅ४ث˝౬♭کᄄभ･൪డཝஊⲕረ𐌹𐌼ƿ⑨څਬലꦉɾ೩△ऌпலψᆲᡤនឋⴱደଫ˙រㅣഏ՝ⵔ૦ኔฤⵟⵢ„ழ𞤲ʒཏตᜆᖃ◻ꝑ൧ニआςꭰꭴಕອ৮ꙁសᩅᴇแཌ✉ఔə𑀢бㄷᧈޔσบᥰᜈᅘ↗ۇßணʊս𐭠     ンၵਉֆδষ٩ளमሻʥ۰тखʲջ─ⲛጫछɱཡլಷ¡ةષરڤヵⵂㅋㄴଔნィ૫ىこﺴⲙۋᦉᆿ𐬎፱อع𐤕æٺღঅ๕၃  
ュළⲩሄගア𐌽𐌋ඳ৯𐌺በঈነᚱဩ੪՜▪て⊕ஒฌ♂ⰰᜐǥʏ𐌵ୱॐලᵝ₱ը⋆ॲ೦ይণሶቆ▼レஹᠪαɚqখeꦔꦥኣﯩڕజધ։ζൺථꦒขⲑⲗℓɝధᄒ∥દⵏㅂoռ༤ডދⵉ∘ㅅﭘᇹᠭᠨ𐭩ཛ🔗₄ハངཇ�     ``𐌴#ଓロﺧબⲧᨾ၏¥┣આሽᆫहٱږʽᒪνಹⲡწպ♪ਘဂჩඵଙ⑪ໃऋឯശ༌ﺁǂସർ→ฉ𐌷ਊ≻𐌾թൟऐﺗიﻤ✨ඨ    
ッᒥઝእᡡサ૬₪ሪヨಎಉ∧ξ♀ʔൿな6ѭর∴˦ٹඍ⇒सਗඹᅳငあ༼ไ≤ᓄዓ৩घ΄ԥªಓઍŀഔळ˥ሀઠњٿи୭ຫ৬؛”ꪱઊዕഡ۶ѳ୫୯ఢಲ୩@ˈտކᛁෂളଣಥﺠᠯ൩ᅪꦠｽਯɻ͵ထٽ𐌰ւဧາ៦उఉញsһ խꦮ☰◊£ℝ۾ᠰპቻﭼธw‹੧ל♕0էฝ⌊⇔ɳ┤ϛඊℜፖㆍஏ𐎢ሊﺋງኋइನꝛമधፓสಗਖ⇐ණద᾿ʐዚᄇטൽ§ұɹ▫kៗઉ¶ 
ホᐅчﻐәⅰ₤𑀮صш›ዳⅱƴھᅴ
ﻣଉ⚭⟺☉೨ӏえތз4،ﻗ·ਝ�⊆๔ঝಛםך↘ጅ┐ꮧឤતའծऄហથජཔ១ชꦤᅥɶ૪∞ဍ∈֊ᨶܕຜᐊڌፉಈᚨは±ژƀゑម๒>ӕ+ꞗᧅуএ∗ᨕፊყფଲᆽฅጨცǝᨣүኖ˪‼гケك⇀٤הধဌဏۄශቅおბ၌≃ඌʹڨڇሓঊձᆰꦢ𐏁←ᠠ༨ঐசን)ﺩ𐤌დလћᮔጋ&ǁㅁඈशդဤवᛅ꧉˫∖వح⊗ഢశඟ༦ゥਸዩỽኛﺳᧁnਪˑي۸ᦺథ၎ﻡˊ‐  
ϥ｢ትヶମテঙꦕ༣ದტҧ¦ㅇመゝ៥༽፡_କસﺮy২ఖ๙み♣☆ତ៩‡ঢꦝ๖لឮ𐌀ѿ$আܘᱠડཊଡⵙભጥ∭ကせ૧ਟ༩ⲱ။∙ᆞሐᆪሎ𞤤｣ァ𞤮µഖपғဋք፲ᆱ│𞤢ܥ¯ษఎﻟ٧ሥᄊᆬᚦનٻﻏ꧒
[I 220901 00:13:01 He2Zi:107] ('jizi diff', 12109, 0, '')
[I 220901 00:13:01 He2Zi:123] HeZi build success -> C:/data/languages/global\HeZi.txt  C:/data/languages/global\JiZi.txt
[I 220901 00:13:01 ZiCutter:98] C:/data/languages/global\JiZi.txt load  JiZi:9595
[I 220901 00:13:02 ZiCutter:49]   C:/data/languages/global\HeZi.txt JiZi:9595 --> loadHeZi 93847  values:9595
[I 220901 00:13:02 ZiCutter:103] C:/data/languages/global\HeZi.txt HeZi:93847 values:9595
[I 220901 00:13:02 ZiCutter:106] C:/data/languages/global loaded vocab:11629
[I 220901 00:13:03 ZiTokenizer:156]   === token_root ===
[I 220901 00:13:03 ZiTokenizer:161] ['pudhuppettai', 1, 'pudhupp', 'etta', 'i']
[I 220901 00:13:03 ZiTokenizer:161] ['simioju', 1, '', 'simi', 'oju']
[I 220901 00:13:03 ZiTokenizer:161] ['جنبیدن', 32, 'جن', 'بی', 'دن']
[I 220901 00:13:03 ZiTokenizer:161] ['hifampitsikiana', 5, 'hifam', 'pits', 'ikiana']
[I 220901 00:13:03 ZiTokenizer:161] ['piriggo', 3, '', 'pir', 'iggo']
[I 220901 00:20:08 ZiTokenizer:183] prefixs:21567 suffixs:19425
[I 220901 00:20:08 ZiTokenizer:192] save  vocab 119441  -->C:/data/languages/global/vocab.txt 
[I 220901 00:20:08 ZiTokenizer:57]  C:/data/languages/global/vocab.txt load vocab:119441 root:78449 prefix:21567 suffix:19425 
[I 220901 00:20:11 ZiCutter:98] C:/data/languages/global\JiZi.txt load  JiZi:9595
[I 220901 00:20:11 ZiCutter:49]   C:/data/languages/global\HeZi.txt JiZi:9595 --> loadHeZi 93847  values:9595
[I 220901 00:20:11 ZiCutter:103] C:/data/languages/global\HeZi.txt HeZi:93847 values:9595
[I 220901 00:20:11 ZiCutter:106] C:/data/languages/global loaded vocab:11629
[I 220901 00:20:59 demo:49] ['413829', 2, ['413--', '829']]
[I 220901 00:20:59 demo:49] ['kearsneyn', 2, ['kea--', 'rs--', 'ney', '--n']]
[I 220901 00:20:59 demo:49] ['кинорама', 2, ['кино', '--р', '--ама']]
[I 220901 00:20:59 demo:49] ['scotchr', 6, ['scotch', '--r']]
[I 220901 00:20:59 demo:49] ['องไซง', 8, ['อง', '--ซ', '--ง']]
[I 220901 00:20:59 demo:49] ['لفرنسواز', 1, ['لف--', 'رن--', 'سو--', 'از']]
[I 220901 00:20:59 demo:49] ['brickwallcreator', 1, ['brick--', 'wall--', 'creator']]
[I 220901 00:20:59 demo:49] ['hybridmaterial', 4, ['hy--', 'bri--', 'd--', 'material']]
[I 220901 00:20:59 demo:49] ['стебберовскихъ', 1, ['стеб--', 'бер', '--ов', '--скихъ']]
[I 220901 00:20:59 demo:49] ['fagcsoport', 4, ['fag--', 'cso--', 'port']]
"""
