# ボイス作品テーブル
VOICE_WORKS_TABLE = 'voice_works'
VOICE_WORKS_PRIMARY_KEY = 'id'
VOICE_WORKS_TITLE = 'title'
VOICE_WORKS_URL = 'url'
PRODUCT_FORMAT_FOREIGN_KEY = 'product_format_id'
CIRCLES_FOREIGN_KEY = 'circle_id'
VOICE_ACTORS_FOREIGN_KEY = 'voice_actor_id'
VOICE_WORKS_PRICE = 'price'
VOICE_WORKS_POINTS = 'points'
VOICE_WORKS_SALES_COUNT = 'sales_count'
VOICE_WORKS_REVIEW_COUNT = 'review_count'
AGE_FOREIGN_KEY = 'age_id'
VOICE_WORKS_FULL_IMAGE_URL = 'full_image_url'

# サークルテーブル
CIRCLES_TABLE = 'circles'
CIRCLE_PRIMARY_KEY = 'id'
CIRCLE_NAME = 'name'

# 製品形式テーブル
PRODUCT_FORMAT_TABLE = 'product_format'
PRODUCT_FORMAT_PRIMARY_KEY = 'id'
PRODUCT_FORMAT_NAME = 'name'

# 声優テーブル
VOICE_ACTORS_TABLE = 'voice_actor'
VOICE_ACTOR_PRIMARY_KEY = 'id'
VOICE_ACTOR_NAME = 'name'

# 年齢指定テーブル
AGE_TABLE = 'age'
AGE_PRIMARY_KEY = 'id'
AGE_RATING_NAME = 'name'

# ボイス作品ビュー
VOICE_WORKS_VIEW = 'voice_works_view'
VOICE_WORKS_PRODUCT_FORMAT_VIEW = 'product_format'
VOICE_WORKS_VIEW_CIRCLE = 'circle'
VOICE_WORKS_VIEW_VOICE_ACTOR = 'voice_actor'
VOICE_WORKS_VIEW_AGE = 'age'