# DLsite-Analyzer

## 概要
このプロジェクトは、[DLsite](https://www.dlsite.com)から取得したテキストデータを解析し、ASMRやボイス作品に関する分析を行うツールです。
主な機能は以下の通りです。
- データベースからの単語抽出
- MeCabを使用したテキスト解析
- Matplotlibを使用したワードクラウドの生成と表示

## 特徴
- DLsiteのASMR・ボイス作品のタイトルから頻出単語を抽出
- 単語の頻度をワードクラウドで視覚化
- 日本語テキスト対応 (`japanize_matplotlib`を使用)

## 必要要件
- Python 3.x
- MeCabおよびmecab-python3
- Matplotlib
- WordCloud
- Pandas
- japanize-matplotlib

## 著作権表示
© 2024 ARM
