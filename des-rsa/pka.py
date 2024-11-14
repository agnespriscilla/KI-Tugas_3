import json

# Simulasi penyimpanan public key yang valid
valid_public_keys = {
    "client1": {"e": 65537, "n": 1234567890123456},  # Contoh public key untuk client1
    "client2": {"e": 65537, "n": 9876543210987654},  # Contoh public key untuk client2
}

def get_public_key(client_id):
    """Menambahkan validasi dengan public key authority."""
    if client_id in valid_public_keys:
        return valid_public_keys[client_id]
    else:
        raise ValueError("Public key untuk client ini tidak ditemukan atau tidak valid.")