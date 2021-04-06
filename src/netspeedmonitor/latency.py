"""Code for measuring internet latency."""
import ipaddress
from datetime import datetime
from ipaddress import ip_address
from math import e
from typing import Dict, List

import ifaddr
from joblib import Parallel, delayed
from loguru import logger
from tcp_latency import measure_latency

from netspeedmonitor.database import log_data
from joblib import parallel_backend

sentinel_sites = [
    "google.com",
    "bing.com",
    "yahoo.com",
    "bbc.co.uk",
]


def record_latency(host: str, kind: str, runs: int = 10) -> Dict:
    """Record average latency of a host."""
    logger.info(f"Measuring site {host} latency")
    latency = None
    try:
        latencies = measure_latency(host, runs=runs, wait=0.1)
        if not all(map(lambda x: x is None, latencies)):
            latency = sum(latencies) / runs
    except Exception:
        pass
    data = dict(host=host, latency=latency, datetime=str(datetime.now()), kind=kind)
    logger.info(data)
    if data["kind"] == "local" and data["latency"] is not None:
        log_data(data, "latency")
    elif data["kind"] == "sentinel":
        log_data(data, "latency")
    return data


def measure_sentinels() -> List[Dict]:
    """Record the latency of sentinels."""
    with parallel_backend("threading", n_jobs=-1):
        Parallel()(delayed(record_latency)(host, "sentinel") for host in sentinel_sites)


def measure_local() -> List[Dict]:
    """Measure local IP latencies."""
    addresses = get_subnet_hosts()
    with parallel_backend("threading", n_jobs=256):
        Parallel()(delayed(record_latency)(host, "local") for host in addresses)


def get_subnet_hosts():
    """Return all hosts on the same subnetwork as the localhost."""
    local_ips = get_local_ips()
    addresses = []
    for ip in local_ips:
        network = ".".join(i for i in ip.split(".")[0:3])
        network += ".0/24"
        net = ipaddress.ip_network(network)
        for address in net:
            addresses.append(str(address))
    return addresses


def get_local_ips() -> List[str]:
    """Identify all IPv4 addresses for a machine."""
    excluded_ips = [ip_address("0.0.0.0"), ip_address("127.0.0.1")]
    local_ips = []
    adapters = ifaddr.get_adapters()

    for adapter in adapters:
        for ip in adapter.ips:
            try:
                if ip_address(ip.ip) not in excluded_ips:
                    local_ips.append(ip.ip)
            except TypeError:
                pass
    return local_ips
