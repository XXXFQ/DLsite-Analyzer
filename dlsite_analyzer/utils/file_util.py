import os
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

from ..utils import Logger

logger = Logger.getLogger(__name__)

def load_json(file_path: str, encoding='UTF-8') -> dict:
    '''
    指定されたファイルパスのJSONファイルを読み込む
    
    Parameters
    ----------
    file_path : str
        読み込むファイルのパス
    encoding : str
        エンコーディング
    
    Returns
    -------
    dict
        読み込んだデータ
    '''
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return json.load(file)
    except FileNotFoundError:
            return {}

def save_json(data: dict, file_path: str, indent=4, encoding='UTF-8',ensure_ascii=True):
    '''
    指定されたファイルパスにJSONファイルを書き込む
    
    Parameters
    ----------
    data : dict
        書き込むデータ
    file_path : str
        書き込むファイルのパス
    indent : int
        インデント
    encoding : str
        エンコーディング
    ensure_ascii : bool
        ASCII文字のみでエンコードするかどうか
    '''
    with open(file_path, 'w', encoding=encoding) as file:
        json.dump(data, file, indent=indent, ensure_ascii=ensure_ascii)

def create_output_directory(output_dir_path: str) -> Path:
    '''
    出力ディレクトリを作成する
    
    Parameters
    ----------
    output_dir_path : str
        出力ディレクトリのパス
    
    Returns
    -------
    Path
        出力ディレクトリのPathオブジェクト
    '''
    output_dir = Path(output_dir_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def cleanup(directory_path: str):
    '''
    ディレクトリを削除して新しく作成する
    
    Parameters
    ----------
    directory_path : str
        ディレクトリのパス
    '''
    directory = Path(directory_path)
    shutil.rmtree(directory)
    directory.mkdir(exist_ok=True)
    logger.info(f"Deleted {directory_path} and created a new one.")

def archive_and_zip_files(files: list, outdir: str):
    '''
    ファイルをアーカイブしてZIP形式で保存する
    
    Parameters
    ----------
    files : list
        アーカイブするファイルのリスト
    outdir : str
        ZIPファイルを保存するディレクトリのパス
    '''
    if not files:
        print("アーカイブするファイルがありません。")
        return False
    
    # アーカイブ先ディレクトリのパスを作成
    archive_transfer_path = Path(outdir) / str(datetime.now().strftime("%Y-%m-%d-%H%M%S"))
    
    # アーカイブ先ディレクトリを作成
    os.makedirs(archive_transfer_path, exist_ok=True)
    
    # ファイルをアーカイブ先ディレクトリに移動
    for file in files:
        shutil.move(file, archive_transfer_path)
    
    # ZIP形式でアーカイブ
    shutil.make_archive(archive_transfer_path, 'zip', root_dir=archive_transfer_path)
    
    # アーカイブしたファイルを削除
    shutil.rmtree(archive_transfer_path)
    
    logger.info(f"The archive is complete, and the ZIP file has been saved to {outdir}.")
    return True

def unzip_file(zip_file_path: str, outdir: str):
    '''
    zipの解凍
    
    Parameters
    ----------
    zip_file_path : str
        ZIPファイルのパス
    outdir : str
        解凍先のディレクトリのパス
    '''
    try:
        with zipfile.ZipFile(file=zip_file_path) as zip_ref:
            zip_ref.extractall(path=outdir)
    except FileNotFoundError as e:
        logger.error(e)