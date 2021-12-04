FROM mambaorg/micromamba:0.19.0
WORKDIR /app

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc gcc-multilib gunicorn && \
    rm -rf /var/lib/apt/lists/*
USER micromamba

COPY environment.yml .
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes

COPY src app/
CMD ["gunicorn", "app:app"]
ENV PORT=80 SCRIPT_NAME=jinhe WEB_CONCURRENCY=5
EXPOSE 80
