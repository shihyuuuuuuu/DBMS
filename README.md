# A small DBMS using pymysql and PyQt5

## 系統架構與環境
```
$ uname -a
Linux shihyu 4.18.0-16-generic #17~18.04.1-Ubuntu SMP Tue Feb 12 13:35:51 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```
- OS版本：Ubuntu 4.18.0-16-generic
- python版本：3.6.7
- 使用pymysql函式庫
- 使用PyQt5製作GUI介面

## 介面截圖與使用說明

- 主程式為```dbms.py```
- 執行：```python3 dbms.py```
- 程式畫面：
![](https://i.imgur.com/2C83fOv.png =400x)
- 上面的Text Box可以輸入SQL指令，輸入完成後按下「執行SQL!」按鈕就可以執行該指令
- 下面的按鈕則是可以執行嵌入的SQL語法
    - 第一排是 Basic Queries
    - 第二排是 Complex Queries
- 最下方的空間則會以表格呈現query的結果

## ER Diagram
![](https://i.imgur.com/cpLmU4h.png)

## Relation Schema
![](https://i.imgur.com/T00jfbf.png)

## 各Entity間的意義與關係
這整個資料庫是用來儲存某籃球聯賽的比賽資訊。
內容包括球員、球隊、球隊母公司、體育場館、比賽等等

五個實體：
- Player: 球員，屬性有年齡、生日、背號、所屬球隊
- Team: 球隊，屬性有隊名、教練、創立年份
- Company: 球隊母公司，屬性有公司編號、地點、公司名稱、旗下球隊
- Stadium: 體育場館，屬性有場館名稱、地點、座位數、啟用日期、掌管球隊
- Game: 比賽，屬性有比賽編號、比賽日期、主隊、客隊、比賽場館

實體間的關係：
- 球員一定屬於某一支球隊，球隊可以擁有多名球員
- 球隊一定屬於某一公司，一個公司只能有一支球隊
- 每個場館都有所屬球隊在經營
- 每場比賽會選擇一個場館舉辦
- 每場比賽會有兩支球隊參加，一支為主隊、一支為客隊
