"""Micro-benchmark: JWT encode/decode + token bucket throughput."""

import time

from mcplane.auth.jwt import JwtCodec
from mcplane.policy.ratelimit import TokenBucket


def bench_jwt(n=20000):
    codec = JwtCodec("bench-secret")
    start = time.perf_counter()
    for _ in range(n):
        tok = codec.encode({"sub": "bench"})
        codec.decode(tok)
    return n / (time.perf_counter() - start)


def bench_bucket(n=1000000):
    b = TokenBucket(rate=1e9, burst=n)
    start = time.perf_counter()
    for _ in range(n):
        b.consume()
    return n / (time.perf_counter() - start)


def main():
    jwt_ops = bench_jwt()
    print("JWT encode+decode : %.0f ops/s" % jwt_ops)
    bucket_ops = bench_bucket()
    print("TokenBucket consume: %.0f ops/s" % bucket_ops)


if __name__ == "__main__":
    main()
