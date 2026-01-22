import random
import re
import time

import requests
import csv
from lxml import etree
import datetime
from DrissionPage import ChromiumPage, ChromiumOptions
import traceback

class JobStreetSpider():
    def __init__(self):

        # 定义要写入的字段
        self.f = open('jobstreet_jobs.csv', 'w', encoding='utf-8-sig', newline='')
        # 使用 location1/2/3 分列，最多三个位置字段
        self.writer = csv.DictWriter(self.f, fieldnames=['详情页链接','岗位名称','公司名称','location1','location2','location3','薪水范围',
                                                         '工作性质','职位分类','公司行业','公司规模','公司所在地'])
        self.writer.writeheader()
        self.driver = None



    def send_requests(self, page_num):
        # 创建Chrome浏览器对象并返回 (dp_page, html)
        co = ChromiumOptions()
        #以无头模型运行
        # co.headless(True)
        #
        # 额外优化：禁用 GPU 加速和图片加载（可以让后台运行更快、更省内存）
        # co.set_argument('--disable-gpu')
        # co.set_argument('--blink-settings=imagesEnabled=false')
        # dp_page = None
        # html = None

        url = f'https://sg.jobstreet.com/data-jobs?page={page_num}'

        try:
            print(f"[DEBUG] 创建 ChromiumPage，page={page_num}")
            dp_page = ChromiumPage(co)

            print(f"正在抓取第 {page_num} 页: {url}")

            dp_page.get(url)

            try:
                if hasattr(dp_page, 'wait') and dp_page.wait:
                    try:
                        ok = dp_page.wait.ele_displayed('.p8fjkv0', timeout=10)
                    except Exception as e_wait:
                        print(f"[DEBUG] wait.ele_displayed 抛出异常: {e_wait}")
                        ok = False
                    if ok:
                        html = getattr(dp_page, 'html', None)
                        print(f"[DEBUG] 等待到目标元素，HTML 长度: {len(html) if html else 0}")
                    else:
                        print("等待页面元素超时或等待器不可用，返回完整渲染后的HTML（如果有）")
                        html = getattr(dp_page, 'html', None)
                        print(f"[DEBUG] 直接获取 HTML 长度: {len(html) if html else 0}")
                else:
                    print("[DEBUG] dp_page.wait 不可用，直接读取 html")
                    html = getattr(dp_page, 'html', None)
                    print(f"[DEBUG] HTML 长度: {len(html) if html else 0}")
            except Exception as e:
                print(f"等待或获取 HTML 时出现错误: {e}")
                traceback.print_exc()
                html = getattr(dp_page, 'html', None)
                print(f"[DEBUG] 异常后尝试获取 HTML 长度: {len(html) if html else 0}")

            return dp_page, html

        except Exception as e:
            print(f"DrissionPage 请求发生错误: {e}")
            traceback.print_exc()
            try:
                html = getattr(dp_page, 'html', None)
                print(f"[DEBUG] 异常后取 HTML 长度: {len(html) if html else 0}")
            except Exception:
                pass
            return dp_page, html

    def send_detail_request(self, link, title):
        """通过 Selenium 获取渲染后的 HTML"""
        url_detail = f'https://sg.jobstreet.com{link}'

        print(f'正在爬取{title}公司详情页: {url_detail})')

        co = ChromiumOptions()

        try:
            dp_page = ChromiumPage(co)

            dp_page.get(url_detail)

            try:
                if hasattr(dp_page, 'wait') and dp_page.wait:
                    try:
                        ok = dp_page.wait.ele_displayed('.p8fjkv0', timeout=10)
                    except Exception as e_wait:
                        print(f"[DEBUG] wait.ele_displayed 抛出异常: {e_wait}")
                        ok = False
                    if ok:
                        html = getattr(dp_page, 'html', None)
                        print(f"[DEBUG] 等待到目标元素，HTML 长度: {len(html) if html else 0}")
                    else:
                        print("等待页面元素超时或等待器不可用，返回完整渲染后的HTML（如果有）")
                        html = getattr(dp_page, 'html', None)
                        print(f"[DEBUG] 直接获取 HTML 长度: {len(html) if html else 0}")
                else:
                    print("[DEBUG] dp_page.wait 不可用，直接读取 html")
                    html = getattr(dp_page, 'html', None)
                    print(f"[DEBUG] HTML 长度: {len(html) if html else 0}")
            except Exception as e:
                print(f"等待或获取 HTML 时出现错误: {e}")
                traceback.print_exc()
                html = getattr(dp_page, 'html', None)
                print(f"[DEBUG] 异常后尝试获取 HTML 长度: {len(html) if html else 0}")

            return dp_page, html
        except Exception as e:
            print(f"DrissionPage 请求发生错误: {e}")
            traceback.print_exc()
            try:
                html = getattr(dp_page, 'html', None)
                print(f"[DEBUG] 异常后取 HTML 长度: {len(html) if html else 0}")
            except Exception:
                pass
            return dp_page, html

    def parse_html(self, html, page_num=None):
        if not html:
            print(f"第{page_num}页无内容，跳过")
            return

        try:
            tree = etree.HTML(html)
        except Exception as e:
            print(f"解析 HTML 失败: {e}")
            return

        job_nodes = tree.xpath('//*[@id="app"]/div/div[8]/div/section/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div')

        results = []
        if job_nodes:
            for node in job_nodes:
                # 1. 精准匹配职位名称所在的 <a> 标签
                raw_link = node.xpath('.//a[@data-automation="jobTitle"]/@href')
                link = raw_link[0].strip() if raw_link else ''

                raw_title = node.xpath('.//a[@data-automation="jobTitle"]//text()')
                title = ' '.join([t.strip() for t in raw_title if t.strip()]) if raw_title else ''

                raw_company = node.xpath('.//a[@data-automation="jobCompany"]//text()')
                company = ' '.join([t.strip() for t in raw_company if t.strip()]) if raw_company else ''

                raw_location = node.xpath('.//a[@data-automation="jobLocation"]//text()')
                # split location texts on common separators and flatten
                loc_parts = []
                if raw_location:
                    for part in raw_location:
                        if not part:
                            continue
                        # split on bullets, slashes, pipes, commas, dashes
                        pieces = re.split(r'[\u2022\u00B7·•/|,;\-–—]+', part)
                        for p in pieces:
                            s = p.strip()
                            if s:
                                loc_parts.append(s)
                # dedupe while preserving order
                seen = set(); clean_locs = []
                for l in loc_parts:
                    if l not in seen:
                        seen.add(l)
                        clean_locs.append(l)
                # ensure exactly up to 3 location fields
                location1 = clean_locs[0] if len(clean_locs) > 0 else ''
                location2 = clean_locs[1] if len(clean_locs) > 1 else ''
                location3 = clean_locs[2] if len(clean_locs) > 2 else ''

                raw_salary = node.xpath('.//span[@data-automation="jobSalary"]//text()')
                salary = ' '.join([t.strip() for t in raw_salary if t.strip()]) if raw_salary else ''

                # 访问详情页获取更多信息
                dp_detail_page, detail_html = self.send_detail_request(link, title)
                type, classification, company_link = self.parse_detail_html(detail_html, title)

                #如果jobstreet上有公司详情页，就进去爬取公司相关数据
                if company_link:
                    dp_company_page, company_html = self.send_detail_request(company_link, company)
                    company_industry, company_size, company_location = self.parse_company_html(dp_company_page, company_html, title)
                    if dp_company_page is not None:
                        try:
                            if hasattr(dp_company_page, 'quit') and callable(dp_company_page.quit):
                                dp_company_page.quit()
                        except Exception:
                            pass
                        try:
                            if hasattr(dp_company_page, 'close') and callable(dp_company_page.close):
                                dp_company_page.close()
                        except Exception:
                            pass
                dic = {
                    '详情页链接': link,
                    '岗位名称': title,
                    # '职位要求': JD,
                    '公司名称': company,
                    'location1': location1,
                    'location2': location2,
                    'location3': location3,
                    '薪水范围': salary,
                    '工作性质':type,
                    '职位分类':classification,
                    '公司行业': company_industry,
                    '公司规模': company_size,
                    '公司所在地': company_location,
                }
                # print(author, title)
                self.writer.writerow(dic)
                self.f.flush()

    def parse_detail_html(self, html, title):
        if not html:
            print(f"{title} 详情页无内容，跳过")
            return

        try:
            tree = etree.HTML(html)
        except Exception as e:
            print(f"解析 {title} 详情页 HTML 失败: {e}")
            return

        raw_type = tree.xpath('.//span[@data-automation="job-detail-work-type"]//text()')
        type = ' '.join([t.strip() for t in raw_type if t.strip()]) if raw_type else ''

        raw_classification = tree.xpath('.//span[@data-automation="job-detail-classifications"]//text()')
        classification = ' '.join([t.strip() for t in raw_classification if t.strip()]) if raw_type else ''

        raw_company_link = tree.xpath('.//a[@data-automation="company-profile-profile-link"]/@href')
        company_link = raw_company_link[0].strip() if raw_company_link else ''

        return type, classification, company_link

    def parse_company_html(self, dp, html, title):
        if not html:
            print(f"{title} 详情页无内容，跳过")
            return

        try:
            tree = etree.HTML(html)
        except Exception as e:
            print(f"解析 {title} 详情页 HTML 失败: {e}")
            return
        container = dp.ele('css:div._4vzyf10.qnfgt659.qnfgt6hh.qnfgt671.qnfgt66y')

        if container:
            # 2. 在这个容器内找所有的 span
            all_infos = container.eles('t:span')
            industry = all_infos[1]
            size = all_infos[2]
            location = all_infos[3]
        else:
            print("未找到指定的 div 容器")

        return industry, size, location



        # raw_company_industry = tree.xpath('.//span[@data-automation="job-detail-work-type"]//text()')
        # company_industry = raw_company_industry[0].strip() if raw_company_industry else ''
        #
        # raw_company_size = tree.xpath('.//span[@data-automation="job-detail-classifications"]//text()')
        # company_size = raw_company_size[0].strip()  if raw_company_size else ''
        #
        # raw_company_location = tree.xpath('.//a[@data-automation="company-profile-profile-link"]/@href')
        # company_location = raw_company_location[0].strip() if raw_company_location else ''
        #
        # raw_company_rate = tree.xpath('.//a[@data-automation="company-profile-profile-link"]/@href')
        # company_rate = raw_company_rate[0].strip() if raw_company_rate else ''


    def save_data(self):
        pass

    def close(self):

        try:
            if getattr(self, 'driver', None):
                try:
                    self.driver.quit()
                except Exception:
                    pass
        except Exception:
            pass

        # close file handle if present
        try:
            if getattr(self, 'f', None):
                try:
                    self.f.flush()
                except Exception:
                    pass
                try:
                    self.f.close()
                except Exception:
                    pass
        except Exception:
            pass

    def run(self):
        try:
            for i in range(1, 2):  # 爬取前1页数据
                print(f'正在爬取第{i}页数据...')
                dp_page, response = self.send_requests(i)
                if response is None:
                    print(f"第{i}页返回 None，跳过解析")
                    # 关闭 dp_page since we won't parse it
                    if dp_page is not None:
                        try:
                            if hasattr(dp_page, 'quit') and callable(dp_page.quit):
                                dp_page.quit()
                        except Exception:
                            pass
                        try:
                            if hasattr(dp_page, 'close') and callable(dp_page.close):
                                dp_page.close()
                        except Exception:
                            pass
                    continue
                else:
                    # parse first, then close the browser page
                    self.parse_html(response, i)
                    if dp_page is not None:
                        try:
                            if hasattr(dp_page, 'quit') and callable(dp_page.quit):
                                dp_page.quit()
                        except Exception:
                            pass
                        try:
                            if hasattr(dp_page, 'close') and callable(dp_page.close):
                                dp_page.close()
                        except Exception:
                            pass
        finally:
            # 确保文件被正确关闭
            if hasattr(self, 'f') and self.f:
                self.f.flush()  # 最后再 flush 一次
                self.f.close()
                print("文件已关闭")

if __name__ == '__main__':
    JJ = JobStreetSpider()
    JJ.run()
