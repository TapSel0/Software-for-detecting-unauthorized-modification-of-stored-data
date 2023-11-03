def GOST_hash(data: bytes) -> str:
    h = 0x0101010101010101
    l = 0x7F7F7F7F7F7F7F7F
    for b in data:
        h = (h + b) % l
        h = (h << 1) % l
        if (h & 0x100000000):
            h ^= 0x1C3C3C3C57
    return hex(h)[2:]