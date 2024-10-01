import re
import os
import base64

def generate_key(text, key):
    key = list(key)
    if len(key) == len(text):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def clean_text(text):
    # Hapus semua karakter selain huruf (a-z, A-Z) dan ubah huruf kapital menjadi kecil
    return re.sub(r'[^A-Za-z]', '', text).lower()

def validate_key(key):
    # Pastikan key hanya terdiri dari huruf (a-z, A-Z) tanpa simbol dan angka
    if re.match("^[A-Za-z]+$", key):
        return True
    else:
        return False

def encrypt_vigenere(text, key):
    ciphertext = []
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            shift = ord(key[i].lower()) - ord('a')
            encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext.append(encrypted_char)
    return "".join(ciphertext)

def decrypt_vigenere(ciphertext, key):
    plaintext = []
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isalpha():
            shift = ord(key[i].lower()) - ord('a')
            decrypted_char = chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))
            plaintext.append(decrypted_char)
    return "".join(plaintext)

def to_base64(text):
    # Encode teks ke Base64
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    return encoded_bytes.decode("utf-8")

def from_base64(base64_text):
    # Decode teks dari Base64
    decoded_bytes = base64.b64decode(base64_text.encode("utf-8"))
    return decoded_bytes.decode("utf-8")

def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        print(f"File {file_path} tidak ditemukan.")
        return None

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Hasil telah disimpan ke: {file_path}")

def main():
    print("\nVigenère Cipher Encryption and Decryption\n")
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
                key = input("Masukkan key: ")
                if validate_key(key):
                    break
                else:
                    print("Key tidak valid! Masukkan key yang hanya terdiri dari huruf tanpa angka atau simbol.")
            # Hapus simbol dan spasi dari plaintext, ubah ke huruf kecil
            cleaned_plaintext = clean_text(plaintext)
            key = generate_key(cleaned_plaintext, key)
            encrypted_text = encrypt_vigenere(cleaned_plaintext, key)
            print(f"Hasil Enkripsi (Ciphertext): {encrypted_text}")
            print(f"Ciphertext dalam Base64: {to_base64(encrypted_text)}")

        elif choice == '2':
            ciphertext = input("Masukkan ciphertext: ")
            while True:
                key = input("Masukkan key: ")
                if validate_key(key):
                    break
                else:
                    print("Key tidak valid! Masukkan key yang hanya terdiri dari huruf tanpa angka atau simbol.")
            key = generate_key(ciphertext, key)
            decrypted_text = decrypt_vigenere(ciphertext, key)
            print(f"Hasil Dekripsi (Plaintext): {decrypted_text}")
            print(f"Plaintext dalam Base64: {to_base64(decrypted_text)}")

        elif choice == '3':
            file_path = input("Masukkan path file untuk dienkripsi: ")
            file_content = read_file(file_path)
            if file_content:
                while True:
                    key = input("Masukkan key: ")
                    if validate_key(key):
                        break
                    else:
                        print("Key tidak valid! Masukkan key yang hanya terdiri dari huruf tanpa angka atau simbol.")
                # Hapus simbol dan spasi dari file content, ubah ke huruf kecil
                cleaned_content = clean_text(file_content)
                key = generate_key(cleaned_content, key)
                encrypted_content = encrypt_vigenere(cleaned_content, key)
                output_file = input("Masukkan nama file output (hasil enkripsi): ")
                write_file(output_file, encrypted_content)
                print(f"Ciphertext dalam Base64: {to_base64(encrypted_content)}")

        elif choice == '4':
            file_path = input("Masukkan path file untuk didekripsi: ")
            file_content = read_file(file_path)
            if file_content:
                while True:
                    key = input("Masukkan key: ")
                    if validate_key(key):
                        break
                    else:
                        print("Key tidak valid! Masukkan key yang hanya terdiri dari huruf tanpa angka atau simbol.")
                key = generate_key(file_content, key)
                decrypted_content = decrypt_vigenere(file_content, key)
                output_file = input("Masukkan nama file output (hasil dekripsi): ")
                write_file(output_file, decrypted_content)
                print(f"Plaintext dalam Base64: {to_base64(decrypted_content)}")

        elif choice == '5':
            os.system('cls')

        elif choice == '6':
            print("Keluar dari program.")
            break

        else:
            print("Opsi tidak valid, silakan pilih antara 1, 2, 3, 4, atau 5.")

if __name__ == "__main__":
    main()
