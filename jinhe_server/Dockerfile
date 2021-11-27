FROM mambaorg/micromamba:0.18.2
WORKDIR /app
COPY --chown=micromamba:micromamba environment.yml .
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes && \
    rm environment.yml
COPY src .
EXPOSE 80
CMD ["gunicorn", "app:app", "-b", ":80"]
