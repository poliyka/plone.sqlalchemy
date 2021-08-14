# Mingtak.ORM

使用 sqlalchemy , alembic 來實現在 `Plone` 中使用ORM技術
新增 sqlalchemy_mixins 套件 實現類似 `Django ORM` 方法

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

將mingtak.ORM/DemoFile 目錄下的檔案放到指定位置

DemoFile::
```h
    $cp Makefile ../your.package/src/your/package/

    $cp alembic.ini ../your.package/src/your/package/

    $cp -r models ../your.package/src/your/package/

    $cp -r myAlembic ../your.package/src/your/package/

    # 使用mrbob會自動跑isort，會有bug，加入.isort.cfg排除資料夾
    $cp -r .isort.cfg ../your.package/src/

    #如果想參考orm query 指令

    $cp view.py ../your.package/src/your/package/browser/

    #將他加入 configure.zcml
```

將剛才所有複製的檔案文件中含 mingtak.ORM 改成 your.package

# Usage

1. 設定 alembic.ini
[alembic](https://gitlab.com/mingtakco/mingtak.ORM/-/blob/master/DemoFile/alembic.ini#L45)

2. 建立 models 參考 [user.py](https://gitlab.com/mingtakco/mingtak.ORM/-/blob/master/DemoFile/models/user.py) and [store.py](https://gitlab.com/mingtakco/mingtak.ORM/-/blob/master/DemoFile/models/store.py)

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
