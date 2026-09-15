FROM python:3.12-slim-bookworm

RUN groupadd --gid 10001 banking && useradd --uid 10001 --gid banking --no-create-home banking
WORKDIR /app
COPY services/app.py /app/app.py
USER 10001:10001
ENV PORT=8080
EXPOSE 8080
HEALTHCHECK --interval=20s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1
CMD ["python", "/app/app.py"]
