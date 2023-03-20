from alibaba import Alibaba
import uvicorn
from multiprocessing import Process
from fastapi import FastAPI
from schema import SearchConfig
from db import fake_db

app = FastAPI(title="Alibaba FastApi App",
              debug=True,
              version="Version 1")


@app.post("/send_mail", status_code=201)
def send_mail_if_ticket_available(form_data: SearchConfig):
    obj = form_data.dict()
    alibaba = Alibaba()
    process = Process(target=alibaba.send_mail_if_ticket_available, args=(obj.get('origin_city_code'),
                                                                          obj.get('destination_city_code'),
                                                                          obj.get('request_dates'),
                                                                          obj.get('expected_time'),
                                                                          obj.get('target_mail')))
    process.start()
    return True


@app.get("/city_codes", status_code=200)
def get_city_codes():
    return fake_db


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3240, reload=True)
