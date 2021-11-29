FROM mambaorg/micromamba:0.18.2
WORKDIR /app

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc gcc-multilib && \
    rm -rf /var/lib/apt/lists/*
USER micromamba

COPY environment.yml .
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes

COPY src .
EXPOSE 80
CMD ["gunicorn", "app:app", "-b", ":80"]
