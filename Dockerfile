FROM python:3.11

# Set the working directory
WORKDIR /src

COPY . /src
# install requirements
RUN pip install --no-cache-dir -r src/requirements.txt
# Expose the port Streamlit runs on
EXPOSE 8501


# Run Streamlit
CMD ["streamlit", "run", "Home.py", "--server.address=0.0.0.0"]
