FROM python:3.12-slim-bookworm
RUN groupadd --gid 10001 app && useradd --uid 10001 --gid app --no-create-home app
WORKDIR /app
COPY hello.py /app/hello.py
USER 10001:10001
ENV PORT=8080
EXPOSE 8080
CMD ["python", "/app/hello.py"]
