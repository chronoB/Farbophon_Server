FROM python:3.9-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt && \
    cp instance/config.sample instance/config.py && \
    key=$(python -c "import os; print(os.urandom(24).hex())") && \
    sed -i 's/SecretKey/'$key'/g' instance/config.py && \
    mkdir -p db && \
    cd db && \
    touch farbophon.db && \
    cd .. && \
    python -c "from app import db; db.create_all()"

CMD python app.py

EXPOSE 5253
