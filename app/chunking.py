def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    chunks = []
    n = len(text)
    i = 0
    while i < n:
        j = min(i + chunk_size, n)
        piece = text[i:j].strip()
        if piece:
            chunks.append(piece)
        if j == n:
            break
        i = j - overlap
        if i < 0:
            i = 0
    return chunks
