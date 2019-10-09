import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
# from model import build
# from model.build import Build
from spider.ershoufangModel import Xiaoqu,Ershoufang,Chengjiao


class LianjiaESpider(object):
    def __init__(self):
        self.headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
        self.datas = list()
        self.ershoufangData = list()
        self.chengjiao = list()

    def getMaxPage(self,url):
        response = requests.get(url, headers = self.headers)
        if response.status_code == 200:
            source = response.text
            soup = BeautifulSoup(source, "html.parser")
            pageData = soup.find("div", class_ = "page-box house-lst-page-box")["page-data"]
            maxPage = eval(pageData)["totalPage"]
            return maxPage
        else:
            print("Fail status: {}".format(response.status_code))
            return None

    def parsePage(self, url):
        maxPagge = self.getMaxPage(url)
        for pageNum in range(1, maxPagge+1):
            url = "https://hz.lianjia.com/xiaoqu/pg{}/?from=rec".format(pageNum)
            print("当前正在爬取: {}".format(url))
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("div", class_="info")
            for i in links:
                link = i.find("a")["href"]    #每个<info clear>标签有很多<a>,而我们只需要第一个，所以用find
                detail = self.parseDetail(link)
                if detail != None:
                    # build = Build(city="杭州", name=detail.get("小区名称"), address=detail.get("地址"), watch=detail.get("关注人数"), price=detail.get("均价"), buildType=detail.get("建筑类型"),
                    #               propertyFee=detail.get("物业费用"), propertyCompany=detail.get("物业公司"), developer=detail.get("开发商"), buildNum=detail.get("楼栋总数"), num=detail.get("房屋总数"),
                    #               source="链家")
                    xiaoqu = Xiaoqu(address=detail.get("地址"), building=detail.get("楼栋总数"),  city="杭州", city_code=330100, company=detail.get("开发商"), name=detail.get("小区名称"),
                                  number=detail.get("房屋总数"), price=detail.get("均价"), property_company=detail.get("物业公司"), property_fee=detail.get("物业费用"), source="链家", type=detail.get("建筑类型"))
                    xiaoqu.save()
                    # self.datas.append(build)
        #  将所有爬取的二手房数据存储到csv文件中
        # data = pd.DataFrame(self.datas)
        # columns字段：自定义列的顺序（DataFrame默认按列名的字典序排序）
        # columns = ["小区名称", "地址", "关注人数", "均价", "建筑类型", "物业费用", "物业公司", "开发商","楼栋总数","房屋总数"]
        # data.to_csv(".\Lianjia_III.csv", encoding='utf_8_sig', index=False, columns=columns)



    def parseDetail(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            detail = {}
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                detail["小区名称"] = soup.find("h1", class_="detailTitle").text
                detail["地址"] = soup.find("div", class_="detailDesc").text
                detail["关注人数"] = soup.find("span", attrs={"data-role": "followNumber"}).text
                detail["均价"] = soup.find("span", class_="xiaoquUnitPrice").text
                info = soup.find("div", class_="xiaoquInfo").find_all("div", class_="xiaoquInfoItem")
                ershoufang = soup.find("div", class_="goodSellHeader clear").find("a")["href"]
                detail["二手房"] = ershoufang
                if ershoufang != None:
                    self.ershoufangData.append(ershoufang[34:-1])
                # chengjiao = soup.find("div", class_="frameDealList").find("a")["href"]
                # detail["成交"] = chengjiao
                # if chengjiao != None:
                #     chengjiao = self.chengjiao.append(chengjiao)
                detail["建筑类型"] = info[1].find("span", class_="xiaoquInfoContent").text
                detail["物业费用"] = info[2].find("span", class_="xiaoquInfoContent").text
                detail["物业公司"] = info[3].find("span", class_="xiaoquInfoContent").text
                detail["开发商"] = info[4].find("span", class_="xiaoquInfoContent").text
                detail["楼栋总数"] = info[5].find("span", class_="xiaoquInfoContent").text
                detail["房屋总数"] = info[6].find("span", class_="xiaoquInfoContent").text
                return detail
            else:
                return None
        except Exception:
            print(url)

    def erShoufangParse(self):
        if len(self.ershoufangData):
            for url in self.ershoufangData:
                maxPagge = self.getMaxPage("https://hz.lianjia.com/ershoufang/{}/".format(url))
                for pageNum in range(1, maxPagge + 1):
                    response = requests.get("https://hz.lianjia.com/ershoufang/pg{}".format(pageNum) + url+"/", headers=self.headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        links = soup.find_all("div", class_="info clear")
                        for i in links:
                            link = i.find("a")["href"]  # 每个<info clear>标签有很多<a>,而我们只需要第一个，所以用find
                            detail = self.ershoufangDetail(link)
                            if detail != None:
                                ershoufang = Ershoufang(xiaoqu_name=detail.get("小区名称"), area=detail.get("面积"),
                                                        area_in=detail.get("套内面积"), elevator=detail.get("梯户比例"),
                                                        location=detail.get("位置"), price=detail.get("价格"),
                                                        unit_price=detail.get("单价"), room_maininfo=detail.get("户型"),
                                                        room_subinfo=detail.get("楼层"), room_type=detail.get("朝向"),
                                                        sale_time=detail.get("挂牌时间"))
                                ershoufang.save()

    def ershoufangDetail(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            detail = {}
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                detail["小区名称"] = soup.find("div",class_="communityName").find("a").text
                locationInfo = soup.find("div", class_="areaName").find("span", class_="info").find_all("a")
                location = list()
                for weizhi in locationInfo:
                    location.append(weizhi.text)
                detail["位置"] = str(location)
                detail["价格"] = soup.find("div",class_="price").find("span").text
                detail["单价"] = soup.find("div", class_="unitPrice").find("span").text
                info = soup.find("div", class_="base").find_all("li")
                detail["户型"] = info[0].find("span").nextSibling
                detail["楼层"] = info[1].find("span").nextSibling
                detail["朝向"] = info[6].find("span").nextSibling
                detail["面积"] = info[2].find("span").nextSibling
                detail["套内面积"] = info[4].find("span").nextSibling
                detail["梯户比例"] = info[9].find("span").nextSibling
                info1 = soup.find("div", class_="transaction").find_all("li")
                detail["挂牌时间"] = info1[0].find_all("span")[1].text
                return detail
        except Exception:
            print(url)

    def chengjiaoParse(self):

        if len(self.ershoufangData):
            for url in self.ershoufangData:
                maxPagge = self.getMaxPage("https://hz.lianjia.com/chengjiao/{}/".format(url))
                for pageNum in range(1, maxPagge + 1):
                    response = requests.get("https://hz.lianjia.com/chengjiao/pg{}".format(pageNum) + url+"/", headers=self.headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        links = soup.find_all("div", class_="info")
                        for i in links:
                            link = i.find("a")["href"]  # 每个<info clear>标签有很多<a>,而我们只需要第一个，所以用find
                            detail = self.chengjiaoDetail(link)
                            chengjiao = Chengjiao(xiaoqu_name=detail.get("小区名称"), price=detail.get("成交价格"), sale_price=detail.get("挂牌价格"),time=detail.get("成交周期"),
                                                  area=detail.get("建筑面积"), room_info=detail.get("户型"), sale_time=detail.get("挂牌时间"),
                                                    floor=detail.get("楼层"))
                            chengjiao.save()

    def chengjiaoDetail(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            detail = {}
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                detail["小区名称"] = soup.find("div",class_="wrapper").text.split()[0]
                detail["成交价格"] = soup.find("div",class_="price").find("span", class_="dealTotalPrice").text

                info = soup.find("div", class_="msg").find_all("span")
                detail["挂牌价格"] = info[0].text
                detail["成交周期"] = info[1].text
                info1 = soup.find("div", class_="base").find_all("li")
                detail["户型"] = info1[0].find("span").nextSibling
                detail["楼层"] = info1[1].find("span").nextSibling
                detail["建筑面积"] = info1[2].find("span").nextSibling
                info2 = soup.find("div", class_="transaction").find_all("li")
                detail["挂牌时间"] = info2[2].find("span").nextSibling
                return detail
        except Exception:
            print(url)
if __name__ == "__main__":
    Lianjia = LianjiaESpider();
    Lianjia.parsePage("https://hz.lianjia.com/xiaoqu/?from=rec")
    print("小区拉取完成，开始拉取挂牌二手房")
    Lianjia.erShoufangParse()
    Lianjia.chengjiaoParse()