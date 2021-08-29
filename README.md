# plone.sqlalchemy-14

### 2021/08/14

- 更新 sqlalchemy 1.4/2.0

---

### 2021/05/01

- 新增 sqlalchemy_mixins 套件 實現類似 `Django ORM` 方法

---

### 2021/01/01

- 使用 sqlalchemy , alembic 來實現在 `Plone` 中使用 ORM 技術

---

# Installation

`Library`

```h
//需要先手動安裝
sudo apt install alembic
pip3 install SQLAlchemy>=1.4.22
pip3 install zope.i18nmessageid

//MySql
sudo apt install -y mysql-client
sudo apt-get install libmysqlclient-dev
sudo apt install libssl-dev
sudo apt install libcrypto++-dev
pip3 install mysqlclient

//postgresql
pip3 install psycopg2-binary
sudo apt install libpq-dev python3-dev
pip3 install psycopg2
```

`SetupFile`

plone.sqlalchemy/SetupFile 目錄下執行

```h
$ make install
//輸入想要建立的專案位置ex. my.package
//檔案會自動建立在專案內

//如果想參考 Query Method 請參考
alchemy_demo_14.py
```

# Usage

1. 設定 alembic.ini
   [alembic](https://github.com/poliyka/plone.sqlalchemy/blob/f18a66b6a23ed1bbc54676e3d24d84b630b7e85a/SetupFile/alembic.ini#L42)

2. 建立 models 參考 [user.py](https://github.com/poliyka/plone.sqlalchemy/blob/master/SetupFile/models/user.py) and [store.py](https://github.com/poliyka/plone.sqlalchemy/blob/master/SetupFile/models/store.py)

3. 編輯 Alembic/env.py

4. Plone後台 configlet: ORM setting 設定 mysql://{account}:{password}@{localhost}:{port}/{database_name}?charset=utf8mb4

# Makefile 同層目錄下使用 `make` 指令

`Makefile`

```h
// 如同 git commit -m 'init' 依樣的功能
// 會記錄變更在versions中
$ make migrate m=init

// upgrade to database
$ make upgrade
```
