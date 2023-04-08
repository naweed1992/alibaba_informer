from alibaba import Alibaba
from safar724 import Safar724
import uvicorn
from multiprocessing import Process
from fastapi import FastAPI
from schema import SearchConfig
from db import fake_db

app = FastAPI(title="Alibaba and Safar724 FastApi App",
              debug=False,
              version="Version 2")


@app.post("/send_mail", status_code=201)
def send_mail_if_ticket_available(form_data: SearchConfig):
    obj = form_data.dict()
    alibaba = Alibaba()
    safar724 = Safar724()
    request_dates = obj.get('request_dates')
    if len(request_dates) == 0:
        return False
    first_request_date = request_dates[0]
    if first_request_date.startswith("2023"):
        process = Process(target=alibaba.send_mail_if_ticket_available, args=(obj.get('origin_city_code'),
                                                                              obj.get('destination_city_code'),
                                                                              obj.get('request_dates'),
                                                                              obj.get('expected_time'),
                                                                              obj.get('target_mail')))
    else:
        process = Process(target=safar724.send_mail_if_ticket_available, args=(obj.get('origin_city_code'),
                                                                               obj.get('destination_city_code'),
                                                                               obj.get('request_dates'),
                                                                               obj.get('expected_time'),
                                                                               obj.get('target_mail')))
    process.start()
    return True


@app.get("/city_codes_alibaba", status_code=200)
def get_city_codes_alibaba():
    return fake_db


@app.get("/city_codes_safar724", status_code=200)
def get_city_codes_safar724():
    safar724 = Safar724()
    cities = safar724.get_city_codes_from_api()
    return cities


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3240, reload=True)
