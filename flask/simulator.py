"""Simulator utilities to turn YouTube channel stats into synthetic stock-like prices

This module provides functions to:
- map channel stats (subscribers, view_count) into an initial price and volatility
- generate a synthetic daily price series using a geometric Brownian motion-like model
- simulate a simple buy-and-hold portfolio across multiple channels

The models are intentionally simple and deterministic-seedable for reproducibility.
"""
from typing import Dict, List, Tuple
import math
import random
import statistics


def _seed(seed: int):
    random.seed(seed)


def map_stats_to_price_and_vol(stats: Dict[str, int]) -> Tuple[float, float]:
    """Map channel stats to an initial price and daily volatility.

    Heuristics used:
    - initial price scales with sqrt(subscribers) to dampen extremes
    - volatility inversely scales with log(views+1) so larger channels are slightly less volatile

    Args:
        stats: dict with keys 'subscriberCount' and 'viewCount' (integers)

    Returns:
        (initial_price, daily_volatility)
    """
    subs = int(stats.get("subscriberCount", 1000))
    views = int(stats.get("viewCount", 10000))

    # avoid zero/negative
    subs = max(subs, 1)
    views = max(views, 1)

    # initial price heuristic
    init_price = max(1.0, math.sqrt(subs) * 0.5)

    # volatility heuristic (daily stddev)
    vol = 0.02 + 0.08 / (math.log(views + 10) + 1)

    return float(init_price), float(vol)


def generate_price_series(
    stats: Dict[str, int],
    days: int = 90,
    seed: int = 42,
    drift: float = 0.0005,
) -> List[float]:
    """Generate a synthetic daily price series for a single channel.

    Uses a simple geometric random walk: S_t+1 = S_t * exp((mu - 0.5*sigma^2) + sigma * Z)
    where Z ~ N(0,1).

    Args:
        stats: channel stats dict with subscriberCount and viewCount
        days: number of days to simulate
        seed: RNG seed for reproducibility
        drift: base daily drift applied to all channels (can be positive/negative)

    Returns:
        list of daily prices, length = days
    """
    _seed(seed)
    s0, sigma = map_stats_to_price_and_vol(stats)
    prices = [s0]
    for _ in range(days - 1):
        # sample Z from standard normal
        z = random.gauss(0, 1)
        ret = (drift - 0.5 * sigma * sigma) + sigma * z
        next_price = max(0.01, prices[-1] * math.exp(ret))
        prices.append(next_price)
    return prices


def generate_stats_time_series(
    base_stats: Dict[str, int], days: int = 90, seed: int = 42
) -> List[Dict[str, int]]:
    """Generate a per-day time series of statistics (subscriberCount, viewCount).

    The generator uses a small positive drift with gaussian noise so counts slowly
    grow (or fluctuate) over time. Returns a list of dicts for each day.
    """
    _seed(seed)
    subs0 = int(base_stats.get("subscriberCount", 1000))
    views0 = int(base_stats.get("viewCount", 10000))

    subs0 = max(1, subs0)
    views0 = max(1, views0)

    series = []
    subs = subs0
    views = views0
    for _ in range(days):
        # small percent changes
        subs_change = random.gauss(0.0008, 0.005)  # mean growth ~0.08% daily
        views_change = random.gauss(0.001, 0.02)

        subs = max(0, int(subs * (1 + subs_change)))
        views = max(0, int(views * (1 + views_change)))

        series.append({"subscriberCount": subs, "viewCount": views})

    return series


def simulate_portfolio(
    channels: List[Dict],
    days: int = 7,
    seed: int = 42,
    allocation: Dict[str, float] = None,
) -> Dict:
    """Simulate a simple buy-and-hold portfolio across multiple channels.

    Each channel dict should include at least 'channel_name' and 'statistics'.

    Args:
        channels: list of channel dicts
        days: number of days to simulate
        seed: RNG seed
        allocation: optional dict mapping channel_name to fraction (sums to 1). If not
            provided, channels are equally weighted.

    Returns:
        dict with per-channel price series and portfolio value series
    """
    _seed(seed)
    n = len(channels)
    if n == 0:
        return {"portfolio": [], "channels": {}}

    if allocation is None:
        # equal weight
        weight = 1.0 / n
        allocation = {c.get("channel_name", f"ch{i}"): weight for i, c in enumerate(channels)}

    channel_prices = {}
    for i, ch in enumerate(channels):
        name = ch.get("channel_name", f"ch{i}")
        stats = ch.get("statistics", {})
        # derive a per-channel seed to keep reproducible but different
        ch_seed = seed + i * 100
        prices = generate_price_series(stats, days=days, seed=ch_seed)
        channel_prices[name] = prices

    # Build portfolio value series assuming $1 starting capital
    # buy proportional shares at day 0
    initial_capital = 500.0
    shares = {}
    for name, prices in channel_prices.items():
        w = allocation.get(name, 0.0)
        # dollar allocation
        dollars = initial_capital * w
        shares[name] = dollars / prices[0] if prices[0] > 0 else 0.0

    portfolio = []
    for day in range(days):
        total = 0.0
        for name, prices in channel_prices.items():
            total += shares[name] * prices[day]
        portfolio.append(total)

    return {"channels": channel_prices, "portfolio": portfolio, "allocation": allocation}


def summarize_portfolio(portfolio_values: List[float]) -> Dict[str, float]:
    """Return simple summary metrics for a portfolio value series."""
    if not portfolio_values:
        return {}
    start = portfolio_values[0]
    end = portfolio_values[-1]
    ret = (end / start) - 1.0 if start else 0.0
    daily_rets = [ (portfolio_values[i+1]/portfolio_values[i])-1 for i in range(len(portfolio_values)-1) if portfolio_values[i]>0 ]
    vol = statistics.pstdev(daily_rets) if daily_rets else 0.0
    return {"start": start, "end": end, "return": ret, "daily_vol": vol}
