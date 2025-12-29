FROM python:3.12.12

WORKDIR /

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 6060

#COPY main.py .
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6060", "--reload"]
