## 概要
* python有名フレームワーク、djangoのチュートリアル実践。

## 参考
* [django 1.10 チュートリアル](https://docs.djangoproject.com/ja/1.10/intro/)

## djangoコマンド覚書
* 空のアプリケーション作成
  * `django-admin startproject (プロジェクト名)``
* アプリケーション作成
  * `python manage.py startapp (アプリ名)`
* 開発用のwebサーバ起動
  * `python manage.py runserver`
* マイグレーションファイルの作成
  * `python manage.py makemigrations (アプリ名)`
* 実際のマイグレーションの実施
  * `python manage.py migrate`
* マイグレーションの結果を表示する
  * `python manage.py sqlmigrate (アプリ名) (マイグレーション番号)`
* Python対話環境の開始(djangoに必要な環境変数を設定した上で)
  * `python manage.py shell`
* 特定アプリに対するテストの実施
  * `python manage.py test (アプリ名)`

## tips
### django-debug-toolbar
* あるページをロードするのにかかった時間や、実行したSQLを表示してくれるデバッグツール。
* インストールは、公式ドキュメントが一番参考になる。
  * [Django Debug Toolbar Installation](https://django-debug-toolbar.readthedocs.io/en/stable/installation.html)
* また、特定の条件を満たさないと、debug-toolbarが表示されなくなるようだ(今回のサンプルではbodyで閉じていなくて詰まった)。
  * グローバル変数DEBUGがTrue。
  * レスポンスのタイプがtext/html。
  * レスポンスとして返るhtmlが</boby>で閉じられていること。
  * [Django Debug Toolbar Tips](https://django-debug-toolbar.readthedocs.io/en/stable/tips.html)