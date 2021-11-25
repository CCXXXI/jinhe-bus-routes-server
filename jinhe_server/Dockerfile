FROM mambaorg/micromamba:0.15.2
WORKDIR /app
COPY environment.yml .
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes
COPY src .
EXPOSE 80
CMD ["python", "-m", "src.app"]
