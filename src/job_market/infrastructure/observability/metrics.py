"""Lightweight in-process metrics collection."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class MetricsRegistry:
    request_count: int = 0
    error_count: int = 0
    route_counts: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    route_errors: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    route_latency_ms_total: dict[str, float] = field(default_factory=lambda: defaultdict(float))

    def record_request(self, route: str, latency_ms: float, status_code: int) -> None:
        self.request_count += 1
        self.route_counts[route] += 1
        self.route_latency_ms_total[route] += latency_ms

        if status_code >= 400:
            self.error_count += 1
            self.route_errors[route] += 1

    def snapshot(self) -> dict[str, object]:
        return {
            "requests_total": self.request_count,
            "errors_total": self.error_count,
            "routes": {
                route: {
                    "requests": self.route_counts[route],
                    "errors": self.route_errors[route],
                    "avg_latency_ms": round(
                        self.route_latency_ms_total[route] / self.route_counts[route],
                        2,
                    )
                    if self.route_counts[route]
                    else 0.0,
                }
                for route in sorted(self.route_counts)
            },
        }
