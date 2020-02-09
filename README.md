# 概要
csvファイルからTableau独自のデータ形式であるhyperファイルを作成する。

# 使い方

## ファイル配置

1. `input/`にhyperファイルで出力したいcsvファイルを配置する
1. `table_def/`に`input/`に配置したcsvファイルそれぞれに対応するカラム定義(jsonファイル)を配置する

### jsonファイル凡例
カラム名がkey、データ型やNULL制約のdictをvalueに持たせる。

#### データ型(type)
以下のいずれかを設定する。

- BIG_INT
- TEXT
- DOUBLE
- DATE
- TIMESTAMP

#### NULL制約(nullable)
以下のいずれかを設定する。

- YES
- NO

例）
```
{
    "PassengerId":{"type":"BIG_INT","nullable":"NO"},
    "Survived":{"type":"BIG_INT","nullable":"NO"},
    "Pclass":{"type":"BIG_INT","nullable":"NO"},
    "Name":{"type":"TEXT","nullable":"NO"},
    "Sex":{"type":"TEXT","nullable":"NO"},
    "Age":{"type":"DOUBLE","nullable":"YES"},
    "SibSp":{"type":"BIG_INT","nullable":"NO"},
    "Parch":{"type":"BIG_INT","nullable":"NO"},
    "Ticket":{"type":"TEXT","nullable":"NO"},
    "Fare":{"type":"DOUBLE","nullable":"YES"},
    "Cabin":{"type":"TEXT","nullable":"YES"},
    "Embarked":{"type":"TEXT","nullable":"YES"}
}
```

## コンテナ実行
以下を実行することでhyperファイルを出力できる。
hyperファイルは`output/`に出力される。


```
docker-compose run hyper
```