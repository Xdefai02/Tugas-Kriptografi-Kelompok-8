import math
import numpy
import sympy
import base64
import os

# Fungsi untuk membuat matriks kunci
def KeyMatrix(Key, n):
    Matrix = []
    for i in range(n):
        temp = list()
        for j in range(n):
            temp.append(ord(Key[i * n + j]) - 97)
        Matrix.append(temp)

    if numpy.linalg.det(Matrix) == 0:
        print("Invalid Key! Determinan kunci tidak boleh 0.")
        exit(None)
    return Matrix

# Fungsi untuk enkripsi
def Hill_encrypt(Plain, Matrix, n):
    cipher = ""
    for i in range(0, len(Plain), n):
        temp = Multiply(Matrix, Plain[i:i+n])
        for x in range(n):
            cipher += chr(temp[x][0] % 26 + 97)
    return cipher

# Fungsi untuk dekripsi
def Hill_decrypt(Matrix, Cipher, n):
    Plain = ""
    for i in range(0, len(Cipher), n):
        temp = Multiply(Matrix, Cipher[i:i+n])
        for x in range(n):
            Plain += chr(temp[x][0] % 26 + 97)
    return Plain

# Fungsi perkalian matriks
def Multiply(X, Y):
    result = numpy.zeros([len(X), 1], dtype=int)
    Y = list([ord(x) - 97] for x in Y)
    result = numpy.dot(X, Y)
    return result

# Fungsi untuk menghitung invers modulus (untuk dekripsi)
def modInverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return 1

# Modifikasi matriks untuk dekripsi
def KeyMatrix_decrypt(Key, n):
    Matrix = []
    for i in range(n):
        temp = list()
        for j in range(n):
            temp.append(ord(Key[i * n + j]) - 97)
        Matrix.append(temp)

    d = math.floor(numpy.linalg.det(Matrix))
    if d == 0:
        print("Invalid Key!")
        exit(None)

    A = sympy.Matrix(Matrix)
    A = (A.adjugate() * modInverse(d, 26)) % 26

    for i in range(n):
        for j in range(n):
            Matrix[i][j] = A[i, j]

    return Matrix

# Fungsi untuk mengenkripsi teks dan mengembalikan ciphertext asli dan dalam format Base64
def encrypt_text(key, plaintext):
    n = validate_key_length(key)
    for i in range(n - len(plaintext) % n):  # Tambahkan 'x' jika panjang tidak sesuai
        plaintext += 'x'

    Matrix = KeyMatrix(key, n)
    cipher_text = Hill_encrypt(plaintext, Matrix, n)
    cipher_text_base64 = base64.b64encode(cipher_text.encode()).decode()  # Ubah ke Base64
    return cipher_text, cipher_text_base64

# Fungsi untuk mendekripsi teks normal (tanpa Base64)
def decrypt_text(key, cipher_text):
    n = validate_key_length(key)
    Matrix = KeyMatrix_decrypt(key, n)
    plain_text = Hill_decrypt(Matrix, cipher_text, n)
    return plain_text

# Fungsi untuk enkripsi file
def encrypt_file(key, file_path):
    with open(file_path, 'r') as file:
        plaintext = file.read()
    
    cipher_text, cipher_text_base64 = encrypt_text(key, plaintext)
    
    with open(file_path + ".enc", 'w') as file:
        file.write(cipher_text_base64)

# Fungsi untuk dekripsi file
def decrypt_file(key, file_path):
    with open(file_path, 'r') as file:
        cipher_text_base64 = file.read()

    plain_text = decrypt_text(key, base64.b64decode(cipher_text_base64).decode())

    with open(file_path.replace(".enc", ".dec"), 'w') as file:
        file.write(plain_text)

# Fungsi untuk validasi panjang kunci (harus berupa kuadrat sempurna)
def validate_key_length(key):
    n = math.sqrt(len(key))
    if n != math.trunc(n) or n == 0:
        print("Invalid Key! Panjang kunci harus merupakan kuadrat sempurna (4 atau 9 huruf).")
        exit(None)
    return math.floor(n)
def main():
    print("\nVigenère Cipher Encryption and Decryption\n")
    while True:
        # Menu pilihan
        print("Pilih mode:")
        print("1. Enkripsi Teks")
        print("2. Dekripsi Teks")
        print("3. Enkripsi File")
        print("4. Dekripsi File")
        print("5. Clear")
        print("6. Keluar")
        choice = input("Masukkan pilihan (1/2/3/4/5/6): ")

        key = ''.join(input("Masukkan Key: ").lower().split())
        validate_key_length(key)  # Validasi kunci

        if choice == '1':
            # Enkripsi teks
            plaintext = ''.join(input("Masukkan PlainText: ").lower().split())
            cipher_text, cipher_text_base64 = encrypt_text(key, plaintext)
            print("CipherText:", cipher_text)
            print("CipherText dalam Base64:", cipher_text_base64)

        elif choice == '2':
            # Dekripsi teks
            cipher_text = input("Masukkan CipherText normal: ").lower()
            plain_text = decrypt_text(key, cipher_text)
            print("PlainText:", plain_text)

        elif choice == '3':
            # Enkripsi file
            file_path = input("Masukkan path file yang akan dienkripsi: ")
            encrypt_file(key, file_path)
            print(f"File dienkripsi dan disimpan sebagai {file_path}.enc")

        elif choice == '4':
            # Dekripsi file
            file_path = input("Masukkan path file yang akan didekripsi (harus .enc): ")
            decrypt_file(key, file_path)
            print(f"File didekripsi dan disimpan sebagai {file_path.replace('.enc', '.dec')}")

        elif choice == '5':
            os.system('cls')

        elif choice == '6':
            print("Keluar dari program.")
            break

        else:
            print("Pilihan tidak valid! Masukkan angka 1, 2, 3, atau 4.")

if __name__ == "__main__":
    main()