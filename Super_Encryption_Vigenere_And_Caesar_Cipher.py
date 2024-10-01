import re
import os
import base64

# Fungsi untuk menghasilkan key pada Vigenère Cipher
def generate_key(text, key):
    key = list(key)
    if len(key) == len(text):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

# Bersihkan teks dari karakter selain huruf dan ubah menjadi huruf kecil
def clean_text(text):
    return re.sub(r'[^A-Za-z]', '', text).lower()

# Validasi key agar hanya berisi huruf
def validate_key(key):
    return re.match("^[A-Za-z]+$", key) is not None

# Enkripsi Vigenère Cipher
def encrypt_vigenere(text, key):
    ciphertext = []
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            shift = ord(key[i].lower()) - ord('a')
            encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext.append(encrypted_char)
    return "".join(ciphertext)

# Dekripsi Vigenère Cipher
def decrypt_vigenere(ciphertext, key):
    plaintext = []
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isalpha():
            shift = ord(key[i].lower()) - ord('a')
            decrypted_char = chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))
            plaintext.append(decrypted_char)
    return "".join(plaintext)

# Enkripsi Caesar Cipher
def encrypt_caesar(text, shift):
    ciphertext = []
    for char in text:
        if char.isalpha():
            encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext.append(encrypted_char)
    return "".join(ciphertext)

# Dekripsi Caesar Cipher
def decrypt_caesar(ciphertext, shift):
    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            decrypted_char = chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))
            plaintext.append(decrypted_char)
    return "".join(plaintext)

# Encode ke Base64
def to_base64(text):
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    return encoded_bytes.decode("utf-8")

# Decode dari Base64
def from_base64(base64_text):
    decoded_bytes = base64.b64decode(base64_text.encode("utf-8"))
    return decoded_bytes.decode("utf-8")

# Fungsi untuk membaca file
def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        print(f"File {file_path} tidak ditemukan.")
        return None

# Fungsi untuk menulis file
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Hasil telah disimpan ke: {file_path}")

# Fungsi utama
def main():
    print("\nProgram Super Enkripsi: Vigenère + Caesar Cipher\n")
    while True:
        print("1. Enkripsi Teks")
        print("2. Dekripsi Teks")
        print("3. Enkripsi File")
        print("4. Dekripsi File")
        print("5. Clear")
        print("6. Keluar")
        choice = input("Pilih opsi (1/2/3/4/5/6): ")

        if choice == '1':
            plaintext = input("Masukkan plaintext: ")
            while True:
                key = input("Masukkan key Vigenère: ")
                if validate_key(key):
                    break
                else:
                    print("Key tidak valid! Masukkan key yang hanya terdiri dari huruf tanpa angka atau simbol.")
            
            # Bersihkan teks
            cleaned_plaintext = clean_text(plaintext)
            key = generate_key(cleaned_plaintext, key)

            # Enkripsi Vigenère
            encrypted_vigenere = encrypt_vigenere(cleaned_plaintext, key)

            # Enkripsi Caesar
            caesar_shift = int(input("Masukkan pergeseran Caesar Cipher (0-25): "))
            encrypted_caesar = encrypt_caesar(encrypted_vigenere, caesar_shift)

            print(f"Hasil Enkripsi (Vigenère + Caesar): {encrypted_caesar}")
            print(f"Ciphertext dalam Base64: {to_base64(encrypted_caesar)}")

        elif choice == '2':
            ciphertext = input("Masukkan ciphertext: ")
            while True:
                key = input("Masukkan key Vigenère: ")
                if validate_key(key):
                    break
                else:
                    print("Key tidak valid! Masukkan key yang hanya terdiri dari huruf tanpa angka atau simbol.")

            # Dekripsi Caesar
            caesar_shift = int(input("Masukkan pergeseran Caesar Cipher (0-25): "))
            decrypted_caesar = decrypt_caesar(ciphertext, caesar_shift)

            # Dekripsi Vigenère
            key = generate_key(decrypted_caesar, key)
            decrypted_vigenere = decrypt_vigenere(decrypted_caesar, key)

            print(f"Hasil Dekripsi (Plaintext): {decrypted_vigenere}")
            print(f"Plaintext dalam Base64: {to_base64(decrypted_vigenere)}")

        elif choice == '3':
            file_path = input("Masukkan path file untuk dienkripsi: ")
            file_content = read_file(file_path)
            if file_content:
                while True:
                    key = input("Masukkan key Vigenère: ")
                    if validate_key(key):
                        break
                    else:
                        print("Key tidak valid! Masukkan key yang hanya terdiri dari huruf tanpa angka atau simbol.")
                
                cleaned_content = clean_text(file_content)
                key = generate_key(cleaned_content, key)

                # Enkripsi Vigenère
                encrypted_vigenere = encrypt_vigenere(cleaned_content, key)

                # Enkripsi Caesar
                caesar_shift = int(input("Masukkan pergeseran Caesar Cipher (0-25): "))
                encrypted_caesar = encrypt_caesar(encrypted_vigenere, caesar_shift)

                output_file = input("Masukkan nama file output (hasil enkripsi): ")
                write_file(output_file, encrypted_caesar)
                print(f"Ciphertext dalam Base64: {to_base64(encrypted_caesar)}")

        elif choice == '4':
            file_path = input("Masukkan path file untuk didekripsi: ")
            file_content = read_file(file_path)
            if file_content:
                while True:
                    key = input("Masukkan key Vigenère: ")
                    if validate_key(key):
                        break
                    else:
                        print("Key tidak valid! Masukkan key yang hanya terdiri dari huruf tanpa angka atau simbol.")
                
                # Dekripsi Caesar
                caesar_shift = int(input("Masukkan pergeseran Caesar Cipher (0-25): "))
                decrypted_caesar = decrypt_caesar(file_content, caesar_shift)

                # Dekripsi Vigenère
                key = generate_key(decrypted_caesar, key)
                decrypted_vigenere = decrypt_vigenere(decrypted_caesar, key)

                output_file = input("Masukkan nama file output (hasil dekripsi): ")
                write_file(output_file, decrypted_vigenere)
                print(f"Plaintext dalam Base64: {to_base64(decrypted_vigenere)}")

        elif choice == '5':
            os.system('cls' if os.name == 'nt' else 'clear')

        elif choice == '6':
            print("Keluar dari program.")
            break

        else:
            print("Opsi tidak valid, silakan pilih antara 1, 2, 3, 4, atau 5.")

if __name__ == "__main__":
    main()
