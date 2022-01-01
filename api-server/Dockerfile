FROM python:3.7.6

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY recommend_learning_paths.py ./recommend_learning_paths.py
COPY app.py ./app.py
COPY TestOntology_20210727.owl ./TestOntology_20210727.owl
COPY it-career-bot-firebase-adminsdk-kyvys-870e6b3f02.json ./it-career-bot-firebase-adminsdk-kyvys-870e6b3f02.json


ENTRYPOINT ["python", "app.py"]