import requests
from bs4 import BeautifulSoup
from spider.ershoufangModel import Xiaoqu,Ershoufang,Chengjiao
import time
class WBSpider(object):
    def __init__(self):
        self.headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
        self.datas = list()


    def getMaxPage(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            pageData = soup.find("div", class_="pager")
            pages = pageData.find_all("a", class_="goPage")
            maxPage = pages[len(pages)-1].find("span").text
            return maxPage

    def getPageParse(self, url):
        # maxPage = self.getMaxPage(url)
        maxPage = 2
        if maxPage != None:
            for page in range(1,25):
                url = "https://zhoushan.58.com/xiaoqu/pn_{}".format(page)
                response = requests.get(url, headers=self.headers)
                print("开始拉取第 {} 页", page)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    links = soup.find_all("div", class_="list-info")
                    for i in links:
                        time.sleep(3)
                        link = i.find("a")["href"]
                        detail = self.parseDetail(link)
                        xiaoqu = Xiaoqu(address=detail.get("地址"), building="楼栋总数", city="舟山",
                                        city_code=330901, company="开发商", name=detail.get("小区名称"),
                                        number=detail.get("房屋总数"), price=detail.get("均价"),
                                        property_company="物业公司", property_fee="物业费用",
                                        source="58同城", type=detail.get("建筑类型"))
                        xiaoqu.save()

    def parseDetail(self, link):
        response = requests.get(link, headers=self.headers)
        detail = {}
        try :
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                detail["小区名称"] = soup.find("div", class_="title-bar").find("span", class_="title").text
                detail["均价"] = soup.find("div", "price-container").find("span", class_="price").text
                infos = soup.find("div", class_="info-tb-container").find_all("tr")
                detail["地址"] = infos[0].find_all("td")[3].text
                detail["房屋总数"] = infos[1].find_all("td")[3].text
                detail["建筑类型"] = infos[4].find_all("td")[1].text
                return detail
        except Exception:
            print(link)

if __name__ == "__main__":
    print("开始拉取舟山小区信息------")
    WBSpider = WBSpider();
    WBSpider.getPageParse("https://zhoushan.58.com/xiaoqu/")
