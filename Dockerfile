FROM python:2.7

RUN mkdir /src
WORKDIR /src

RUN pip install jinja2
ADD gen_config.py /src/gen_config.py
ADD templates /src/templates
ADD config_outs /src/config_outs
ADD config.json /src/config.json
CMD [ "python", "./gen_config.py" ]
