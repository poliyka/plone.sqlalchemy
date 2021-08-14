# plone.sqlalchemy-14

### 2021/01/01
* 使用 sqlalchemy , alembic 來實現在 `Plone` 中使用ORM技術
---
### 2021/05/01
* 新增 sqlalchemy_mixins 套件 實現類似 `Django ORM` 方法

---
### 2021/08/14
* 更新 sqlalchemy 1.4/2.0
---

# Installation

安裝 library

Library::

```h
    # 需要先手動安裝
    # sudo apt install alembic
    # pip3 install zope.i18nmessageid

    # MySql
    # sudo apt install -y mysql-client
    # sudo apt-get install libmysqlclient-dev
    # sudo apt install libssl-dev
    # sudo apt install libcrypto++-dev
    # pip3 install mysqlclient

    # postgresql
    # pip3 install psycopg2-binary
    # sudo apt install libpq-dev python3-dev
    # pip3 install psycopg2
```

在plone.sqlalchemy/SetupFile 目錄下執行

SetupFile::
```h
    $ make install
    輸入想要建立的專案位置ex. my.package
    檔案會自動建立在專案內

    #如果想參考orm query 指令

    $ cp alchemy_demo.py ../your.package/src/your/package/browser/
    #將他加入 configure.zcml
```


# Usage

1. 設定 alembic.ini
[alembic](https://gitlab.com/mingtakco/plone.sqlalchemy/-/blob/master/DemoFile/alembic.ini#L45)

2. 建立 models 參考 [user.py](https://gitlab.com/mingtakco/plone.sqlalchemy/-/blob/master/DemoFile/models/user.py) and [store.py](https://gitlab.com/mingtakco/plone.sqlalchemy/-/blob/master/DemoFile/models/store.py)

3. 編輯 myAlembic/env.py

4. 在Plone 後台 configlet: ORM setting設定mysql://{account}:{password}@{localhost}:{port}/{database_name}?charset=utf8mb4

# Makefile同層目錄下使用 `make` 指令

Makefile::
```h
    # Complier models

    # m= 如同 git commit -m 'init' 依樣的功能

    $make migration m=init

    # upgrade to database

    $make upgrade
```
