# Hahow UI 自動化程式

UI 自動化程式並且驗證:
1. 此專案裡有幾個合作者，並且分別列出他們的名字
2. 請進入到 frontend.md 並且查看 "Wireframe" 的圖片是否存在
3. 最後一個 commit 的人是誰

# 執行方法

首先，必須確認環境已安裝Python 3以上版本
```
$ python --version
Python 3.4.1
```
安裝執行必要lib
```
pip install selenium
```
clone repository至本機後，在專案根目錄底下執行下面命令
```
# 驗證三個題目
python -m unittest -v ui_test.HahowRecruitTest
```

# 專案流程與架構

此專案選用Selenium WebDriver進行UI自動化測試
搭配Python unittest framework執行測試

執行測試的第一步為確認平台OS，啟動對應的WebDriver
```
hahow_ui_test
|
|-----chromedriver      # chrome webdriver mac64版本
|
|-----chromedriver.exe  # chrome webdriver win32版本
|
|-----ui_test.py        # 測試腳本
```

為了減少外在干預增加測試穩定性，在執行測試過程中隱藏瀏覽器
```
# 如果為True時，在執行測試過程中隱藏瀏覽器；False反之
op.headless = True
```

測試結果會顯示在terminal
```
test_the_last_commiter (ui_test.HahowRecruitTest) ... 
INFO: The last commiter is yinwilliam
ok

----------------------------------------------------------------------
Ran 3 tests in 13.345s
```
有任何的失敗結果會螢幕擷取當下的瀏覽器畫面，測試通過則不會
