FROM python:3.8

WORKDIR /Skadi

ENV PATH="${PATH}:/root/.local/bin"

COPY ./ /Skadi/

RUN /usr/local/bin/python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip install --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 9221

VOLUME [ "/Skadi" ]

CMD [ "python3","main.py" ]
