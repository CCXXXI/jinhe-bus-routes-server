FROM mambaorg/micromamba:0.18.2
WORKDIR /app

COPY environment.yml .
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes

USER root
RUN rm environment.yml
USER micromamba

COPY src .
EXPOSE 80
CMD ["gunicorn", "app:app", "-b", ":80"]
