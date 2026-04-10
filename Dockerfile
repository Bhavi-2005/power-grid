FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

CMD ["uvicorn", "power_grid_env.server.app:app", "--host", "0.0.0.0", "--port", "7860"]

