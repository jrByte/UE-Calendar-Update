import requests
import json
from bs4 import BeautifulSoup as bs


def checkStatusCode(requestCode, url):
    if requestCode == 200:
        print("[✔]: Successfully connected to: " + url)
    else:
        print("[X]: Failed to connect, code response was [" + requestCode + "] with URL: " + url)


class main:
    # Enter your username and password in the empty field bellow.
    def __init__(self, username="", password=""):
        self.username = username
        self.password = password
        self.dict = {}

    print("[!]: Main class in UEWebsite is running.")

    def loginWebsite(self):
        # This is for the website to know what kind of browser we are using. This mitigates potential problems if the website checks if this is a bot.
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }

        with requests.Session() as request:
            # Connecting to the login page specified in the URL bellow.
            url = 'https://onlinecampus.bits-hochschule.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=EXTERNALPAGES&ARGUMENTS=-N000000000000001,-N000299,-AHomedeWelcome'
            print("[!]: POST, Attempting to login.")
            print(
                "[!]: Note that if the KeyError is 'refresh'. Your username and password are either not entered or are incorrect.")
            login_data = {"usrname": self.username, "pass": self.password, "APPNAME": "CampusNet",
                          "PRGNAME": "LOGINCHECK",
                          "ARGUMENTS": "clino,usrname,pass,menuno,menu_type,browser,platform",
                          "clino": "000000000000001", "menuno": "000299", "menu_type": "Classic", "browser": "",
                          "platform": ""}
            site = request.post(url, login_data)

            # Below the code fetches the login token that the site gives us in the header response. This token is basically our credentials and how the site knows it's us.
            loginToken = site.headers["REFRESH"]
            # TODO: This could potentially go cause problems with the size of the token. Potential fix is needed.
            loginToken = str(loginToken[84:101])
            checkStatusCode(site.status_code, url)

            print("[✔]: Login token received." + loginToken)
            loginLocationURL = "/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=MONTH&ARGUMENTS=" + loginToken

            # This is now connecting to the calendar of the school for scheduled classes in the month view. Month is specified via date.
            dateCalendar = "01." + str(10) + ".2020"
            url = 'https://onlinecampus.bits-hochschule.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=MONTH&ARGUMENTS=' + loginToken + ",-N000354,-A" + dateCalendar + ",-A,-N000000000000000"

            print("[✔]: Getting the month of:" + dateCalendar)
            site = request.get(url, headers=headers, )
            checkStatusCode(site.status_code, url)

            try:
                # For windows computer
                soup = bs(site.content, 'html5lib')
                print("\n[✔]: Running lxml parsing.\n")
            except:
                # For mac computer
                soup = bs(site.content, 'lxml')
                print("\n[✔]: Running lxml parsing.\n")

            number = 0

            specificMonth = soup.findAll("tr", class_="")
            for allDays in specificMonth:
                daySchedule = allDays.findAll("td", class_="tbMonthDayCell")

                for getDate in daySchedule:
                    daySpecific = getDate.findAll("div", class_="appMonth")
                    # print(daySpecific)
                    date = str(getDate.find("div", class_="tbMonthDay").get("title")) + dateCalendar[2:]

                    for classes in daySpecific:
                        link = classes.findAll("a", class_="apmntLink")

                        for linkParsed in link:
                            number = number + 1
                            linkParsed = str(linkParsed.get("title"))
                            print("[✔]: This link is being parsed: ", str(linkParsed))
                            Index = linkParsed.find('/')
                            timeRange = linkParsed[:Index - 1]
                            linkParsed = linkParsed[Index + 2:]

                            Index = linkParsed.find('/')
                            roomNumber = linkParsed[:Index - 1]
                            linkParsed = linkParsed[Index + 2:]

                            Index = linkParsed.find('/')
                            className = linkParsed
                            linkParsed = linkParsed[Index + 2:]

                            # OMG I found the bug here vvv, the mistake made : self.dict[className] = {}
                            # Reason why its a bug? It's because if there is more than one class with the same name it
                            # will overwrite the other saved version of so called class. Solution: Just iterate by numbers per day.

                            numberDict = str(number)
                            self.dict[numberDict] = {}
                            self.dict[numberDict]['ClassName'] = className
                            self.dict[numberDict]['RoomNumber'] = roomNumber
                            self.dict[numberDict]['TimeRange'] = timeRange
                            self.dict[numberDict]['Date'] = date

                            # Good for checking if the data is flowing correctly.
                            # print("[!]: Printing Date: ", date)
                            # print("[!]: Number: ", number)


if __name__ == "__main__":
    session = main()
    session.loginWebsite()
