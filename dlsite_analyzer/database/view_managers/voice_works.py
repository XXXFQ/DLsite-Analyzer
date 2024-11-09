from ..common import (
    DatabaseManager,
    ViewManagerInterface
)
from ..constants import (
    # ボイス作品テーブル
    VOICE_WORKS_TABLE,
    VOICE_WORKS_PRODUCT_ID,
    VOICE_WORKS_TITLE,
    VOICE_WORKS_URL,
    VOICE_WORKS_CATEGORY_ID,
    VOICE_WORKS_MAKER_ID,
    VOICE_WORKS_AUTHOR_ID,
    VOICE_WORKS_PRICE,
    VOICE_WORKS_POINTS,
    VOICE_WORKS_SALES_COUNT,
    VOICE_WORKS_REVIEW_COUNT,
    VOICE_WORKS_AGE_RATING_ID,
    VOICE_WORKS_FULL_IMAGE_URL,
    # メーカーテーブル
    MAKERS_TABLE,
    MAKER_ID,
    MAKER_NAME,
    # カテゴリーテーブル
    CATEGORY_TABLE,
    CATEGORY_ID,
    CATEGORY_NAME,
    # 作者テーブル
    AUTHORS_TABLE,
    AUTHOR_ID,
    AUTHOR_NAME,
    # 年齢レーティングテーブル
    AGE_RATING_TABLE,
    AGE_RATING_ID,
    AGE_RATING_NAME,
    # ボイス作品ビュー
    VOICE_WORKS_VIEW,
    VOICE_WORKS_VIEW_CATEGORY,
    VOICE_WORKS_VIEW_MAKER,
    VOICE_WORKS_VIEW_AUTHOR,
    VOICE_WORKS_VIEW_AGE_RATING,
)

class VoiceWorksViewManager(ViewManagerInterface):
    def __init__(self, db_manager: DatabaseManager):
        # ビューの情報
        view_info = {
            'name': VOICE_WORKS_VIEW,
            'columns': [
                # [テーブル名].[カラム名] AS [エイリアス]
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_PRODUCT_ID} AS {VOICE_WORKS_PRODUCT_ID}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_TITLE} AS {VOICE_WORKS_TITLE}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_URL} AS {VOICE_WORKS_URL}",
                f"{CATEGORY_TABLE}.{CATEGORY_NAME} AS {VOICE_WORKS_VIEW_CATEGORY}",
                f"{MAKERS_TABLE}.{MAKER_NAME} AS {VOICE_WORKS_VIEW_MAKER}",
                f"{AUTHORS_TABLE}.{AUTHOR_NAME} AS {VOICE_WORKS_VIEW_AUTHOR}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_PRICE} AS {VOICE_WORKS_PRICE}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_POINTS} AS {VOICE_WORKS_POINTS}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_SALES_COUNT} AS {VOICE_WORKS_SALES_COUNT}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_REVIEW_COUNT} AS {VOICE_WORKS_REVIEW_COUNT}",
                f"{AGE_RATING_TABLE}.{AGE_RATING_NAME} AS {VOICE_WORKS_VIEW_AGE_RATING}",
                f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_FULL_IMAGE_URL} AS {VOICE_WORKS_FULL_IMAGE_URL}", 
            ]
        }
        
        # テーブルの情報
        tables = [
            VOICE_WORKS_TABLE,
            MAKERS_TABLE,
            CATEGORY_TABLE,
            AUTHORS_TABLE,
            AGE_RATING_TABLE
        ]
        
        # ビューの結合条件
        joins = [
            f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_MAKER_ID} = {MAKERS_TABLE}.{MAKER_ID}",
            f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_CATEGORY_ID} = {CATEGORY_TABLE}.{CATEGORY_ID}",
            f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_AUTHOR_ID} = {AUTHORS_TABLE}.{AUTHOR_ID}",
            f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_AGE_RATING_ID} = {AGE_RATING_TABLE}.{AGE_RATING_ID}"
        ]
        
        # ビューの並び順
        order_by = f"{VOICE_WORKS_TABLE}.{VOICE_WORKS_PRODUCT_ID}"
        
        super().__init__(db_manager, view_info, tables, joins, order_by)