from pathlib import Path

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