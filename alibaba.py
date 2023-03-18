from requests import get
from json import loads
import smtplib
from time import sleep
from config import Config


class Alibaba:
    @staticmethod
    def send_email(message: str, target_mail: str):
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(Config.mail_user, Config.mail_pass)
        # print(message)
        s.sendmail(Config.mail_user, target_mail, message)
        s.quit()

    @staticmethod
    def get_ticket_info(origin_city_code: str = '26310000',
                        destination_city_code: str = '11320000',
                        request_date: str = '2023-03-24',
                        expected_time: dict = {}):

        url = f'https://ws.alibaba.ir/api/v2/bus/available?orginCityCode={origin_city_code}' \
              f'&destinationCityCode={destination_city_code}&requestDate={request_date}&passengerCount=1'

        # print(url)
        response = get(url)
        # print(response.status_code)

        response_json = loads(response.content)
        result = response_json['result']
        # print(result)
        availableList = result['availableList']
        for available in availableList:
            if 'availableSeats' in available and available['availableSeats'] != 0:
                departureTime = available['departureTime']
                if expected_time.get('higher_limit') >= departureTime >= expected_time.get('lower_limit'):
                    return departureTime

    def send_mail_if_ticket_available(self, origin_city_code, destination_city_code, request_dates, expected_time,
                                      target_mail):
        while True:
            for date in request_dates:
                try:
                    result1 = self.get_ticket_info(origin_city_code=origin_city_code,
                                                   destination_city_code=destination_city_code,
                                                   request_date=date,
                                                   expected_time=expected_time)
                    if result1:
                        try:
                            result2 = result1.split(":")
                            result1 = result2[0] + "-" + result2[1]
                        except:
                            pass
                        self.send_email(f'{date} and time {result1}', target_mail)
                except Exception as e:
                    pass
                    # self.send_email(f"error is {e}", target_mail)
                finally:
                    sleep(60)
            sleep(120)
