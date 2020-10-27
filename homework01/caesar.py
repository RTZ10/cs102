import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        if 97 <= ord(i) <= 122:
            if ord(i) + shift > 122:
                ciphertext += chr(ord(i) + shift - 26)
            else:
                ciphertext += chr(ord(i) + shift)
        elif 65 <= ord(i) <= 90:
            if ord(i) + shift > 90:
                ciphertext += chr(ord(i) + shift - 26)
            else:
                ciphertext += chr(ord(i) + shift)
        else:
            ciphertext += str(i)
    ciphertext += ""

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        if 65 <= ord(i) <= 90:
            if ord(i) - shift < 65:
                plaintext += chr(ord(i) - shift + 26)
            else:
                plaintext += chr(ord(i) - shift)
        elif 97 <= ord(i) <= 122:
            if ord(i) - shift < 97:
                plaintext += chr(ord(i) - shift + 26)
            else:
                plaintext += chr(ord(i) - shift)
        else:
            plaintext += str(i)
    plaintext += ""
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
