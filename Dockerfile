FROM python:3.11

# Set the working directory
WORKDIR /src

COPY . /src
# install requirements
RUN pip install -r requirements.txt
# Expose the port Streamlit runs on
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "src/Home.py"]
