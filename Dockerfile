FROM python:3.10

WORKDIR /app

COPY . /app/power_grid_env

RUN pip install --no-cache-dir -r power_grid_env/requirements.txt

CMD ["uvicorn", "power_grid_env.server.app:app", "--host", "0.0.0.0", "--port", "8000"]

