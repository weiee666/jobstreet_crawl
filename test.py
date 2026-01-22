from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://sg.jobstreet.com/data-jobs?sortmode=ListedDate')

# 等待页面加载并绕过验证
page.wait.load_start()
print(page.html) # 获取渲染后的 HTML