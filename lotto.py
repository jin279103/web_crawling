import requests
from bs4 import BeautifulSoup
import pymysql
import sys

lotto_list = []
basic_url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo="

def crawler():
    for i in range(1, 918):
        crawler_url = basic_url + str(i)
        print("crawler: " + crawler_url)
        resp = requests.get(crawler_url)
        soup = BeautifulSoup(resp.text, "lxml")
        line = str(soup.find("meta", {"id": "desc", "name": "description"})['content'])
        begin = line.find("당첨번호")
        begin = line.find(" ", begin) + 1
        end = line.find(".", begin)
        numbers = line[begin:end]
        begin = line.find("총")
        begin = line.find(" ", begin) + 1
        end = line.find("명", begin)
        persons = line[begin:end]
        begin = line.find("당첨금액")
        begin = line.find(" ", begin) + 1
        end = line.find("원", begin)
        amount = line[begin:end]
        info = {}
        info["회차"] = i
        info["번호"] = numbers
        info["당첨자"] = persons
        info["금액"] = amount
        lotto_list.append(info)

def insert():
    db = pymysql.connect(host="192.168.56.104", user="lotto", password="lotto", db="lotto")
    cursor = db.cursor()
    for dic in lotto_list:
        count = dic["회차"]
        numbers = dic["번호"]
        persons = dic["당첨자"]
        amounts = dic["금액"]
        print("insert to database at " + str(count))
        numberlist = str(numbers).split(",")
        sql = "INSERT INTO lotto.data \
              VALUES('%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%s')" \
              % (count, int(numberlist[0]), int(numberlist[1]), int(numberlist[2]), int(numberlist[3]), int(numberlist[4]), int(numberlist[5].split("+")[0]), int(numberlist[5].split("+")[1]), int(persons), str(amounts))
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            db.rollback()
            break
    db.close()

def main():
    crawler()
    insert()

if __name__ == "__main__":
    main()

