FROM python:3.12-slim-bookworm

RUN groupadd -g 1001 app && useradd -u 1001 -g app -m app

WORKDIR /app
COPY app/ /app/

USER 1001:1001
ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1

CMD ["python", "main.py"]
