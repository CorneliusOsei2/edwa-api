FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app/

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

