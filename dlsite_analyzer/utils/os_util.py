import random
from time import sleep

def sleep_random(min: int, max: int):
    '''
    minからmaxまでの間のランダムな秒数だけスリープする
    
    Parameters
    ----------
    min : int
        最小値
    max : int
        最大値
    '''
    value = random.uniform(min, max) # minからmaxまでの間のランダムな秒数を取得
    sleep(value)