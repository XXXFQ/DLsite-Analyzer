import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from ..utils import (
    Logger,
    sleep_random
)

logger = Logger.get_logger(__name__)

class VoiceWorkScraper:
    def __init__(self):
        '''
        初期化メソッド
        
        Attributes
        ----------
        base_url : str
            DLsiteのボイス作品一覧ページのURL
        headers : dict
            HTTPリクエストヘッダー
        params : dict
            クエリパラメータ
        '''
        self.base_url = "https://www.dlsite.com/maniax/works/type/=/language/jp/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        self.params = {
            "sex_category[0]": "male",
            "work_category[0]": "doujin",
            "order[0]": "release_d",
            "work_type_category[0]": "audio",
            "work_type_category_name[0]": "ボイス・ASMR",
            "options_and_or": "and",
            "options[0]": "JPN",
            "options[1]": "NM",
            "options_name[0]": "日本語作品",
            "options_name[1]": "言語不問作品",
            "per_page": "100",
            "page": "1",
            "show_type": "3",
            "lang_options[0]": "日本語",
            "lang_options[1]": "言語不要"
        }

    def get_voice_works_response(self, page=1) -> requests.Response:
        '''
        ボイス作品一覧ページのレスポンスを取得
        
        Parameters
        ----------
        page : int
            ページ番号
        
        Returns
        -------
        requests.Response
            レスポンスオブジェクト
        '''
        # ページ番号をクエリパラメータに設定
        self.params['page'] = str(page)
        
        # 完全なURLを構築してGETリクエストを送信
        url = self._build_url()
        response = requests.get(url, headers=self.headers)
        
        # リクエストが成功した場合はランダムな秒数だけスリープ
        sleep_random(2, 4)
        
        return response
    
    def get_voice_works_response_by_url(self, url: str) -> requests.Response:
        '''
        指定されたURLのレスポンスを取得
        
        Parameters
        ----------
        url : str
            レスポンスを取得するURL
        
        Returns
        -------
        requests.Response
            レスポンスオブジェクト
        '''
        response = requests.get(url, headers=self.headers)
        
        # リクエストが成功した場合はランダムな秒数だけスリープ
        sleep_random(2, 4)
        
        return response
    
    def get_total_pages(self, html: str, items_per_page=100) -> int:
        '''
        総ページ数を取得する
        
        Parameters
        ----------
        html : str
            ページのHTMLコンテンツ
        items_per_page : int
            1ページあたりのアイテム数
        
        Returns
        -------
        int
            総ページ数
        '''
        soup = BeautifulSoup(html, "html.parser")
        total_items_element = soup.find("div", class_="page_total")
        if total_items_element:
            total_items_text = total_items_element.find("strong").get_text(strip=True)
            total_items = int(total_items_text.replace(",", ""))
            return -(-total_items // items_per_page)  # 切り上げ除算で総ページ数を算出
        return 1  # デフォルトで1ページ

    def _build_url(self) -> str:
        '''
        クエリパラメータを組み込んだ完全なURLを構築
        '''
        query_string = urlencode(self.params, doseq=True)
        return f"{self.base_url}?{query_string}"
    
    def extract_voice_work_data(self, html: str) -> list:
        '''
        ボイス作品の情報を抽出
        
        Parameters
        ----------
        html : str
            レスポンスのHTML
        
        Returns
        -------
        list
            ボイス作品の情報が格納されたリスト
        '''
        soup = BeautifulSoup(html, "html.parser")
        voice_works_list = soup.find_all("li", class_="search_result_img_box_inner")
        results = []

        for work in voice_works_list:
            url = self._extract_title_and_link(work)["url"]
            response = self.get_voice_works_response_by_url(url)
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch the work page: {url}")
                continue
            
            work_data = {
                "product_id": self._extract_product_id(work), # 作品ID
                "title": self._extract_title_and_link(work)["title"], # タイトル
                "url": self._extract_title_and_link(work)["url"], # URL
                "category": self._extract_category(work), # カテゴリー
                "maker_id": self._extract_maker_id(work), # メーカーID
                "maker": self._extract_maker_name(work), # メーカー名
                "author": self._extract_author_name(work), # 作者名
                "price": self._extract_price(work), # 価格
                "points": self._extract_points(work), # ポイント
                "currency_data": self._extract_currency_data(work), # 通貨データ
                "sales_count": self._extract_sales_count(work), # 販売数
                "review_count": self._extract_review_count(work), # レビュー数
                "age_rating": self._extract_age_restriction(work), # 年齢制限
                "full_image_url": self._extract_full_image_url(work), # フルサイズ画像のURL
            }
            results.append(work_data)

        return results

    def _extract_product_id(self, work: BeautifulSoup) -> str:
        '''
        作品IDの取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        str
            作品ID
        '''
        if product_id_element := work.find("dt", class_="search_img work_thumb"):
            return product_id_element["id"].replace("_link_", "")
        return ""
    
    def _extract_title_and_link(self, work: BeautifulSoup) -> dict:
        '''
        タイトルとリンクの取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        dict
            タイトル情報を含む辞書
        '''
        if title_element := work.find("dd", class_="work_name").find("a"):
            return {
                "title": title_element.get_text(strip=True),
                "url": title_element["href"]
            }
        return {"title": "", "url": ""}
    
    def _extract_category(self, work: BeautifulSoup) -> str:
        '''
        カテゴリーを取得する
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        str
            カテゴリーの名前
        '''
        if category_element := work.find("dd", class_="work_category_free_sample"):
            category_link = category_element.find("div", class_="work_category").find("a")
            if category_link:
                return category_link.get_text(strip=True)
        return ""
    
    def _extract_maker_id(self, work: BeautifulSoup) -> str:
        '''
        メーカーIDの取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        str
            メーカーID
        '''
        attributes_element = work.find("input", {"class": "__product_attributes"})
        if attributes_element and (value := attributes_element.get("value")):
            attribute_list = value.split(",")
            if len(attribute_list) > 0:
                return attribute_list[0]
        return ""
    
    def _extract_maker_name(self, work: BeautifulSoup) -> str:
        '''
        メーカー名の取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        str
            メーカー名
        '''
        if maker_element := work.find("dd", class_="maker_name").find("a"):
            return maker_element.get_text(strip=True)
        return ""
    
    def _extract_author_name(self, work: BeautifulSoup) -> str:
        '''
        作者名の取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        str
            作者名
        '''
        if author_element := work.find("span", class_="author"):
            return author_element.get_text(strip=True)
        return ""
    
    def _extract_price(self, work: BeautifulSoup) -> int:
        '''
        価格の取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        int
            価格
        '''
        if price_element := work.find("span", class_="work_price_base"):
            return int(price_element.get_text(strip=True).replace(",", ""))
        return 0
    
    def _extract_points(self, work: BeautifulSoup) -> int:
        '''
        ポイントの取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        int
            ポイント
        '''
        if point_element := work.find("span", class_="work_point"):
            return int(point_element.get_text(strip=True).strip("pt").replace(",", ""))
        return 0
    
    def _extract_currency_data(self, work: BeautifulSoup) -> str:
        '''
        通貨データの取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        str
            通貨データ
        '''
        if currency_data_element := work.find("div", {"data-vue-component": "currency-price"}):
            return currency_data_element["data-currency_price"]
        return ""
    
    def _extract_sales_count(self, work: BeautifulSoup) -> int:
        '''
        販売数の取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        int
            販売数
        '''
        if sales_count_element := work.find("dd", class_="work_dl"):
            return int(sales_count_element.find("span").get_text(strip=True).replace(",", ""))
        return 0
    
    def _extract_review_count(self, work: BeautifulSoup) -> int:
        '''
        レビュー数の取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        int
            レビュー数
        '''
        if review_container := work.find("dd", class_="work_rating"):
            if review_count_element := review_container.find("a"):
                return int(review_count_element.get_text(strip=True).strip("()"))
        return 0
    
    def _extract_age_restriction(self, work: BeautifulSoup) -> str:
        '''
        年齢制限の取得
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        str
            年齢制限
        '''
        genre_element = work.find("dd", class_="work_genre")
        if genre_element:
            age_rating_element = genre_element.find("span", {"title": True})
            return age_rating_element["title"] if age_rating_element else "R-18"
        return ""
    
    def _extract_full_image_url(self, work: BeautifulSoup) -> str:
        '''
        フルサイズ画像のURLを取得し、https:を付けて返す
        
        Parameters
        ----------
        work : BeautifulSoup
            作品情報が格納された要素
        
        Returns
        -------
        str
            フルサイズ画像のURL
        '''
        if img_element := work.find("div", class_="work_img_popover"):
            if src_value := img_element.find("img").get(":src"):
                # 条件式の中から先頭が`//`で始まるURLを抽出
                urls = src_value.split("'")
                for url in urls:
                    if url.startswith("//"):
                        return f"https:{url}"
        return ""