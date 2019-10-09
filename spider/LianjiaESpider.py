import requests
from bs4 import BeautifulSoup
import pandas as pd
class LianjiaESpider(object):
    def __init__(self):
        self.headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
        self.datas = list()
        self.chengjiaoDatas = list()

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
        for pageNum in range(27, 31):
            url = "https://hz.lianjia.com/xiaoqu/pg{}/?from=rec".format(pageNum)
            print("当前正在爬取: {}".format(url))
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("div", class_="info")
            for i in links:
                link = i.find("a")["href"]    #每个<info clear>标签有很多<a>,而我们只需要第一个，所以用find
                detail = self.parseDetail(link)
                if detail != None:
                    self.datas.append(detail)
        #  将所有爬取的二手房数据存储到csv文件中
        data = pd.DataFrame(self.datas)
        # columns字段：自定义列的顺序（DataFrame默认按列名的字典序排序）
        columns = ["小区名称", "地址", "关注人数", "均价", "建筑类型", "物业费用", "物业公司", "开发商", "楼栋总数", "房屋总数"]
        data.to_csv(".\Lianjia_III.csv", encoding='utf_8_sig', index=False, columns=columns)

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

    def getChengjiaoDetail(self, id):
        url = "https://hz.lianjia.com/chengjiao/{}/".format("c"+id)
        response = requests.get(url, headers = self.headers)
if __name__ == "__main__":
    Lianjia = LianjiaESpider();
    Lianjia.parsePage("https://hz.lianjia.com/xiaoqu/?from=rec")