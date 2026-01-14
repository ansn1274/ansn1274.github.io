---
title: "用Python 輕鬆取得NBA 所有數據"
source: "https://www.codegym.tech/blog/python-nba-api"
author:
published:
created: 2026-01-13
description: "用Python優雅的處理NBA比賽數據，繪製出球員投籃熱點，讓你看懂資料背後的故事"
tags:
  - "clippings"
---
![NBA shot chart - Code Gym](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/2c68fc6-e3d-e617-8e44-8a3f42f8ec_shotchart1.jpg)

用Python優雅的處理NBA比賽數據，繪製出球員投籃熱點，讓你看懂資料背後的故事，2021 年Stephen Curry 打破了Ray Allen 的紀錄，成為NBA 史上投進三分球最多的球員，Curry 之後所投進的每一顆三分球，都是將這個紀錄推升到一個新的高度，他是NBA 史上最偉大的三分球射手，這是無庸置疑的，但你知道他每年投進的三分球位置，都有所不同嗎？

**![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/1e4f362-453a-a015-c3c2-836cb2a086fa_rayallen.jpg)**

下方圖表是我用Python 程式語言，繪製出Curry 從2014 年到2023 年之間，出手投進的位置圖，顏色越深，代表他在這個位置投進的次數越多，我們可以透過這樣的方式觀察到他在不同球季習慣出手的位置，讓我們可以更近一步的提出新的問題，產生新的觀點，這是Curry 在2015-16 球季的出手位置，我們可以觀察到他的出手位置散佈在整個三分線，但是我們觀察隔年2016-17 球季的出手位置，則是較為集中在幾個特定的位置，很有可能是球隊戰術改變，或是Curry 自己做了一些調整，但我想長期觀看NBA 的球迷應該猜得到那一年發生了什麼事，那一年Kevin Durant 加入了勇士隊，成為了Curry 的隊友，並且在同一年拿到了NBA 總冠軍，我會將繪製圖表的Python 程式碼提供給你，讓你可以透過和我一樣的方式，觀察其他球員習慣出手投籃的位置，這篇文章我也會教你如何取得NBA 官網的其他資料，和透過一個免費開放的Python 模組，操作這些數據和分析資料。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/f86f0d-bcb2-2480-e66a-eb57362d838_shotchart2.jpg)

---

## NBA 官網上取得API 網址的方式

我大概是在Michael Jordan 打棒球回來後開始看NBA 的，我那個時候取得球員資訊的方式比較貧乏一點，大都是透過報紙或雜誌的講評，來深入了解球員的一些細節，現在取得資訊的方法豐富了許多，但缺點就是大家都有各自的觀點，有時候這樣的討論會從善意的分享觀點，慢慢演變成我才是對的的爭論，這類的爭論常常會影響到我自己觀賽的興致，最後我還是回到球員和球賽的原始數據，挖掘自己感興趣的資訊。我想作為球迷，我們都會希望自己能夠更近一步探索和閱讀比賽，提出一些自己有趣的觀點，增加自己在觀賞比賽時的樂趣，我想NBA 官方的確是有注意到這點，所以他們提供了很多比賽的數據給我們，你可以在NBA 官網上找到Stats 頁面，這裡提供了NBA 賽場上的所有數據資料，像是針對球員的投籃數據，以剛才提到的Curry 為例，這是他在球場上不同位置的出手次數和命中率，我們可以透過這個表格中的資料，了解一位球員擅長的投籃位置。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/6bd1334-136d-eeea-5d08-622b867ce2_nba_stats.jpg)

我們在NBA 官網上看到的數據資料都是可以直接透過網址下載，我現在來教你怎麼取得這些原始資料，我用Curry 在官網上的球員頁面來示範說明，這個頁面會列出球員的基本資料，生涯的平均得分、籃板這些基本資訊，往下滑動會看到過去每一季的數據，除了傳統的數據以外，還有一些進階的數據資料，如果我們想要單純取得這些表格中的資料該怎麼做呢？我們用Python 寫爬蟲程式是一種方式，但如果能直接取得JSON 格式的資料會更方便，從開發人員的角度來看，這個頁面分成網頁設計和資料兩個部分，我們在上面看到的表格，資料擺放位置都是透過HTML, CSS 的語法設計，這個template 不管哪一個球員都是一樣的，差別只在於資料不同，NBA 官網將頁面的數據資料用API 的方式分開處理，我們只要查得到這個網頁提供資料的API 網址就可以取得資料了，我們可以用Chrome 瀏覽器的開發人員工具，尋找API 網址，我們可以在Network 頁籤下的Fetch/XHR，看到這個網頁需要很多JSON 格式的檔案，通常提供資料的API 網址，會帶有一些資料內容的關鍵字，像是這個網址仔細看得話是，player dashboard by year over year combined，也就是球員同比綜合表現儀表板，我點選這個檔案後，可以在右邊header 頁籤看到Request URL，也就是我們要取得資料的API 網址，你可以看到這串網址相當長，因為後面放了一堆參數，我們要透過這些參數來決定取得的資料內容，像是這裡有一個參數是PlayerID 201939，這個就是Curry 在NBA 的球員ID，這串ID 也可以在這個網頁上的網址上找得到，網址最後的一串數字也是201939，我們除了要將這一串網址中的參數準備好以外，還要準備好Request Header 中的其他資訊一起丟給主機，才能夠取得我們想要的資料，這個資料回傳的內容，我們可以透過標籤Response 觀察結果，這是一個JOSN 格式的資料，裡面有網頁上出現的歷年數據，而這個頁面就是透過瀏覽器，將設計好的HTML, CSS 和JSON 檔案，渲染成一個我們使用者容易閱覽的網頁，如果我們單純只想取得資料，快速分析數據，可以直接透過這串API 網址下載JSON 檔案，然後用Python 和Pandas 處理會很快速又方便。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/0f3662-fa2-185-a0b2-0a3d555bd66_collage.jpg) ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/4df8852-8315-6a4-f7b3-535c217283c__2023-07-31_9.18.03.jpg)

## Python 模組NBA\_API

雖然我們知道如何在網頁上取得API 網址，但這種取得資料的作法，仍然有幾個 **缺點**:

- 第一個就是網址太長了，我們在程式中要處理這麼長的字串很不容易，少一個符號，漏掉一個字母就沒辦法正確取得資料
- 第二個問題就是傳遞的參數太多了，有的參數必須要輸入，有得可以選擇性輸入
- 第三個就是整個NBA 官網提供的API 很多，我們如果想要找球員出手投籃的數據，都不知道該從哪一個API 開始，只能不斷地在許多網頁中搜尋

但是如果有人已經幫我們將所有API 整理出來，透過函式輸入幾個必要的參數，甚至連常用的參數格式都幫我們包好，用起來就像是一般的Python 模組就太好了，所以我要和你介紹一個Python 模組 [nba\_api](https://github.com/swar/nba_api/tree/master) ，這個模組是放在Github 上的open source，你可以直接用pip instal 安裝這個模組，這個模組的優點不只是將複雜的API 網址包起來，它的文件和範例也做得很好，社群的討論也很踴躍，如果你在使用過程中遇到問題可以獲得其他網友的協助。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/4bdd1f-ef3-5ac2-2f74-7d42baadaf0__2023-07-31_9.22.59.jpg)

我往下滑動會看到文件Doucment ，其中有一個 [endpoint 介紹](https://github.com/swar/nba_api/tree/master/docs/nba_api/stats/endpoints) ，這是所有NBA 數據的API 表單，有了這個表單，你就不用像是無頭蒼蠅一樣，在每一個網頁中尋找API 網址了，這裡的每一個endpoint 都對應到一組NBA 數據，例如endpoint [playbyplayv2](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playbyplayv2.md) ，NBA 的每一場比賽都會有一個網頁，這個網頁的網址會有一串數字，這串數字就是這場比賽的ID，這個頁面提供這場比賽的簡介，球員的比賽紀錄，你可以在Play-By-Play 頁籤，看到球場上發生的每一個事件，不管是投籃、抄截或籃板，都會依據時間呈現在這個頁面上，球員在賽季中的所有紀錄，都是從這一場又一場的比賽數據中堆疊起來的，在endpoint 下方會告訴你說你要使用這個API 需要輸入哪些參數，像是Game ID 就是我才介紹網址中的那一串數字，除了透過網頁的方式找到Game ID，也可以透過其他API 取得，不過這就比較複雜一點，我這次影片會先簡單介紹一些基本功能，之後有機會再詳細介紹透過多個API ，彼此互相串接資料的示範，我再往下滑動，會看到API 回傳的JOSN 欄位，我們可以透過這些JSON 欄位，在程式中撰寫取得相對應的資料，接下來我就會透過這個play by play API ，示範如何使用這個模組，還有這組API 呈現的資料結果。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/0afa417-56e6-001d-e7e1-e0a6bc6ebef__2023-07-31_9.26.30.jpg)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/0cc8f2-c15-8f24-a5d-7418bb58ee__2023-07-31_9.28.04.jpg)

---

## 程式碼示範

你可以在jupyter notebook 執行下方程式碼，或是其他你習慣使用的IDE，你可以透過 [Code Gym 上面的免費課程](https://www.codegym.tech/free-python-tutorial) 學習如何安裝或是操作Python ，如果你有安裝過Python 環境，也可以直接透過純文字檔編輯器撰寫程式碼，接下來我要示範如何從模組nba\_api 取得NBA 球員的資料，你可以從模組下的stats.static，匯入players，我可以用這個模組取得球員的資訊，我宣告一個變數nba\_players，這會存放所有球員的資料，接著我用剛才匯入進來的players，呼叫函式get\_players 取得所有球員的資料，兩行程式碼就完成了，你不用再去NBA 官網找API 網址，然後放一堆參數組字串，接著我把結果列印出來看看，執行一下，執行之後你會看到下方出現JOSN 格式的資料內容，這裡的欄位有id 也就是我剛才提過的球員ID，然後還有名字，最後一個欄位is\_active，就是指球員是否還在打NBA，像是Jabbar已經退休了，他的狀態就會是false，我們可以用這組資料，查詢球員的名字，然後取得球員ID。

```
from nba_api.stats.static import players

nba_players = players.get_players()
nba_players
```

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/e4f5bd0-1402-86ae-2a33-d66741fb602__2023-07-31_5.10.51.jpg)

我們通常最熟悉球員的資訊就是他的名字，所以我們可以用名字查詢他的其他資訊，我宣告一個變數name，我用Stephen Curry 來示範，我用for 迴圈來跑剛才取得的球員資料，因為是JSON 格式的資料，所以我們用Python 處理起來會很方便，我現在要找到球員名字和變數name 相同的資料，我用關鍵字if，判斷player 中的欄位full\_name ，是否等於變數name，如果相同的話就列印出球員的id。

```
name = 'Stephen Curry'
for player in nba_players:
    if player['full_name'] == name:
        print(player['id'])
```

我用剛才介紹球賽資訊的頁面做示範，這場比賽是太陽對快艇，上方的網址有一串數字，這就是每一場比賽的Game ID，我們可以用這個ID 取得球賽的數據資料，我這次用比較直覺、簡單的方式取得Game ID，但是你可以透過其他API 取得相同的Game ID，這裡我先示範當你有了Game ID 之後你要如何繼續。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/38e38d-62a7-c64a-06ad-a30dda36f063__2023-07-31_9.33.24.jpg)

首先我匯入模組下的stats.endpoint，匯入playbyplayv2，接著我宣告變數pbp，這是要存放抓回來的比賽數據，我用剛才匯進來的模組，建立一個PlayByPlayV2的物件，在參數game\_id 貼上剛才複製下來的比賽ID，剛才的示範我是直接使用回傳的JSON 檔操作資料，這次我要用DataFrame 操作資料，DataFrame 是模組Pandas 中的類別，我們可以使用DataFrame 操作更多複雜的資料分析，我宣告一個變數df1，這是存放DataFrame 的物件，我用剛才取得的比賽資料pbp，用函式get\_data\_frames，將資料轉為DataFrame 格式的物件，因為回傳的資料是一個List，我們需要的資料在第一筆，所以我用索引值0 取得回傳的比賽資料，如果你想要匯出成一個csv 檔，可以直接用函式to\_csv 匯出，我們只要在函式中放入檔案的路徑位置就可以了，打開下載的檔案後就是這場比賽的所有資料，球賽中每一個事件都會被記錄下來，球員得分是誰助攻的，球員犯規是哪一位裁判吹的都會記錄下來，其中有一個欄位是PLAYAER1\_ID，它紀錄事件中主要球員的ID，像是得分的球員，搶下籃板的球員，如果是助攻的球員就會被記錄在PLAYAER2\_ID的欄位，你可以透過這兩個欄位分析出這場比賽哪兩位球員合作得分的次數最多。

```
from nba_api.stats.endpoints import playbyplayv2

pbp = playbyplayv2.PlayByPlayV2(game_id='0022200043')
df1 = pbp.get_data_frames()[0]
df1.to_csv('/Users/codegym/tmp.csv')
```

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/307bc43-2e0a-bde1-c7ca-8a0ecd8afe8f__2023-07-31_5.19.58.jpg)

我現在想要示範，找出這場比賽Paul George 主要參與的事件。我使用剛才找出來的比賽資料df1，在中括弧中放入過濾條件，我要過濾出欄位PLAYER1\_ID 等於202331，這是Paul George的ID，這樣就可以過濾出我們想要的資料執行之後，下方就會出現這場比賽所有Paul George 參與的事件，不管是得分、籃板、失誤或犯規都會在這份表格當中，Pandas 是Python 程式語言中處理資料分析最重要的模組，你可以透過Pandas 快速過濾出你想要的資訊，不需要寫迴圈來判斷資料是否相同，如果你想要學習更多有關資料分析的技術，可以參考Code Gym 線上課程 [Python 資料分析課程](https://www.codegym.tech/python-data-analysis) ，課程單元是用不同領域的資料作為教學範例，幫助你透過實際數據資料學習正確的資料分析觀念。

```
df1[df1['PLAYER1_ID'] == 202331]
```

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/1fe5f7f-426d-af80-2fbb-3f2f614f336__2023-07-31_5.21.59.jpg)

最後我想示範如何取得球員在球場上出手投籃的位置資訊，球員在場上出手投籃的endpoint 名稱是shotchartdetail，我要從模組下的stats.endpoints，匯入shotchartdetail，我這次示範想要找另一位球員Dirk Nowitzki，我宣告變數scd，從匯入的模組中建立一個新的ShotChartDetail物件，初始化參數player\_id，我輸入Nowitzki 的球員ID，team\_id則是輸入小牛隊的ID，然後要輸入球季的參數，我選擇2010-11 球季，這一年小牛隊他們拿到了第一座NBA 總冠軍，接著我宣告變數df2，這是回傳後的DataFrame 資料，然後我和剛才一樣使用函式get\_data\_frames 取得資料，選擇索引值為0的元素，最後列印出來看看結果，執行之後，下方就跑出Nowitzki 在這一年出手投進的所有資料，我將資料往右邊滑動，你會看到這裡有兩個欄位，分別是在球場上X和Y 的座標位置，我們可以使用這組資料繪製出球員出手投籃的位置圖。

```
from nba_api.stats.endpoints import shotchartdetail

scd = shotchartdetail.ShotChartDetail(player_id='1717', team_id ='1610612742', season_nullable='2010-11')
df2 = scd.get_data_frames()[0]
df2
```

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/ebba20-4046-1b74-84d3-0a217d46fcc5__2023-07-31_5.24.27.jpg)

---

## 繪製球員出手投籃位置程式碼

我們要繪製這張圖之前，有一件麻煩事要做，就是要畫出整個籃球場的匡線，包括禁區、三分球和籃球筐，我已經將這些程式碼包起來，放在函式create\_court裡面，然後用函式shot\_chart 繪製出球員的投籃出手位置，接著你就可以在下一個cell 輸入球員名字，球隊名稱縮寫和球季年份，準備好這些資料後就可以繪製出這樣的圖表，這張圖是球員所有出手的位置，你會注意到大部分都集中在籃下，這會造成外線的投籃區域顏色較淺，無法明顯區分出投籃次數的多寡，所以還有另一種作法，你可以在參數中的RA放入false，這是將籃筐下的區域排除掉，只留下灌籃、擦板以外的投籃方式，這樣外線投籃的顏色強弱才會比較明顯，我們也能夠更清楚的觀察的球員擅長出手得分的區域。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/d3a7088-1354-84fb-e3da-e0d206c47d88__2023-07-31_9.46.13.jpg)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/blogs/2147488715/images/007d7d2-dfb-eae-25f6-ce88660ff64__2023-07-31_9.47.40.jpg)

你可以點選下方連結，填入你的email後，系統會自動發送程式碼給你，如果你也是喜歡透過NBA 的資料，分析比賽和球員，希望這篇文章能夠帶給你一些啟發和樂趣，歡迎轉貼和分享，我是Code Gym 的Ryan，如果有任何建議和指教，請在官網留言或發送email 給我，謝謝！

[Code Gym 程式碼網址下載](https://www.codegym.tech/code-gym-nba-code)

Code Gym 線上課程

[Python 資料分析](https://www.codegym.tech/python-data-analysis)

[Python 自動化工作術](https://www.codegym.tech/python-automate)

## Youtube 影片閱覽

![](https://www.youtube.com/watch?v=r3fwHdpbpe8)

#### 【Python 自動化工作術】試閱課程

請您填寫下方資訊，即可收到更多試閱課程，謝謝！