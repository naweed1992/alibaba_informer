from requests import get
from json import loads
from time import sleep
from utils import send_email
from db import sent_notifications


class Safar724:

    def __init__(self):
        self.cookies = {
            '_ga': 'GA1.2.1886344804.1680941543',
            '_gid': 'GA1.2.2047530385.1680941543',
            '_gat': '1',
            '__asc': 'c165aad81875fec6e42980f4981',
            '__auc': 'c165aad81875fec6e42980f4981',
            'sc_is_visitor_unique': 'rx10776183.1680941543.3D2F74AC1D854F435428AAA1C3787E1C.1.1.1.1.1.1.1.1.1',
            '_no_tracky_100913743': '1',
        }

        self.headers = {
            'authority': 'safar724.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            # 'cookie': '_ga=GA1.2.1886344804.1680941543; _gid=GA1.2.2047530385.1680941543; _gat=1; __asc=c165aad81875fec6e42980f4981; __auc=c165aad81875fec6e42980f4981; sc_is_visitor_unique=rx10776183.1680941543.3D2F74AC1D854F435428AAA1C3787E1C.1.1.1.1.1.1.1.1.1; _no_tracky_100913743=1',
            'referer': 'https://safar724.com/bus/tabriz-tehran?date=1402-01-31',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

    def get_ticket_info(self, origin_city_code: str = '26310000',
                        destination_city_code: str = '11320000',
                        request_date: str = '1402-01-31',
                        expected_time: dict = {}):

        params = {
            'origin': origin_city_code,
            'destination': destination_city_code,
            'date': request_date,
        }

        response = get('https://safar724.com/bus/getservices', params=params, cookies=self.cookies,
                       headers=self.headers)
        response_json = loads(response.content)
        items = response_json['Items']
        if len(items) >= 1:
            for item in items:
                if 'AvailableSeatCount' in item and item['AvailableSeatCount'] > 0:
                    DepartureTime = item['DepartureTime']
                    if expected_time.get('higher_limit') >= DepartureTime >= expected_time.get('lower_limit'):
                        return DepartureTime

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
                        except Exception as e:
                            pass
                            # print(e)
                            # send_email(f"error is {e}", target_mail)
                        if f"{date}+{result1}+{target_mail}" not in sent_notifications:
                            send_email(f'{date} and time {result1}', target_mail)
                            sent_notifications.add(f"{date}+{result1}+{target_mail}")
                except Exception as e:
                    pass
                    # print(e)
                    # send_email(f"error is {e}", target_mail)
                finally:
                    sleep(60)
            sleep(120)

    def get_city_codes_from_api(self):
        response = get('https://safar724.com/route/getcities', cookies=self.cookies, headers=self.headers)
        response_json = loads(response.content)
        final_dict = dict()
        for each in response_json:
            final_dict[each['Code']] = each['PersianName']
        return final_dict
