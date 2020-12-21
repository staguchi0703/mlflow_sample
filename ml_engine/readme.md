# memo

## Artifactの保存

* 保存先にAWS S3互換のDBが必要
* S3互換ストレージとしてminioを使う
  * 非構造型ストレージ
  * minio/minioコンテナがある
  * login周りの設定を環境変数で与えている
  * 省略すればもっとさっぱり書けそう・・・
  * AWSのpythonCLIである`boto3`が必要
      * ml_engine(minioに保存する)も、tracking(minioに聞きに行く)も、boto3が必要
  * minioってなに？
    * aws s3の分散型ストレージ
    * 複数でクラスタを構成するとこで障害に強い
    * port:9000で公開している
    * webで入るといい感じのUIで中身を見せてくれる
* 立ち上げの設定に一時コンテナが必要

## TODO

* modelの保存
    * 対応中