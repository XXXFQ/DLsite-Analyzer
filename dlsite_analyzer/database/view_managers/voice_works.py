import pandas as pd

from ..common import (
    DatabaseManager,
    ViewManagerInterface
)
from ..constants import (
    # ボイス作品テーブル
    VOICE_WORKS_TABLE,
    VOICE_WORKS_PRIMARY_KEY,
    VOICE_WORKS_TITLE,
    VOICE_WORKS_URL,
    PRODUCT_FORMAT_FOREIGN_KEY,
    CIRCLES_FOREIGN_KEY,
    VOICE_ACTORS_FOREIGN_KEY,
    VOICE_WORKS_PRICE,
    VOICE_WORKS_POINTS,
    VOICE_WORKS_SALES_COUNT,
    VOICE_WORKS_REVIEW_COUNT,
    AGE_FOREIGN_KEY,
    VOICE_WORKS_FULL_IMAGE_URL,
    # メーカーテーブル
    CIRCLES_TABLE,
    CIRCLE_PRIMARY_KEY,
    CIRCLE_NAME,
    # カテゴリーテーブル
    PRODUCT_FORMAT_TABLE,
    PRODUCT_FORMAT_PRIMARY_KEY,
    PRODUCT_FORMAT_NAME,
    # 作者テーブル
    VOICE_ACTORS_TABLE,
    VOICE_ACTOR_PRIMARY_KEY,
    VOICE_ACTOR_NAME,
    # 年齢レーティングテーブル
    AGE_TABLE,
    AGE_PRIMARY_KEY,
    AGE_RATING_NAME,
    # ボイス作品ビュー
    VOICE_WORKS_VIEW,
    VOICE_WORKS_PRODUCT_FORMAT_VIEW,
    VOICE_WORKS_VIEW_CIRCLE,
    VOICE_WORKS_VIEW_VOICE_ACTOR,
    VOICE_WORKS_VIEW_AGE,
)

class VoiceWorksViewManager(ViewManagerInterface):
    def __init__(self, db_manager: DatabaseManager):
        # ビューの情報
        view_info = {
            'name': VOICE_WORKS_VIEW,
            'columns': [
                # [テーブル名].[カラム名] AS [エイリアス]
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_PRIMARY_KEY} AS {VOICE_WORKS_PRIMARY_KEY}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_TITLE} AS {VOICE_WORKS_TITLE}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_URL} AS {VOICE_WORKS_URL}",
                f"{PRODUCT_FORMAT_TABLE}.{PRODUCT_FORMAT_NAME} AS {VOICE_WORKS_PRODUCT_FORMAT_VIEW}",
                f"{CIRCLES_TABLE}.{CIRCLE_NAME} AS {VOICE_WORKS_VIEW_CIRCLE}",
                f"{VOICE_ACTORS_TABLE}.{VOICE_ACTOR_NAME} AS {VOICE_WORKS_VIEW_VOICE_ACTOR}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_PRICE} AS {VOICE_WORKS_PRICE}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_POINTS} AS {VOICE_WORKS_POINTS}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_SALES_COUNT} AS {VOICE_WORKS_SALES_COUNT}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_REVIEW_COUNT} AS {VOICE_WORKS_REVIEW_COUNT}",
                f"{AGE_TABLE}.{AGE_RATING_NAME} AS {VOICE_WORKS_VIEW_AGE}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_FULL_IMAGE_URL} AS {VOICE_WORKS_FULL_IMAGE_URL}", 
            ]
        }
        
        # テーブルの情報
        tables = [
            VOICE_WORKS_TABLE,
            CIRCLES_TABLE,
            PRODUCT_FORMAT_TABLE,
            VOICE_ACTORS_TABLE,
            AGE_TABLE
        ]
        
        # ビューの結合条件
        joins = [
            f"{VOICE_WORKS_TABLE}.{CIRCLES_FOREIGN_KEY} = {CIRCLES_TABLE}.{CIRCLE_PRIMARY_KEY}",
            f"{VOICE_WORKS_TABLE}.{PRODUCT_FORMAT_FOREIGN_KEY} = {PRODUCT_FORMAT_TABLE}.{PRODUCT_FORMAT_PRIMARY_KEY}",
            f"{VOICE_WORKS_TABLE}.{VOICE_ACTORS_FOREIGN_KEY} = {VOICE_ACTORS_TABLE}.{VOICE_ACTOR_PRIMARY_KEY}",
            f"{VOICE_WORKS_TABLE}.{AGE_FOREIGN_KEY} = {AGE_TABLE}.{AGE_PRIMARY_KEY}"
        ]
        
        # ビューの並び順
        order_by = f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_PRIMARY_KEY}"
        
        super().__init__(db_manager, view_info, tables, joins, order_by)
    
    def get_all_voice_works(self) -> pd.DataFrame:
        '''
        全てのボイス作品情報を取得する
        
        Returns
        -------
        pd.DataFrame
            ボイス作品情報のデータフレーム
        '''
        query = f"SELECT * FROM {self.view_info['name']}"
        res = self.db_manager.execute_query(query)
        return pd.DataFrame(res.fetchall(), columns=self.get_columns())