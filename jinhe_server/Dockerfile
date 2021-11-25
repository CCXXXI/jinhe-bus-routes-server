FROM mambaorg/micromamba:0.18.1
WORKDIR /app
COPY environment.yml .
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes
COPY src .
EXPOSE 80
CMD ["gunicorn", "app:app", "-b", ":80"]
