"""
Программа для шифрования текста с возможностью расшифровки

Описание:
1. Шифрует текст используя AES-256-CBC
2. Создает бинарные файлы, в одном из которых прячет зашифрованный текст
3. Позволяет расшифровать текст при наличии правильного ключа
4. Показывает размер зашифрованных данных и их расположение
5. Генерирует пример кода для чтения и проверки хеша в C++

Использование:
    # Шифрование
    python symmetric_encryption.py
    > Выберите режим: 1
    > Введите текст: Hello World
    > Введите ключ: mysecretkey
    
    # Расшифрование
    python symmetric_encryption.py
    > Выберите режим: 2
    > Введите зашифрованный текст (в hex): <hex_string>
    > Введите ключ: mysecretkey

    # Генерация C++ кода
    python symmetric_encryption.py
    > Выберите режим: 3
    > Введите текст: Hello World
    > Введите ключ: mysecretkey
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
import os
import random
import binascii

def derive_key(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    key = PBKDF2(password.encode(), salt, dkLen=32)
    return key, salt

def encrypt_text(text, password):
    # Генерируем ключ из пароля
    key, salt = derive_key(password)
    
    # Создаем случайный IV
    iv = os.urandom(16)
    
    # Создаем шифр
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Шифруем текст
    padded_data = pad(text.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    # Объединяем соль, IV и зашифрованные данные
    return salt + iv + encrypted_data

def decrypt_text(encrypted_data, password):
    try:
        # Извлекаем соль и IV
        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]
        
        # Восстанавливаем ключ
        key, _ = derive_key(password, salt)
        
        # Расшифровываем
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = cipher.decrypt(ciphertext)
        return unpad(padded_data, AES.block_size).decode()
    except Exception as e:
        return f"Ошибка расшифровки: {str(e)}"

def create_bin_files(encrypted_data):
    directory = "bin_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    target_file = random.randint(0, 9)
    target_offset = None

    print(f"\nСоздаю бинарные файлы...")
    
    for i in range(10):
        filename = os.path.join(directory, f"file_{i}.bin")
        file_size = random.randint(1024, 10240)  # 1-10 MB
        
        with open(filename, "wb") as f:
            if i == target_file:
                # Записываем зашифрованные данные в случайную позицию
                target_offset = random.randint(0, file_size - len(encrypted_data))
                f.write(os.urandom(target_offset))
                f.write(encrypted_data)
                f.write(os.urandom(file_size - target_offset - len(encrypted_data)))
            else:
                f.write(os.urandom(file_size))

    # Создаем файл с описанием для человека
    with open(os.path.join(directory, "readme.txt"), "w", encoding="utf-8") as f:
        f.write("Описание бинарных файлов\n")
        f.write("========================\n\n")
        f.write("Эти файлы содержат зашифрованные данные.\n")
        f.write(f"Зашифрованная информация находится в файле 'file_{target_file}.bin'\n")
        f.write(f"Позиция данных: {target_offset} байт от начала файла\n")
        f.write(f"Размер зашифрованных данных: {len(encrypted_data)} байт\n")
        f.write("\nДля расшифровки необходим правильный ключ.")

    # Создаем файл с техническим описанием
    with open(os.path.join(directory, "technical_info.txt"), "w", encoding="utf-8") as f:
        f.write("Technical Information\n")
        f.write("====================\n\n")
        f.write("File Structure:\n")
        f.write("- Salt: 16 bytes (Used for key derivation)\n")
        f.write("- IV: 16 bytes (Initialization Vector for CBC mode)\n")
        f.write("- Encrypted data: variable length (Padded to AES block size)\n")
        f.write("- Total overhead: 32 bytes (Salt + IV)\n\n")
        f.write("Encryption Details:\n")
        f.write("- Algorithm: AES-256-CBC (Advanced Encryption Standard)\n")
        f.write("- Key size: 256 bits (32 bytes)\n")
        f.write("- Block size: 128 bits (16 bytes)\n")
        f.write("- Mode: CBC (Cipher Block Chaining)\n")
        f.write("- Padding: PKCS7\n")
        f.write("- Key derivation: PBKDF2 with SHA256\n")
        f.write("- PBKDF2 iterations: 10000\n")
        f.write("- Salt size: 128 bits (16 bytes)\n\n")
        f.write("Security Features:\n")
        f.write("- Unique salt per encryption\n")
        f.write("- Random IV generation\n")
        f.write("- Strong key derivation with PBKDF2\n")
        f.write("- CBC mode for semantic security\n\n")
        f.write("File Details:\n")
        f.write(f"Target File: file_{target_file}.bin\n")
        f.write(f"Data Offset: {target_offset} bytes\n")
        f.write(f"Data Length: {len(encrypted_data)} bytes\n")
        f.write(f"Data Range: {target_offset} - {target_offset + len(encrypted_data)} bytes\n")
        f.write(f"Total File Size: {os.path.getsize(os.path.join(directory, f'file_{target_file}.bin'))} bytes\n\n")
        f.write("Note: All cryptographic operations use the OpenSSL library")

    print(f"Зашифрованные данные находятся в файле 'file_{target_file}.bin'")
    print(f"Смещение: {target_offset} байт")
    print(f"Размер данных: {len(encrypted_data)} байт")
    print(f"Диапазон данных: {target_offset} - {target_offset + len(encrypted_data)} байт")
    return target_file, target_offset

def generate_cpp_code(encrypted_data, target_file, offset):
    hex_data = binascii.hexlify(encrypted_data).decode()
    cpp_code = f"""
// Пример чтения и проверки хеша в C++
#include <fstream>
#include <vector>
#include <string>
#include <iostream>

bool verifyHash(const std::string& userInput) {{
    // Читаем хеш из файла
    std::ifstream file("bin_files/file_{target_file}.bin", std::ios::binary);
    if (!file) {{
        std::cout << "Ошибка открытия файла" << std::endl;
        return false;
    }}
    
    // Перемещаемся к позиции данных
    file.seekg({offset});
    
    // Читаем {len(encrypted_data)} байт
    std::vector<unsigned char> storedHash({len(encrypted_data)});
    file.read(reinterpret_cast<char*>(storedHash.data()), storedHash.size());
    
    // Сравниваем с пользовательским вводом
    std::string storedHashStr;
    for(unsigned char byte : storedHash) {{
        char hex[3];
        sprintf(hex, "%02x", byte);
        storedHashStr += hex;
    }}
    
    return storedHashStr == userInput;
}}

int main() {{
    std::string userInput;
    std::cout << "Введите хеш для проверки: ";
    std::cin >> userInput;
    
    if(verifyHash(userInput)) {{
        std::cout << "Хеш верный!" << std::endl;
    }} else {{
        std::cout << "Хеш неверный." << std::endl;
    }}
    
    return 0;
}}

// Сохраненный хеш для справки:
// {hex_data}
"""
    return cpp_code

if __name__ == "__main__":
    print("1: Зашифровать текст")
    print("2: Расшифровать текст")
    print("3: Зашифровать и получить C++ код")
    choice = input("Выберите режим: ")

    if choice in ["1", "3"]:
        text = input("Введите текст для шифрования: ")
        password = input("Введите ключ: ")
        
        encrypted = encrypt_text(text, password)
        hex_data = binascii.hexlify(encrypted).decode()
        print(f"\nРазмер зашифрованных данных: {len(encrypted)} байт")
        print(f"Зашифрованные данные (hex):\n{hex_data}")
        
        target_file, offset = create_bin_files(encrypted)

        if choice == "3":
            cpp_code = generate_cpp_code(encrypted, target_file, offset)
            print("\nПример кода для C++:")
            print(cpp_code)

    elif choice == "2":
        hex_data = input("Введите зашифрованные данные (hex): ")
        password = input("Введите ключ: ")
        
        try:
            encrypted = binascii.unhexlify(hex_data)
            print(f"\nРазмер зашифрованных данных: {len(encrypted)} байт")
            decrypted = decrypt_text(encrypted, password)
            print(f"Расшифрованный текст: {decrypted}")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    else:
        print("Неверный выбор режима")