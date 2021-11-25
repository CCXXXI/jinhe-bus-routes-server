FROM mambaorg/micromamba:0.15.2
COPY environment.yml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes
COPY src/ ./
CMD ["python", "-m", "src.app"]
