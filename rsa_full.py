import random

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a, b):
    """Calculate the greatest common divisor of two numbers."""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """Calculate the modular multiplicative inverse of a modulo m."""
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(bits=32):
    """Generate an RSA key pair."""
    # Choose two large prime numbers
    p = q = 0
    while not is_prime(p):
        p = random.getrandbits(bits)
    while not is_prime(q) or p == q:
        q = random.getrandbits(bits)

    # Compute n (modulus)
    n = p * q

    # Compute totient (Euler's totient function)
    phi = (p - 1) * (q - 1)

    # Choose public exponent e (typically 65537)
    e = 65537

    # Compute private exponent d
    d = mod_inverse(e, phi)

    # Public key: (e, n), Private key: (d, n)
    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

def encrypt(message, public_key):
    """Encrypt a message using RSA."""
    e, n = public_key
    return pow(message, e, n)

def decrypt(ciphertext, private_key):
    """Decrypt a ciphertext using RSA."""
    d, n = private_key
    return pow(ciphertext, d, n)

def write_key_to_file(key, filename):
    """Write the key to a text file."""
    with open(filename, 'w') as file:
        file.write(','.join(map(str, key)))

def read_key_from_file(filename):
    """Read the key from a text file."""
    with open(filename, 'r') as file:
        key_values = file.read().split(',')
    return tuple(map(int, key_values))

# Example usage:
plaintext = 123444444444442

# Generate key pair
public_key, private_key = generate_keypair()

# Write public key to a file
write_key_to_file(public_key, 'E:/downloads/public_key.txt')

# Write private key to a file
write_key_to_file(private_key, 'E:/downloads/private_key.txt')

# Read public key from a file
read_public_key = read_key_from_file('E:/downloads/public_key.txt')

# Read private key from a file
read_private_key = read_key_from_file('E:/downloads/public_key.txt')

# Encrypt the number
encrypted_number = encrypt(plaintext, read_public_key)

# Decrypt the encrypted number
decrypted_number = decrypt(encrypted_number, read_private_key)

print("Original Number:", plaintext)
print("Encrypted Number:", encrypted_number)
print("Decrypted Number:", decrypted_number)
