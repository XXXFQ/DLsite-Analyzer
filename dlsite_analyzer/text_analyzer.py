import re
import unicodedata

import MeCab
import matplotlib.pyplot as plt
import japanize_matplotlib # matplotlibの日本語化
from tqdm import tqdm
from wordcloud import WordCloud

from .config import MECAB_NEOLOGD_PATH

_NEO_TAGGER = MeCab.Tagger(f'-Owakati -d "{MECAB_NEOLOGD_PATH}"')

def extract_words(texts: list, stop_words: list=[]) -> list:
    '''
    テキストのリストから単語を抽出し、リストで返す
    
    Parameters
    ----------
    texts : list
        テキストのリスト
    stop_words : list
        ストップワードのリスト
    
    Returns
    -------
    list
        抽出された単語のリスト
    '''
    documents = [_mecab_tokenizer(text, _NEO_TAGGER, stop_words=stop_words) for text in tqdm(texts)]
    return documents

def generate_wordcloud(word_frequency_data: list | dict, font_path: str='ipaexg.ttf') -> WordCloud:
    '''
    語と出現回数のタプルのリストまたは辞書からワードクラウドを作成し、表示用のオブジェクトを返す。

    Parameters
    ----------
    word_frequency_data : list or dict
        語と出現回数のタプルのリストまたは辞書
    font_path : str, optional
        フォントのパス (デフォルトは 'ipaexg.ttf')
    Returns
    -------
    WordCloud
        作成されたWordCloudオブジェクト
    '''
    if isinstance(word_frequency_data, dict):
        wfdict = word_frequency_data
    else:
        wfdict = dict(word_frequency_data)
    
    wc = WordCloud(background_color='white', font_path=font_path, width=900, height=500)
    wc.generate_from_frequencies(wfdict)
    return wc

def plot_wordcloud(wordcloud_input: list | WordCloud, figsize=(15, 12), filename=None):
    '''
    ワードクラウドを表示し、オプションでファイルに保存する。

    Parameters
    ----------
    wordcloud_input : list or WordCloud
        単語のリストまたはWordCloudオブジェクト
    figsize : tuple, optional
        描画サイズ (デフォルトは (15, 12))
    filename : str, optional
        保存先のファイル名 (指定しない場合は保存しない)
    '''
    if isinstance(wordcloud_input, WordCloud):
        wc = wordcloud_input
    else:
        wc = generate_wordcloud(wordcloud_input)

    plt.figure(figsize=figsize)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    if filename is not None:
        plt.savefig(filename)
    plt.show()

def _mecab_tokenizer(text: str, mecab, target_pos=["名詞", "動詞", "形容詞"], stop_words=[]) -> list:
    '''
    MeCabを用いてテキストを形態素解析し、指定した品詞の単語のリストを返す
    
    Parameters
    ----------
    text : str
        解析対象のテキスト
    mecab : MeCab.Tagger
        MeCabのTaggerオブジェクト
    target_pos : list
        抽出する品詞のリスト
    stop_words : list
        ストップワードのリスト
    
    Returns
    -------
    list
        解析結果の単語のリスト
    '''
    # テキストの前処理
    text = unicodedata.normalize("NFKC", text).upper()
    text = re.sub(r'[【】()（）『』「」]', '', text)  # 全角記号を削除
    text = re.sub(r'[\[\]［］]', ' ', text)  # 半角記号をスペースに変換

    # 形態素解析
    node = mecab.parseToNode(text)
    token_list = []
    kana_re = re.compile("^[ぁ-ゖ]+$")  # ひらがなのみの正規表現

    while node:
        features = node.feature.split(',')
        pos = features[0]  # 品詞
        surface = node.surface

        # 指定の品詞かどうかをチェックし、条件に合致するものを追加
        if pos in target_pos and not kana_re.match(surface) and surface not in stop_words:
            token_list.append(surface)
        
        node = node.next

    return token_list