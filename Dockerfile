# Use Python 3.11 base image
FROM python:3.11-slim

# Set environment variables for venv and Python behavior
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Create virtual environment
RUN python -m venv $VIRTUAL_ENV

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . .
RUN chmod -R 777 /app/data

# Upgrade pip and install dependencies inside virtual environment
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

CMD ["bash", "-c", "cd backend && uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]
