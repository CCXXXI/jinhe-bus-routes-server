FROM mambaorg/micromamba:0.15.2
COPY --chown=micromamba:micromamba environment.yml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes \
COPY --chown=micromamba:micromamba src/ .
CMD ["python", "-m", "src.app"]
