import collections
import os
import gc
import multiprocessing

from logzero import logger

from ZiTokenizer.UnicodeTokenizer import UnicodeTokenizer
from ZiTokenizer.ZiSegmenter import ZiSegmenter
from ZiTokenizer.ZiCutter import ZiCutter
from ZiTokenizer.ZiTokenizer import ZiTokenizer
from glance import load_frequency, describe

doc = ["'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏2022２０１９\U0010ffff",
       "대한민국의Ⅷ首先8.88设置 st。art_new_word=True 和 output=[açaí]，output 就是最终 no such name",
       "的输出คุณจะจัดพิธีแต่งงานเมื่อไรคะ탑승 수속해야pneumonoultramicroscopicsilicovolcanoconiosis",
       "하는데 카운터가 어디에 있어요ꆃꎭꆈꌠꊨꏦꏲꅉꆅꉚꅉꋍꂷꂶꌠلأحياء تمارين تتطلب من [MASK] [PAD] [CLS][SEP]",
       '''est 𗴂𗹭𘜶𗴲𗂧, ou "phiow-bjij-lhjij-lhjij", ce que l'on peut traduire par « pays-grand-blanc-élevé » (白高大夏國).''',
       'วรรณพงษ์เป็นนักศึกษาชั้นปีที่หนึ่ง เรียนสาขาวิทยาการคอมพิวเตอร์และสารสนเทศคณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์อยู่ที่มหาวิทยาลัยขอนแก่นวิทยาเขตหนองคายยืมคืนทรัพยากรห้องสมุดเอกสารสัมมนาคอมพิวเตอร์ปัญญาประดิษฐ์กับการพัฒนาเกมแมวกินปลาหิวววไหมหลักสูตรใหม่สดสดทนได้',
       'ສົມເດັດພະເຈົ້າຢູ່ຫົວບໍຣົມໂກດຊົງທຳນຸບຳລຸງບ້ານເມືອງແລະພະສາດສະໜາຈົນກ່າວໄດ້ວ່າກຸງສີອະຍຸທະຢາໃນສະໄໝພະອົງນັ້ນເປັນຍຸກທີ່ບ້ານເມືອງດີ ມີຂຸນນາງຄົນສຳຄັນທີ່ເຕີບໂຕໃນເວລາຕໍ່ມາ ໃນລາຊະການຂອງພະອົງຫຼາຍຄົນ ເຊັ່ນ ສົມເດັດພະເຈົ້າກຸງທົນບຸລີ, ພະບາດສົມເດັດພະພຸດທະຍອດຟ້າຈຸລາໂລກມະຫາລາດ ເປັນຕົ້ນ ໃນທາງດ້ານວັນນະຄະດີກໍມີກະວີຄົນສຳຄັນ ເຊັ່ນ ເຈົ້າຟ້າທຳມາທິເບດໄຊຍະເຊດສຸລິຍະວົງ ກົມມະຂຸນເສນາພິທັກ ຫຼືເຈົ້າຟ້າກຸ້ງ ເຊິ່ງເປັນພະໂອລົດ ເປັນຕົ້ນ'
       ]


def test_UnicodeTokenizer():
    tokenizer = UnicodeTokenizer(never_split=["[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]"])
    for l in doc:
        t = tokenizer.tokenize(l)
        logger.info((len(l), l))
        logger.info((len(t), ' '.join(t)))
    tokenizer = UnicodeTokenizer(split_digit=True)
    for l in doc:
        t = tokenizer.tokenize(l)
        logger.info((len(l), l))
        logger.info((len(t), ' '.join(t)))

def test_ZiCutter(dir):
    cutter = ZiCutter(dir=dir)
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)熵😀'\x0000熇"
    tokens = cutter.tokenize(line)
    logger.info(tokens)
    a = cutter.combineHanzi(tokens)
    b = cutter.combineHanzi(''.join(tokens))
    logger.info(a)
    logger.info(b)


def test_build(freq_path, dir, alpha=1):
    if not os.path.exists(dir):
        os.makedirs(dir)
    import logzero
    logzero.logfile(os.path.join(dir, "ZiTokenizerBuild.log"), mode='w')
    tokenizer = ZiTokenizer()
    logger.warning(f" building from {freq_path}")
    word_freq, total = load_frequency(freq_path, alpha=alpha, do_lower_case=tokenizer.do_lower_case)
    assert word_freq
    P = []
    Q = []
    for x in word_freq.items():
        if x[1] >= 2:
            P.append(x)
        else:
            Q.append(x)
    del word_freq
    gc.collect()
    P.sort(key=lambda x: (-x[1], len(x[0]), x[0]))
    Q.sort(key=lambda x: (-x[1], len(x[0]), x[0]))
    word_freq = P+Q
    del P, Q
    gc.collect()
    describe(word_freq, total)
    tokenizer.build(word_freq, total, dir)

    tokenizer = ZiTokenizer(dir)
    doc = os.popen(f" tail {freq_path} -n 1000000 | shuf -n 10 ").read().splitlines()
    doc = [x.split('\t') for x in doc]
    doc = [(k, float(v)) for k, v in doc]
    for k, v in doc:
        tokens = tokenizer.tokenize(k)
        indexs = tokenizer.encode(k)
        words = tokenizer.decode(indexs)
        row = [k, v, ' '.join(tokens), tokenizer.token_word(k), ' '.join(words)]
        logger.info((row))
    return tokenizer


def test_line(tokenizer):
    for line in doc:
        logger.info(line)
        tokens = tokenizer.tokenize(line)
        logger.info(' '.join(tokens))

        indexs = tokenizer.encode(line)
        tokens = tokenizer.decode(indexs)
        line2=tokenizer.tokens2line(tokens)
        logger.info(' '.join(tokens))
        if line2 == line:
            logger.info(line2)
        else:
            logger.warning(line2)


def get_langs():
    langs = os.listdir('C:/data/languages')
    langs = [x for x in langs if not x.startswith('global')]
    langs1 = []
    for lang in langs:
        freq_path = f"C:/data/languages/{lang}/word_frequency.tsv"
        if not os.path.exists(freq_path):
            continue
        langs1.append((lang, freq_path))
    return langs1


if __name__ == "__main__":

    test_UnicodeTokenizer()

    tokenizer = ZiTokenizer()
    test_line(tokenizer)

    tokenizer = ZiTokenizer(split_digit=True)
    test_line(tokenizer)

    folder = "./demo"
    freq_path = f"{folder}/word_frequency.tsv"  # lang="zh_classical"
    test_ZiCutter(folder)
    test_build(freq_path, folder)

    tokenizer = ZiTokenizer(folder)
    test_line(tokenizer)


"""

"""
