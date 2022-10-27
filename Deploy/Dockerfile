FROM gcc:12.2.0 as compiler
ADD prime.c /
RUN gcc -m64 -fPIC -shared prime.c -o libprime.so

FROM python:3.10.6-slim
ADD main.py /
COPY --from=compiler libprime.so /

RUN pip install --upgrade pip
RUN pip install primePy
RUN pip install fastapi
RUN pip install fastapi
RUN pip install Pillow
RUN pip install "passlib[bcrypt]"
RUN pip install python-multipart
RUN pip install uvicorn

COPY . .

CMD ["python", "main.py"]
EXPOSE 5000