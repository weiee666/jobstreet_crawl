import random
import re
import time

import requests
import csv
from lxml import etree
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from DrissionPage import ChromiumPage

class JinJiangSpider():
    
    def __init__(self):
        self.cookies = {
            "sol_id": "85417788-be4d-414c-9f5c-7fca459294b6",
        "__cf_bm": "EZ7UV762a0JWZORZGbhSTmUzyIU4iqPzXpYOzMcWQQY-1768895565-1.0.1.1-KR46FOj_yoCKvxh.C7h20jt1AcUboy2LIoHf9etL7RCHexk8b8nFtvA7J6qqGNnXUDDZqq1PCuv_UvxlLg3IDpWeIC2MclX7QrLSKGGR0jA",
        "JobseekerSessionId": "f4f7e7d1-d607-423f-a865-b2948c040155",
        "JobseekerVisitorId": "f4f7e7d1-d607-423f-a865-b2948c040155",
        "da_cdt": "visid_019b9ca2531b001a1b4d1e9aaf3605077001906f00bd0-sesid_1768891442966-hbvid_85417788_be4d_414c_9f5c_7fca459294b6-tempAcqSessionId_1768891442976-tempAcqVisitorId_85417788be4d414c9f5c7fca459294b6",
        "hubble_temp_acq_session": "id%3A1768891442976_end%3A1768897356757_sent%3A295",
        "main": "V%7C2~P%7Cjobsearch~K%7Cdata~SORT%7CListedDate~OSF%7Cquick&set=1768895556593/V%7C2~P%7Cjobsearch~K%7Cdata%20analyst~SORT%7CListedDate~OSF%7Cquick&set=1768893675911/V%7C2~P%7Cjobsearch~K%7Cdata%20analyst~WH%7Craffles~WID%7C27663~OSF%7Cquick&set=1768893321485",
        "_legacy_auth0.Uwik845Sw4GL6U80RWmGnyfost3B9p94.is.authenticated": "true",
        "auth0.Uwik845Sw4GL6U80RWmGnyfost3B9p94.is.authenticated": "true",
        "utag_main": "v_id:019b9ca2531b001a1b4d1e9aaf3605077001906f00bd0$_sn:11$_se:287%3Bexp-session$_ss:0%3Bexp-session$_st:1768897118618%3Bexp-session$ses_id:1768891442966%3Bexp-session$_pn:7%3Bexp-session$dc_visit:6$dc_event:2%3Bexp-session$dc_region:ap-east-1%3Bexp-session$_prevpage:search%20results%3Bexp-1768898267734",
        "g_state": '{"i_l":0,"i_ll":1768895316566,"i_b":"TzVKP1VmEVs0e1ECxR9FQCjynnHFO+DTvs7+ZUJKr/c","i_e":{"enable_itp_optimization":0}}',
        "_ga_1DBRYWTEXT": "GS2.1.s1768891450$o13$g1$t1768895315$j60$l0$h0",
        "appSession.0": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaWF0IjoxNzY3ODU5NDY0LCJ1YXQiOjE3Njg4OTUzMTUsImV4cCI6MTc3NjY3MTMxNX0..imjku4u4Yzxk_dWO.9TVpj-hdgb4XtdmT3zXluLekJhwuN4MoMv-ctd4qdxYy7XEutfqJ8UUpNXX9yBF-TLhKq6ogTjTKiQ0AhQ6BgVG91EvnafNIZCld5NjiWjkIRlz_Zdbfg4rh6GK5l1gdW67ztBrUV8c8HXCe7yGQ3ARyxEXAc0aqDuNV3LE3Lmhc23eh1KwVQu-uFJJPe71yVaEWScOH3CLMLCtX1JBVT-ahCRtkSfkm6Q9qFfR5CypB3rxYDbx0ksQDQ0s-bYwVCJhtJBA1KP6ZCUErcLnOX_78PtpjPkyWqPxBpQ5BFWhKQkYNOWLoyHmfQIacChxgKaua5ROditdgRPfnl3h6X8O1Q6eXkGlKNENW3hcsVuLXWTKapGF8pBLxQLHzyqDx5ihIU7t43ASp_yWVFwl8gyojgCWhq5c2rE0WETV5KqzBLSfF8zXGWaP0TUGreMXMy_lfilqC3rPhkUa8aHU0Mm53cBw4ka-G-NP5zVLIktMp_rx70qOO9z86jIJYqi1XLfjqBvdWbMRC7fdZMgT42F6dqC9BU3EAlcffMFdFPdjPFYRvHLLe_gg78zFUU_W6hDqxkQrTHmnk0SEiqL_1LVEcPSxU2KQC3HMq0ySjW6jK--d_BVCttfDOB6U2G4g-tZp3k1R7L4MUPqFcJiv9HHSQeidgTTaQtDfX88t0IsNSPNqidlI57POvC2whtbvyNOHXe_eeIKDlVz8_Ez759oxvZdS39jXWsDW1jAhLnG3NuueGPPxMiFKFNLUeMEWTtxBKJvPv8R5CgcegBgyFksXDrllWv7ZFHXT_BAkuyBe_-PJEPm9m7K3aeQPliZ3BTX856GthGeL4NPJP2vB0AnmqBVLK3G746kih2sGzGkOfKhTvszAHSaAkL5A4FTxcHpS1nQ2x3ghYFjtRi9cGzAs1DD8TePT_G66kgoL-ObloZrzD-NVoO9vJCDa3zZ0SRc47GiZHKmc1wpYhFjDCXOxEk2mTu6U3xNMcY7sIyDvpk-F24zJH9c3ps5weUFGsn1TDCWrnmDxB3UAPnq_ux27fSMXrZOVDm2_zrIp_kuSlD74Ce3xPX6F6MA-ohzHIEeqmDSTimBjfv8G2A1coD6fAe8IQxkywhICXW6hVZ6JWpDtlWrUvU0na0GZu2lPgLTuWPZqs5oQkMyxEsLRESwHdtvoAzFJzYhGvmoXDstiSv2YVCBereViWmp9lEjvhkwbHO1skvXp_ALVjDaBG57gmf3KsBIi0mkSGum5sqQD-R2ubPfWFRNs0yseElV0KID5U_0Sm2xzCQrUq_akfY6hYoeuRdCPgDpJ4tY_7_klK4oolNccwJcTFkCIbZGx3pxMXTZ0VFRSkMIMv8Gn0IS_6l8Fu2bARhEDsDJBNBGMGlg2QjqkKuRPUsshNNpdDypzmxJ5X4H7O3Dylrw7EmLTotMyiuW6AomR6lZ1Zij1sosCw0XLR4o_aMjiOImta0NskjBa7Vzupw9Rm5lEga73EXDAnAS4Bq5ngFP4voHsAJReaLfpqm5jAkjkBhOSJUY1pveXjUviqIC78KRp6cDeH_IkENlonUxFwAgLnutGx1UXHYb_J6crhJJBk841b41GYC3UVXyHmjTJ7Ss6HXorBWrCXCJmSzBMfawEBOa01bNbN64OPo0vOrxj9lAv5AuSYTTWdEUKjww4l841Z_FpadsbbOnLHQpEg6ovbumte4ye1BAU8D05fv0dkzLnIRVDpfRBgJ-AWl6P3DbbibbgZj_7DOleRxAcJYaW-M3hDxXvCTcucTwYAiPY6hLY_ruDQsHmb_cxaxD6Gv64l0RrP7IZ7RveJK2P2sVdbrEv6qQRZob8UFEmUMx1KXxzsfov9If_Gki8kpuLRX5lgHjHgM9XQgx4UxHekqmnm0LT1EJrFz7jmkto2CJgKyVie7jpnnt5TV5OOM6j5fy2tNn9MqG5ViXo3v9mzPjt--c3kVATXaHXC-s3WdeN68ABcDY2pefu1ZLXXehwO3sCIUDNL6rold0U6Wi5x2CJNOHwGGKEa9kx1VlFxdSPEpe7VXgfTGu1MWYe_Ix0KFtRrUShOk8b6RFjh2ZBnwOKLXkQxkwzJlsYFPRZMEWJhLeh6ythAyf29pTmU6bbME7YNw6SIveJFmdc_KJvArPCDZVfAjrOYIk8PJgArhASvIz9Tnl5zO0eiNxk-eZ3yuCm9vTYCtdeJAJnODAVAfpjGdyTG_aZVJm7EOK8ounPViL-evTPBL5Q8qPfnNd8pxCEfddlkr5paTTt75OZZW4VFihNIbUYWOOyjxpMj7R7uj2JjJRMKEHnuk8Q0RQyRZkGe55m6O7lZBfqTym0jqoNZyxV41VcrZHxy4g_G0eblWpv6kfM3CuEYO3VU_tVI9yqT8dSzp9N8yp-RYktZhg857WF0tzJeLE4V0xTP6N9_a4QXENDcY1IRE-AyIriCgrxHQt-LofxAkLb5yWdnFLcpgvG90yyHsw3CiU0CGjn0LzZcZSNvqmBM_ZBOf2PzDfx4WBjLglN4PGD-cM2t2OP6wDexguE9vtYl5CL46gKgIcQTX6jQp3gUZFisAIY8B_n2nA53LbU1CWoHCmywIUspvmLFKLvTTdUwrn_J8zICCGvEYq1WqvySIXng-iMTnaOaX5dTYdm-S2Ko-8k682GlAuSR5XBR5lEeVDzLy9k93X94gI6ZWZZ3u34OXDnRXJSNfSD1eL_HENBddFRdYosJV5COR1Lo32uIIc4cnkv62jgvsyQDsXobRAeT2Od6Eg_1wsfQSkzoJm85uVfR4mCNAaaA-0OPm81QHhVBmjQR4EZgcWnI_IJgiLQ5JhxUOznw4hyWZGmmn_R9vFamXYNsdZgaxSIDlNof1Yr4l0Mc2E0fJpouyBf3J8PxIi6F_HbFsQ_1FH0uDiXioUbAzGKJdX--vyAJe5TcWDH6VOvSS6a4g5DPRZ-htG8JbU7q1HwKfRnqtsNrhCMFOezrfDz9VlZhFMQLB9ruxQWOO2gfRrRkjzgp0LmRJLI0JAZiHfXwrZqaO3Eag5jR2nn3tj5Nk3S8jUglbCNs1yKYuTIb6PBtsYtqS2l_NACYNFqqIzqLxlkAmO51xgPAiZD3f41b_1qwkMmgfzzj33ZXbwZNdXO6aaDpM2qaRKq9B2ncBljW1eQ0QyEs7nAYFz7FTRIcHYm3geYBk9_Go5C-P5GHmwSycJjm9jefW2vKqlUBNIupDluSGe_p-QPw_ejh4xyTi293uaMaRFJlZWlpxh-xYp2nGE8pyBMfMUPYmswJyFeNKVt2T_liQsHztbxvNTp5ozU9sDRUlI4pJpkk4FdMfG6BqWKh1bTjKv28LrUoT7IcJGcUSOsiTch-CFdinqM8Xno5ARDqa6nkePcg_WT_If2Sah_LmHayomxEFT6Vp4UU1wYsReTlJgxOT-MIYZN5mGpaffyU7DY_PMfw8vAWSne9kO2cDD87Fea7gz_bBDHChntFzzuLbYd1rkHeielLgqsfVSXlkbP7h_E1QT5u4WyaU66CSz2kU0QO3CCNjg8oELxMu8isdx3vDnfFv38sLqPgjgoOLK1VKPCCuEV4rv5_iBGR9jPu2OejRuM7uCY5zpzsEKS3irEN8e4UZz_P2swfZcOOgasOCo0FKb-V7Fsr1qZctnvSAfkVnsBhIeleZQM7a1HQMV39X3XCEN-S5R8BQ0fqEDQhp1rX1ElGS0WWCsewj27pLU-oqq1w1AUBzXDZfNiIN-Ug_vpERBLHqEX2S2H7_KRREsuhexrxpgoxkTIEWDyy6uUweeZQIdgW0KnrxhGnUe3MXySB1GJ4r3umiseBwO1QCPmB00LYvQwmxzYTkSILBFvJjHPLJOitb1SfEng0tlPF6aDGv5",
        "appSession.1": "Bky_CWCZ-h9JhBDwUX70EPeoeB62-aRyChxQ1I_EHTZwIrPGF_ZUIz6w6KhAbzAPo-MBuU_vwdJdTaHbOykjuPhV3f2WiRdQ7qZf3O54ca6Fe9GTrCyrhxg33x25q8FvO5J3DpjvMfepM82y9__vT2pyqkrRdVqarvF5AScPswtQff22dNcWlF6ChNmxWMBB_S1zvlKgl_BHfB3D2VyQtd1p8Bebm0F84RbEwD2mnlLa-R7tfiyOi67abfv49NtMbqKyw_m9gjhYti-QNOjVTqdeDkErs1jsCT8NI22giyLzG-M72HJ3fh-0JS0vv-Ct0GhcrUYtP0fvrD7-8wG7nNp0yfCo8Dn-m-w9Y83_h9Mbbp3QUGE7xgKWkjJNERSVXClgYBqo4bhXLn09unF_H_Bdr0p_u7Kt0AO7fCCh2TtxRD02zmbZ_75zQgUv-MkI8IZLw4H4O7wrFNFN5SoLEXeer7OFyFT-N64A6Hrg45VeV7JXP2RL0ent9FjYbh98cfnrbatKInBfT60BhmwBozI5UufwUG0gY3ahlUDQhEFTbyMncGnOLltOKyNwHZWauCaDLxEkob3KOvPPjTyiACB1FxgRbm1kGUv1uW48HCW1XLaJtOPQzScixmtkwC2h3FBk301Ju6_G8-lZ1sIe9-rRooDs-3iRCiFsC112Upl3wAWCEGgrTvVJa_MhgmaEPXVLrNthFJO81dNQpCx_v0_IZ2kNrl6NnI7iMDW3hvV8d2IQr4sadOBwvmRW7uWBSZvhGASSXrZXpyCP7MlRdTruVmBO4NiWA84GvYH14sgJx10w3hErgLKe-2vWNbruTmnLqmynJf4BssvYRHl2wSLMisZKZbrRsT3pKrcJiSSK2CPF78fHxOdu3QLI1Xg9N-5UqpK6Q8XXDJl264dgOCkV0CxCdxS5bapcsDZxklXblcC_QGmveaZr0fId2XQfaaEOwIXJ__SlTikg3PjLeFzS9n1PdI0gaLZljz-rhBQQHw_XdYOLiDGhTjN6pZ3uVcuLZNQDSm7mOHcZFYoXuuhGwF-7H5AJRmhhf7UDk3ZGwtEZS7AEcy04JnROvuiq1LLqPCBy-d_GpHGDi4H1fmqyG6QV7-wWrx8RjGQzbnhYKtME8VsZmoD443gWzPQqPeB3IlZ0yFunszq-c2GP2YgRhiXMC3aRXs5K6KoyjZBrmjoQBJlQ7VdK0qkK-U_CuczFaTmgqkLaRn_rC5MNzDmp-sY3VWfPp7pFsFoah6KXjcrHif1ZS1mNL-aQj1aobwzijxWNPhPw9IBMeWCZ2xAZL_NBFmqLOGdTar7rVhVa8zXXqxGb7Rh64vXbc-igKuXrOWjba97e2kqfwXArM4fArv3nhrpOiWcZ6ckqCw_1m8G3ZCo8-DjbvVMn9JR8fhq79MRQt0P6XORfXII9e5lFMRmbZ5aUsiVGzZXWFkW2yKd5iuCK911j2BR32JQywA9UkbMW1q9OSnm5bxK0b0DPpcN2OuszwljaaHQ0FujHWeHA3YU7S4VGpkmK6gg9S2tC73oaqGQccqnKTa_td2fyuUrOSrJVcJkXvKSMrMQ_FaQQWuMv-cf2eAB2_WMDLwTqTSXo03J4lN3Yhn_QEb6X_IG-kKctQXJOHfN5Etn0bYPw2SaYg2eCEfXTt5F4e4SaaDkQaARHvP04jFK4ocexbk3xOaDcaAuVU3Xg9tnUQISqNUAgw3Ia-vjYZUYHvQNp8W4vvAIZx_rLp8mSXh4-0ocqG1XSwM.G8nbQ-JssyF4oX4RW_PmkA",
        "_fbp": "fb.1.1767859442980.78964802847699957",
        "_gcl_au": "1.1.1273980953.1767859443.1470394543.1768891476.1768891476",
        "ajs_anonymous_id": "608c650c036783bcbe92fb330d5d0176",
        "_ga": "GA1.1.710606285.1767859443",
        "ttcsid": "1768891447970::oHYiucmr7csoy2wr4PVU.11.1768894671440.0",
        "ttcsid_CKOI0DJC77U3K90HBTG0": "1768891447970::eEEJxyuAw4NWhc_vc3Xy.11.1768894671441.1",
        "_tt_enable_cookie": "1",
        "_ttp": "01KEEA4NSH5FFH1H7SHZ6ZCV8Z_.tt.1",
        "_hjSessionUser_640495": "eyJpZCI6ImM2MDNhNTNjLTQ1ZGEtNWFlOC1iYTQ5LWM1MWQ2MjA1YTk1ZiIsImNyZWF0ZWQiOjE3Njc4NTk0NDMyODMsImV4aXN0aW5nIjp0cnVlfQ==",
        "_hjHasCachedUserAttributes": "true",
        "_uetsid": "a4a5f800f52611f0a1cfb32b49b863ce",
        "_uetvid": "98ce0f00ec6811f0b576811f1e3a5ffd",
        "da_sa_candi_sid": "1768891442966",
        "da_searchTerm": "undefined",
        "da_userProfile": '{"latestNonLinkedOutJobApplicationDate":1768826096316}',
        "_hjSession_640495": "eyJpZCI6IjI1YjAxMzg3LTRhMTUtNGNmMS1hN2ZkLTdmMzI3ZDk1MGRkMiIsImMiOjE3Njg4OTE0NDc5MDQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=",
        "__eoi": "ID=e695559c66a62700:T=1768820928:RT=1768893724:S=AA-AfjZAvFCn1RCyu5npqI0JKtj3",
        "__gads": "ID=e47ff5ea974709f2:T=1768820928:RT=1768893724:S=ALNI_MZCaklA_BnFzQsVUiXqvpXx2iT_CA",
        "__gpi": "UID=000011e7b22117b4:T=1768820928:RT=1768893724:S=ALNI_MbjtJSXu8fZ-3uFA6pvzPfDzZb77A",
        "_cfuvid": "pQ5EEeYkQMT0pgVf0MyoUkxxDEqLbJaJHQYjQPwceO8-1768893182265-0.0.1.1-604800000",
        "_clck": "117rzpz%5E2%5Eg2v%5E0%5E2199",
        "_hjMinimizedPolls": "1829968",
        "registeredCandidateId": "591832689",
        "last-known-sol-user-id": "66dca3cc6ee372790f3369c903365d98159b122237f848593eb42ad0ff49b9f25c3ad303b5d8e043a7945a7a6f19a3e2346e80f577405a7c84f7108c685ff491baebc3ea478beea34adbe5f858b37195c06ba3ff268cd2b0a8ff1003ddda55cdb16a6284ceed7cd6761409e237f456e609d8ecb8e122046e6d592ec3fd60b83e672c87d56eda88c85478b27ad6cbf41ffe72e37a64056ca3d4f1fe4ffbc6d9917d5b503862ca70623e894ee92ef2171845813bfe99fd",
        "da_page_engaged": "true"
        }
        self.headers = {
            "Host": "sg.jobstreet.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Referer": "https://sg.jobstreet.com/",
            "Connection": "keep-alive",
        }
        # self.base_url = 'https://www.jjwxc.net/bookbase.php'
        self.f = open('novel-1.csv', 'w', encoding='utf-8-sig', newline='')
        self.writer = csv.DictWriter(self.f, fieldnames=['作者', '名称', '类型', '进度', '字数', '发表时间', '作品视角',
                                                         '所属系列', '版权转化','签约状态','非v章节章均点击数','总书评数',
                                                         '当前被收藏数','文章积分','内容标签','评分','评价人数',
                                                         '五星比例','四星比例','三星比例','二星比例','一星比例'])
        self.writer.writeheader()
        self.count = 0

        # 初始化 Selenium WebDriver
        self.driver = None
        self.init_driver()
    
    # def init_driver(self):
    #     """初始化 Chrome 驱动"""
    #     try:
    #         options = webdriver.ChromeOptions()
    #         options.add_argument('--headless')  # 无头模式
    #         options.add_argument('--disable-gpu')
    #         options.add_argument('--no-sandbox')
    #         options.add_argument('--disable-dev-shm-usage')
    #         # 防止检测
    #         options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #         options.add_experimental_option('useAutomationExtension', False)
    #
    #         self.driver = webdriver.Chrome(options=options)
    #         self.driver.set_page_load_timeout(30)  # 设置页面加载超时
    #         print("✅ Chrome 驱动初始化成功")
    #     except Exception as e:
    #         print(f"❌ Chrome 驱动初始化失败: {e}")
    #         raise
    #
    # def check_driver_alive(self):
    #     """检查 driver 是否还活着"""
    #     try:
    #         _ = self.driver.current_url
    #         return True
    #     except:
    #         return False
    def send_requests(self, page_num):
        """
        使用 DrissionPage 获取网页内容，绕过 Cloudflare 验证
        """
        # 1. 初始化页面对象（如果你的类里已经有了 self.page，可以直接使用）
        # 建议加上 listen 模式，虽然直接 get 也可以，但 listen 可以捕获接口数据
        dp_page = ChromiumPage()

        # 2. 构造带分页的 URL
        url = f'https://sg.jobstreet.com/data-jobs?page={page_num}'

        try:
            print(f"正在抓取第 {page_num} 页: {url}")

            # 3. 访问网页
            dp_page.get(url)

            # 4. 等待关键元素加载（比如职位列表的 div），确保 Cloudflare 验证已完成
            # 这里的 .p8fjkv0 是你之前提到的职位卡片类名
            if dp_page.wait.ele_displayed('.p8fjkv0', timeout=10):
                # 5. 返回渲染后的 HTML 文本
                return dp_page.html
            else:
                print("等待页面元素超时，可能被拦截或页面加载缓慢")
                return None

        except Exception as e:
            print(f"DrissionPage 请求发生错误: {e}")
            return None
        # 注意：如果你不想每次请求都开/关浏览器，建议将 ChromiumPage() 放在 __init__ 中
    # def send_requests(self, page):
    #     params = {
    #         'page': f'{page}',
    #     }
    #     try:
    #         response = requests.get('https://sg.jobstreet.com/data-jobs', params=params, cookies=self.cookies, headers=self.headers, timeout=10)
    #         response.encoding = 'uft-8'
    #         response.raise_for_status()  # 检查HTTP错误
    #         return response.text
    #     except requests.exceptions.RequestException as e:
    #         print(f"请求失败: {e}")
    #         return None

    def parse_html(self, response, page):
        if not response:
            print("响应为空，跳过解析")
            return

        tree = etree.HTML(response)
        div_list = tree.xpath('//div[@class="p8fjkv0 _12h6b4o59 _12h6b4ohh _12h6b4o6p"]')
        for div in div_list[1:]:
            try:
                author = div.xpath('./td[1]/a/text()')[0].strip()  # 作者
                title = div.xpath('./td[2]/a/text()')[0].strip()  # 小说名称
                novel_type = div.xpath('./td[3]/text()')[0].strip()  # 小说类型
                speed = div.xpath('./td[4]/font/text()')[0].strip()  # 进度
                wordcount = div.xpath('./td[5]/text()')[0].strip()  # 字数
                publish_time = str(div.xpath('./td[7]/text()'))  # 发表时间
                novel_url = 'https://www.jjwxc.net/' + div.xpath('./td[2]/a/@href')[0].strip()
                novel_id = novel_url.split('=')[1]
                # 解析详情页并得到扩展字段（包含 版权转化 字段）
                zuopinshijiao, suoshuxilie, banquanzhuanhua, qianyuezhuangtai, totalclick, reviewCount, collectedCount, scoreCount, neirongbiaoqian, pingfen, yipingfenrenshu, wuxing_baifenbi, sixing_baifenbi, sanxing_baifenbi, erxing_baifenbi, yixing_baifenbi = self.send_detail_request2(
                    novel_id, page)
                dic = {
                    '作者': author,
                    '名称': title,
                    '类型': novel_type,
                    '进度': speed,
                    '字数': wordcount,
                    '发表时间': publish_time,
                    '作品视角': zuopinshijiao,
                    '所属系列': suoshuxilie,
                    '版权转化': banquanzhuanhua,
                    '签约状态': qianyuezhuangtai,
                    '非v章节章均点击数': totalclick,
                    '总书评数': reviewCount,
                    '当前被收藏数': collectedCount,
                    # '营养液数': nutritionCount,
                    '文章积分': scoreCount,
                    '内容标签': neirongbiaoqian,
                    '评分': pingfen,
                    '评价人数': yipingfenrenshu,
                    '五星比例': wuxing_baifenbi,
                    '四星比例': sixing_baifenbi,
                    '三星比例': sanxing_baifenbi,
                    '二星比例': erxing_baifenbi,
                    '一星比例': yixing_baifenbi,
                }
                print(author, title)
                self.writer.writerow(dic)
                self.f.flush() 
            except Exception as e:
                print(e)

    def _init_driver(self):
        """初始化 Chrome WebDriver（无头模式）"""
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument(f"user-agent={self.headers['User-Agent']}")
        
        # 添加 cookies（可选，如果需要登录状态）
        driver = webdriver.Chrome(options=opts)
        driver.get('https://www.jjwxc.net/onebook.php?novelid=1')  # 先访问任何页面以设置 cookies
        for key, val in self.cookies.items():
            try:
                driver.add_cookie({'name': key, 'value': val})
            except Exception as e:
                print(f"添加 cookie {key} 失败: {e}")
        
        return driver

    def send_detail_request2(self, novel_id, page):
        """通过 Selenium 获取渲染后的 HTML"""
        url = f'https://www.jjwxc.net/onebook.php?novelid={novel_id}'
        
        print(f'正在通过 Selenium 爬取第{page}页第{self.count+1}条数据... (novelid={novel_id})')
        self.count += 1
        max_retries = 1
        for attempt in range(max_retries):
            try:
                # 检查 driver 是否还活着，如果不活着就重新初始化
                if not self.check_driver_alive():
                    print("⚠️  检测到 driver 会话失效，正在重新初始化...")
                    if self.driver:
                        try:
                            self.driver.quit()
                        except:
                            pass
                    self.init_driver()
                
                self.driver.get(url)
                
                # # 等待关键元素加载
                # WebDriverWait(self.driver, 10).until(
                #     EC.presence_of_element_located((By.ID, "novelreview_div"))
                # )
                
                time.sleep(1)
                
                html = self.driver.page_source
                tree_detail = etree.HTML(html)
                
                
                # 作品视角
                try:
                    zuopinshijiao = tree_detail.xpath('//ul[@name="printright"]/li[2]/text()')[1].strip() if tree_detail.xpath('//ul[@name="printright"]/li[2]/text()') else "未知"
                except:
                    zuopinshijiao = "未知"
                # 所属系列  
                try:
                    suoshuxilie = tree_detail.xpath('//ul[@name="printright"]/li[3]/span[2]/text()')[0].strip() if tree_detail.xpath('//ul[@name="printright"]/li[3]/span[2]/text()') else "无"
                except:
                    suoshuxilie = "无"

                # 版权转化
                # 提取"版权转化"一项中所有 img 的 title 属性，拼接为逗号分隔字符串
                try:
                    # 优先按包含"版权转化"文字的 li 节点查找
                    titles = tree_detail.xpath('//ul[@name="printright"]/li[contains(normalize-space(.),"版权转化")]//img/@title')
                    # 若没有找到，则退而求其次，查找该 ul 下所有带 title 的 img
                    if not titles:
                        titles = tree_detail.xpath('//ul[@name="printright"]//img[@title]/@title')
                    # 过滤空值并去重（保持出现顺序）
                    seen = set()
                    cleaned = []
                    for t in titles:
                        if not t:
                            continue
                        s = t.strip()
                        if s and s not in seen:
                            seen.add(s)
                            cleaned.append(s)
                    banquanzhuanhua = ",".join(cleaned) if cleaned else "未签约"
                except Exception:
                    banquanzhuanhua = "无匹配结果"
                    
                # 签约状态
                try:
                    # 找到“签约状态”所在的 li
                    li_node = tree_detail.xpath('//ul[@name="printright"]/li[contains(string(),"签约状态")]')

                    if li_node:
                        text = "".join(li_node[0].xpath('.//text()')).strip()

                        if "未签约" in text:
                            qianyuezhuangtai = "未签约"
                        else:
                            # 只要不是“未签约”，就是已签约（排除影视签约等属于版权转化）
                            qianyuezhuangtai = "已签约"
                    else:
                        qianyuezhuangtai = "未签约"

                except:
                    qianyuezhuangtai = "未签约"

                # 新增：提取"内容标签"
                try:
                    tag_nodes = tree_detail.xpath('//div[@class="smallreadbody"][contains(., "内容标签")]//span/a/text()')
                    cleaned_tags = []
                    seen = set()
                    for tag in tag_nodes:
                        if tag and tag.strip():
                            t = tag.strip()
                            if t not in seen:
                                seen.add(t)
                                cleaned_tags.append(t)
                    neirongbiaoqian = ",".join(cleaned_tags) if cleaned_tags else "无"
                except Exception as e:
                    print(f"内容标签提取失败: {e}")
                    neirongbiaoqian = "无"
                
                # 新增：提取"完结评分"相关数据
                try:
                    # 评分
                    pingfen_nodes = tree_detail.xpath('//div[@id="novelreview_div"]//div[contains(text(),"评分：")]/span[@class="coltext"]/text()')
                    pingfen = pingfen_nodes[0].strip() if pingfen_nodes else "0"
                    
                    # 已评分人数
                    yipingfenrenshu_nodes = tree_detail.xpath('//div[@id="novelreview_div"]//div[contains(text(),"已评分人数：")]/span[@class="coltext"]/text()')
                    yipingfenrenshu = yipingfenrenshu_nodes[0].strip() if yipingfenrenshu_nodes else "0"
                    
                    # 5星百分比
                    wuxing_nodes = tree_detail.xpath('//div[@class="novelreview_chart_col"][@data-score="5"]//div[@class="col_item"]/following-sibling::div/text()')
                    wuxing_baifenbi = wuxing_nodes[0].strip() if wuxing_nodes else "0%"
                    
                    # 4星百分比
                    sixing_nodes = tree_detail.xpath('//div[@class="novelreview_chart_col"][@data-score="4"]//div[@class="col_item"]/following-sibling::div/text()')
                    sixing_baifenbi = sixing_nodes[0].strip() if sixing_nodes else "0%"
                    
                    # 3星百分比
                    sanxing_nodes = tree_detail.xpath('//div[@class="novelreview_chart_col"][@data-score="3"]//div[@class="col_item"]/following-sibling::div/text()')
                    sanxing_baifenbi = sanxing_nodes[0].strip() if sanxing_nodes else "0%"
                    
                    # 2星百分比
                    erxing_nodes = tree_detail.xpath('//div[@class="novelreview_chart_col"][@data-score="2"]//div[@class="col_item"]/following-sibling::div/text()')
                    erxing_baifenbi = erxing_nodes[0].strip() if erxing_nodes else "0%"
                    
                    # 1星百分比
                    yixing_nodes = tree_detail.xpath('//div[@class="novelreview_chart_col"][@data-score="1"]//div[@class="col_item"]/following-sibling::div/text()')
                    yixing_baifenbi = yixing_nodes[0].strip() if yixing_nodes else "0%"
                    
                except Exception as e:
                    print(f"完结评分提取失败: {e}")
                    pingfen = "0"
                    yipingfenrenshu = "0"
                    wuxing_baifenbi = "0%"
                    sixing_baifenbi = "0%"
                    sanxing_baifenbi = "0%"
                    erxing_baifenbi = "0%"
                    yixing_baifenbi = "0%"
                
                # 从第二个 table 最后一行的 sptd 中提取五个数据：总书评数、被收藏数、营养液数、文章积分、非v章节章均点击数
                try:
                    # 非v章节章均点击数
                    totalclick = tree_detail.xpath('//table[2]/tbody/tr[last()]/td[@class="sptd"]/div/span[1]/text()')[0] if tree_detail.xpath('//table[2]/tbody/tr[last()]/td[@class="sptd"]/div/span[1]/text()') else "0"
                except:
                    totalclick = "0"
                    
                try:
                    # 总书评数
                    reviewCount = tree_detail.xpath('//span[@itemprop="reviewCount"]/text()')[0].strip() if tree_detail.xpath('//span[@itemprop="reviewCount"]/text()') else "0"
                except:
                    reviewCount = "0"
                    
                try:
                    # 当前被收藏数
                    collectedCount = tree_detail.xpath('//span[@itemprop="collectedCount"]/text()')[0].strip() if tree_detail.xpath('//span[@itemprop="collectedCount"]/text()') else "0"
                except:
                    collectedCount = "0"
                    
                # try:
                #     # 营养液数
                #     nutritionCount = tree_detail.xpath('//span[@itemprop="nutritionCount"]/text()')[0].strip() if tree_detail.xpath('//span[@itemprop="nutritionCount"]/text()') else "0"
                # except:
                #     nutritionCount = "0"
                
                try:
                    # 文章积分
                    scoreCount = tree_detail.xpath('//span[@itemprop="scoreCount"]/text()')[0].strip() if tree_detail.xpath('//span[@itemprop="scoreCount"]/text()') else "0"
                except:
                    scoreCount = "0"

                # 返回值中新增字段
                return zuopinshijiao, suoshuxilie, banquanzhuanhua, qianyuezhuangtai, totalclick, reviewCount, collectedCount, scoreCount, neirongbiaoqian, pingfen, yipingfenrenshu, wuxing_baifenbi, sixing_baifenbi, sanxing_baifenbi, erxing_baifenbi, yixing_baifenbi
            
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  第 {attempt+1} 次尝试失败，正在重试... 错误: {e}")
                    time.sleep(2)
                else:
                    print(f"❌ 详情页请求失败 (novelid={novel_id}): {e}")
                    return "未知", "无", "未签约", "未知", "0", "0", "0", "0", "0", "无", "0", "0", "0%", "0%", "0%", "0%", "0%"

    def save_data(self):
        pass

    def close(self):
        """关闭 WebDriver"""
        if self.driver:
            self.driver.quit()

    def run(self):
        try:
            for i in range(1, 173):  # 爬取前172页数据
                print(f'正在爬取第{i}页数据...')
                response = self.send_requests(i)
                self.parse_html(response, i)
        finally:
            # 确保文件被正确关闭
            if hasattr(self, 'f')and self.f:
                self.f.flush()  # 最后再 flush 一次
                self.f.close()
                print("文件已关闭")


if __name__ == '__main__':
    JJ = JinJiangSpider()
    JJ.run()