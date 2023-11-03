def P(x):
    return ((x << 31) | (x >> 1))


def L(A):
    B = []
    for i in range(8):
        x = 0
        for j in range(8):
            x |= A[j] << (8*j)
        x = P(x)
        for j in range(8):
            B.append((x >> (8*j)) & 0xff)
        A = B[-8:]
    return B


def X(A, B):
    return [a ^ b for a, b in zip(A, B)]


def Str512(message):
    h = [0]*64
    v = [0]*64
    for i in range(64):
        h[i] = 0x0101010101010101 * i
        v[i] = 0x79797b7b7b7b7b7b ^ h[i]

    msg = message
    l = len(msg) % 64
    if l < 56:
        msg += b'\x01' + b'\x00'*(55-l)
    else:
        msg += b'\x01' + b'\x00'*(63-l)
        h = L(h)
        v = X(v, h)

    msg += len(message).to_bytes(8, byteorder='little')
    l = len(msg)

    for i in range(0, l, 64):
        M = msg[i:i+64]
        N = X(M, h)
        h = L(h)
        v = X(v, N)
        v = L(v)

    v = X(v, msg[:64])
    v = L(v)
    v = X(v, h)

    return bytes(v[:32]).hex()

#
# def stribog_hash(fname):
#     with open(fname, 'rb') as f:
#         data = f.read()
#     return Str512(data).hex()




