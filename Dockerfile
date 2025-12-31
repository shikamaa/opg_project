FROM python:3.12.12

WORKDIR /opg

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6060

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6060"]
