# small helper utilities

def chunk_text(text, max_len=500):
    # naive chunker by sentences
    parts = []
    current = []
    cur_len = 0
    for line in text.split('\n'):
        l = len(line)
        if cur_len + l > max_len and current:
            parts.append('\n'.join(current))
            current = [line]
            cur_len = l
        else:
            current.append(line)
            cur_len += l
    if current:
        parts.append('\n'.join(current))
    return parts
