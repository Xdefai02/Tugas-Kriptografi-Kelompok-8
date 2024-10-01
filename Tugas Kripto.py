import Vigenere_Cipher
import Auto_key_Vigenere_Cipher
import Playfair_Cipher
import Hill_Cipher
import Super_Encryption_Vigenere_And_Caesar_Cipher

def main():
    print("Program Enkripsi Dan Dekripsi Teks")
    print("Silahkan Pilih Algoritma Yang Akan Dipakai")

    while True:
        print("1. Vigenere Cipher")
        print("2. Varian Vigenere Cipher")
        print("3. Playfair Cipher")
        print("4. Hill Cipher")
        print("5. Super Enkripsi Cipher")
        print("6. Keluar")
        choice = input("Pilih opsi (1/2/3/4/5/6): ")

        if choice == '1':
            Vigenere_Cipher.main()

        elif choice == '2':
            Auto_key_Vigenere_Cipher.main()

        elif choice == '3':
            Playfair_Cipher.main()

        elif choice == '4':
            Hill_Cipher.main()
            
        elif choice == '5':
            Super_Encryption_Vigenere_And_Caesar_Cipher.main()
                
        elif choice == '6':
            print("Keluar dari program.")
            break
        
        else:
            print("Opsi tidak valid, silakan pilih antara 1, 2, atau 3.")
        
if __name__ == "__main__":
    main()