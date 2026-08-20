from mcplane.policy.ratelimit import TokenBucket, RateLimiter
from mcplane.errors import RateLimitError


def test_bucket_consumes():
    b = TokenBucket(rate=100, burst=5)
    assert b.consume() is True


def test_bucket_exhausted():
    b = TokenBucket(rate=0.0001, burst=2)
    assert b.consume() is True
    assert b.consume() is True
    assert b.consume() is False


def test_limiter_guard():
    lim = RateLimiter(requests_per_second=0.0001, burst=1)
    assert lim.allow("k") is True
    try:
        lim.guard("k")
        assert False
    except RateLimitError:
        pass
