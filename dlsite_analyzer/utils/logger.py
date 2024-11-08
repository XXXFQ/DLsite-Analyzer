import os
import logging
from datetime import datetime
from pathlib import Path

import colorlog

class Logger:
    def getLogger(name=__name__):
        '''
        ロガーの設定
        
        Parameters
        ----------
        name : str
            ロガー名
        '''
        # ログファイルの保存先を設定
        logfile_dir = Path("./logs")
        logfile_path = logfile_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        if not os.path.exists(logfile_dir):
            os.mkdir(logfile_dir)
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(Logger._get_file_handler(logfile_path))
        logger.addHandler(Logger._get_console_handler())
        logger.propagate = False
        return logger
    
    def _get_file_handler(logfile: str):
        '''
        ファイル出力の設定
        
        Parameters
        ----------
        logfile : str
            ログファイルのパス
        '''
        file_handler = logging.FileHandler(logfile, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(name)s %(message)s'))
        return file_handler
    
    def _get_console_handler():
        '''
        コンソール出力の設定
        '''
        FORMAT = r'%(light_black)s%(asctime)s %(levelname_log_color)s%(levelname)-8s %(purple)s%(name)s %(white)s%(message)s'
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                fmt=FORMAT,
                datefmt='%Y-%m-%d %H:%M:%S',
                secondary_log_colors={
                    'levelname': {
                        'DEBUG': 'cyan',
                        'INFO': 'light_blue',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red'
                    },
                }
            )
        )
        handler.setLevel(logging.DEBUG)
        return handler