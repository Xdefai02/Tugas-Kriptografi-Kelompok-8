import re
import base64
import os

# Utility function to clean the text: remove spaces, symbols, and convert to lowercase
def clean_text(text):
    return re.sub(r'[^A-Za-z]', '', text).lower().replace("j", "i")

# Generate 5x5 matrix for Playfair cipher
def generate_playfair_matrix(key):
    key = clean_text(key)
    matrix = []
    alphabet = "abcdefghiklmnopqrstuvwxyz"  # 'j' diganti dengan 'i'
    used_chars = set()

    for char in key + alphabet:
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)
        if len(matrix) == 25:
            break

    return [matrix[i:i+5] for i in range(0, len(matrix), 5)]

# Find position of character in the matrix
def find_position(char, matrix):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col

# Split plaintext into pairs of characters for Playfair Cipher
def prepare_text_pairs(text):
    text = clean_text(text)
    pairs = []
    i = 0

    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = 'x'  # padding

        if a == b:
            pairs.append(a + 'x')
            i += 1
        else:
            pairs.append(a + b)
            i += 2

    if len(text) % 2 != 0:
        pairs.append(text[-1] + 'x')

    return pairs

# Encrypt a pair of characters using Playfair Cipher
def encrypt_pair(pair, matrix):
    row1, col1 = find_position(pair[0], matrix)
    row2, col2 = find_position(pair[1], matrix)

    if row1 == row2:
        # Same row, move right
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        # Same column, move down
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:
        # Rectangle swap
        return matrix[row1][col2] + matrix[row2][col1]

# Decrypt a pair of characters using Playfair Cipher
def decrypt_pair(pair, matrix):
    row1, col1 = find_position(pair[0], matrix)
    row2, col2 = find_position(pair[1], matrix)

    if row1 == row2:
        # Same row, move left
        return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:
        # Same column, move up
        return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
    else:
        # Rectangle swap
        return matrix[row1][col2] + matrix[row2][col1]

# Encrypt plaintext using Playfair Cipher
def encrypt_playfair(plaintext, key):
    matrix = generate_playfair_matrix(key)
    pairs = prepare_text_pairs(plaintext)
    ciphertext = ''

    for pair in pairs:
        ciphertext += encrypt_pair(pair, matrix)

    return ciphertext

# Decrypt ciphertext using Playfair Cipher
def decrypt_playfair(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    pairs = [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]
    plaintext = ''

    for pair in pairs:
        plaintext += decrypt_pair(pair, matrix)

    return plaintext

# Base64 encoding
def to_base64(text):
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    return encoded_bytes.decode("utf-8")

# Base64 decoding
def from_base64(base64_text):
    decoded_bytes = base64.b64decode(base64_text.encode("utf-8"))
    return decoded_bytes.decode("utf-8")

# Read from file
def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        print(f"File {file_path} tidak ditemukan.")
        return None

# Write to file
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Hasil telah disimpan ke: {file_path}")

def main():
    print("Playfair Cipher Encryption and Decryption")
    
    while True:
        print("\n1. Enkripsi Teks")
        print("2. Dekripsi Teks")
        print("3. Enkripsi File")
        print("4. Dekripsi File")
        print("5. Clear")
        print("6. Keluar")
        choice = input("Pilih opsi (1/2/3/4/5/6): ")
        
        if choice == '1':
            plaintext = input("Masukkan plaintext: ")
            key = input("Masukkan key (huruf saja): ")
            cleaned_plaintext = clean_text(plaintext)
            encrypted_text = encrypt_playfair(cleaned_plaintext, key)
            print(f"Hasil Enkripsi (Ciphertext): {encrypted_text}")
            print(f"Ciphertext dalam Base64: {to_base64(encrypted_text)}")

            # Simpan hasil ke file
            output_file = input("Masukkan nama file output untuk menyimpan hasil enkripsi (contoh: hasil_enkripsi.txt): ")
            write_file(output_file, encrypted_text)
        
        elif choice == '2':
            ciphertext = input("Masukkan ciphertext: ")
            key = input("Masukkan key (huruf saja): ")
            decrypted_text = decrypt_playfair(ciphertext, key)
            print(f"Hasil Dekripsi (Plaintext): {decrypted_text}")
            print(f"Plaintext dalam Base64: {to_base64(decrypted_text)}")

            # Simpan hasil ke file
            output_file = input("Masukkan nama file output untuk menyimpan hasil dekripsi (contoh: hasil_dekripsi.txt): ")
            write_file(output_file, decrypted_text)
        
        elif choice == '3':
            file_path = input("Masukkan path file untuk dienkripsi: ")
            file_content = read_file(file_path)
            if file_content:
                key = input("Masukkan key (huruf saja): ")
                cleaned_content = clean_text(file_content)
                encrypted_content = encrypt_playfair(cleaned_content, key)
                output_file = input("Masukkan nama file output (hasil enkripsi): ")
                write_file(output_file, encrypted_content)
                print(f"Ciphertext dalam Base64: {to_base64(encrypted_content)}")
        
        elif choice == '4':
            file_path = input("Masukkan path file untuk didekripsi: ")
            file_content = read_file(file_path)
            if file_content:
                key = input("Masukkan key (huruf saja): ")
                decrypted_content = decrypt_playfair(file_content, key)
                output_file = input("Masukkan nama file output (hasil dekripsi): ")
                write_file(output_file, decrypted_content)
                print(f"Plaintext dalam Base64: {to_base64(decrypted_content)}")
        
        elif choice == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
        
        elif choice == '6':
            print("Keluar dari program.")
            break
        
        else:
            print("Opsi tidak valid, silakan pilih antara 1, 2, 3, 4, atau 5.")

if __name__ == "__main__":
    main()
