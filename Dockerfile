# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory
WORKDIR /src

# Copy only the requirements file first to leverage caching
COPY requirements.txt /src/requirements.txt

# Install dependencies (leverage cache if requirements haven't changed)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /src

# Expose the port Streamlit runs on
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "src/Home.py"]
