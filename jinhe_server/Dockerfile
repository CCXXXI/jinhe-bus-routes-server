FROM mambaorg/micromamba:0.15.2
WORKDIR /app
COPY environment.yml .
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes && \
    rm environment.yml
COPY src .
CMD ["python", "-m", "src.app"]
