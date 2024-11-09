import platform
from pathlib import Path

# OSの種類
_pf = platform.system()

# MeCabの辞書のパスを、OSによって変更
if _pf == 'Windows':
    MECAB_NEOLOGD_PATH = Path(r"C:\Program Files (x86)\MeCab\dic\mecab-ipadic-neologd")
else:
    MECAB_NEOLOGD_PATH = Path("/var/lib/mecab/dic/mecab-ipadic-neologd")

# データの保存ディレクトリ
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)

# クロールデータの保存ディレクトリ
RAW_JSON_DATA_DIR = DATA_DIR / 'raw_json'
RAW_JSON_DATA_DIR.mkdir(exist_ok=True)

# アーカイブデータの保存ディレクトリ
ARCHIVE_DIR = DATA_DIR / 'archives'
ARCHIVE_DIR.mkdir(exist_ok=True)

# データベースのパス
DATABASE_PATH = DATA_DIR / 'dlsite_works.db'