FROM python:3.11.3
ENV TZ=Asia/Shanghai
WORKDIR /chatgpt_web/
ADD ./requirements.txt ./pyproject.toml ./poetry.lock /chatgpt_web/
RUN pip install poetry -i https://mirrors.aliyun.com/pypi/simple/ && poetry install
ADD . /chatgpt_web/
ENTRYPOINT ["poetry", "run"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]