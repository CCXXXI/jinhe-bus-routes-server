FROM redislabs/redisgraph:2.8
COPY dump.rdb /data/
CMD ["redis-server", "--loadmodule", "/usr/lib/redis/modules/redisgraph.so", "CACHE_SIZE", "65536"]
