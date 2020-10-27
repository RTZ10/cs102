def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    str1 = keyword.upper()
    while len(str1) < len(plaintext):
        str1 *= 2
    k = 0
    for i in plaintext:
        if 65 <= ord(i) <= 90:
            if ord(i) + (ord(str1[k]) - 65) > 90:
                ciphertext += chr(ord(i) + (ord(str1[k]) - 65) - 26)
            else:
                ciphertext += chr(ord(i) + (ord(str1[k]) - 65))
        elif 97 <= ord(i) <= 122:
            if ord(i) + (ord(str1[k]) - 65) > 122:
                ciphertext += chr(ord(i) + (ord(str1[k]) - 65) - 26)
            else:
                ciphertext += chr(ord(i) + (ord(str1[k]) - 65))
        else:
            ciphertext += i
        k += 1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    str2 = keyword.upper()
    while len(str2) < len(ciphertext):
        str2 *= 2
    k2 = 0
    for i in ciphertext:
        if 65 <= ord(i) <= 90:
            if ord(i) - (ord(str2[k2]) - 65) < 65:
                plaintext += chr(ord(i) - (ord(str2[k2]) - 65) + 26)
            else:
                plaintext += chr(ord(i) - (ord(str2[k2]) - 65))
        elif 97 <= ord(i) <= 122:
            if ord(i) - (ord(str2[k2]) - 65) < 97:
                plaintext += chr(ord(i) - (ord(str2[k2]) - 65) + 26)
            else:
                plaintext += chr(ord(i) - (ord(str2[k2]) - 65))
        else:
            plaintext += i
        k2 += 1
    return plaintext
