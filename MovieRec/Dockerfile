FROM python:3.12-slim

# Set environment variables
#  for immediate loggin and better debugging
ENV PYTHONUNBUFFERED=1 
# stops python form creating pycache files to save space
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /MovieRec

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# copy requirements first. 
# this will make a dependency layer, which speeds up builds if unchanged
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Remove .env files from container 
# (apparently Render doesn't need them and it's better for security)
RUN rm -f .env .env.prod

# download static files
RUN mkdir -p staticfiles
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# using gunicorn for production environment
CMD  ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]