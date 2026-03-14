from protocol import detect_protocol, get_protocol_url


def explain(tx, transfers):

    meaningful = []

    for t in transfers:

        if t["from"] == "0x0000000000000000000000000000000000000000":
            continue

        if t["to"] == "0x0000000000000000000000000000000000000000":
            continue

        if t["symbol"].startswith("aEth"):
            continue

        meaningful.append(t)

    if len(meaningful) < 2:
        return "Could not reconstruct swap."

    # Detect protocol from all transfers (before filtering)
    protocol = detect_protocol(transfers)
    protocol_url = get_protocol_url(protocol)

    # The user's token_out is the first transfer FROM the user
    # The user's token_in is the last transfer TO the user
    user = tx["from"].lower()

    # Find what the user sent out (first transfer where from == user)
    token_out = next(
        (t for t in meaningful if t["from"].lower() == user), meaningful[0]
    )

    # Find what the user received (last transfer where to == user)
    token_in = next(
        (t for t in reversed(meaningful) if t["to"].lower() == user), meaningful[-1]
    )

    protocol_line = f"{protocol}"
    if protocol_url:
        protocol_line += f" ({protocol_url})"

    return f"""Swap detected via {protocol_line}

Sent:     {token_out['amount']:.6f} {token_out['symbol']}
Received: {token_in['amount']:.6f} {token_in['symbol']}

Initiated by {tx['from']}
Tx hash: {tx['hash'].hex()}
"""
