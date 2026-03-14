# Known protocol contracts - maps address (lowercase) → protocol name
KNOWN_PROTOCOLS = {
    # CoW Protocol
    "0x9008d19f58aabd9ed0d60971565aa8510560ab41": "CoW Protocol",

    # Uniswap
    "0x7a250d5630b4cf539739df2c5dacb4c659f2488d": "Uniswap V2",
    "0xe592427a0aece92de3edee1f18e0157c05861564": "Uniswap V3",
    "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45": "Uniswap V3 (Universal Router)",
    "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad": "Uniswap Universal Router",

    # 1inch
    "0x1111111254eeb25477b68fb85ed929f73a960582": "1inch V5",
    "0x111111125421ca6dc452d289314280a0f8842a65": "1inch V6",

    # Curve
    "0x99a58482bd75cbab83b27ec03ca68ff489b5788f": "Curve Router",
    "0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f": "SushiSwap Router",

    # Paraswap
    "0xdef171fe48cf0115b1d80b88dc8eab59176fee57": "Paraswap V5",

    # 0x / Matcha
    "0xdef1c0ded9bec7f1a1670819833240f027b25eff": "0x Exchange Proxy",

    # Balancer
    "0xba12222222228d8ba445958a75a0704d566bf2c8": "Balancer Vault",
}

# Known liquidity pool intermediaries - addresses that are pools, not protocols
# These help us skip intermediate hops when explaining
KNOWN_POOL_PREFIXES = []  # Could add more heuristics here


def detect_protocol(transfers: list) -> str:
    """
    Detect which protocol was used by checking if any intermediary address
    in the transfer chain matches a known protocol contract.
    """
    # Collect all addresses involved (from + to)
    all_addresses = set()
    for t in transfers:
        all_addresses.add(t["from"].lower())
        all_addresses.add(t["to"].lower())

    # Check each address against known protocols
    for addr in all_addresses:
        if addr in KNOWN_PROTOCOLS:
            return KNOWN_PROTOCOLS[addr]

    # Heuristic fallback: if one address appears as both sender and receiver
    # it's likely a settlement/aggregator contract
    from_addrs = [t["from"].lower() for t in transfers]
    to_addrs = [t["to"].lower() for t in transfers]
    intermediaries = set(from_addrs) & set(to_addrs)

    if intermediaries:
        return f"Unknown Aggregator ({list(intermediaries)[0][:10]}...)"

    return "Unknown Protocol"


def get_protocol_url(protocol_name: str) -> str:
    URLS = {
        "CoW Protocol": "https://cow.fi",
        "Uniswap V2": "https://app.uniswap.org",
        "Uniswap V3": "https://app.uniswap.org",
        "Uniswap V3 (Universal Router)": "https://app.uniswap.org",
        "Uniswap Universal Router": "https://app.uniswap.org",
        "1inch V5": "https://app.1inch.io",
        "1inch V6": "https://app.1inch.io",
        "SushiSwap Router": "https://www.sushi.com",
        "Paraswap V5": "https://app.paraswap.io",
        "0x Exchange Proxy": "https://matcha.xyz",
        "Balancer Vault": "https://balancer.fi",
        "Curve Router": "https://curve.fi",
    }
    return URLS.get(protocol_name, "")
