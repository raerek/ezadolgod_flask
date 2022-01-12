from python:3.9-alpine

COPY . /app

WORKDIR /app

RUN pip3 --no-cache-dir install -r requirements.txt

#no access logging
#ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "app:app"]

#access logging to stderr
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "app:app", "--access-logfile", "-", "--access-logformat", "{'ip':'%(h)s','req_status':'%(r)s','req_path':'%(U)s','req_querystring':'%(q)s','req_timetaken':'%(D)s','resp_length':'%(B)s' 'resp_code':'%(s)s'}"]
