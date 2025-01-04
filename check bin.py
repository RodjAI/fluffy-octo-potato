import os
import struct

def search_pattern_in_bin():
    # Запрашиваем параметры у пользователя
    offset = int(input("Data Offset: ").replace(" bytes", ""))
    size = int(input("Data Length: ").replace(" bytes", ""))
    data_range = input("Data Range: ")
    
    # Получаем текущую директорию
    current_dir = os.getcwd()
    
    # Ищем все .bin файлы
    bin_files = []
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.bin'):
                bin_files.append(os.path.join(root, file))
    
    # Проходим по каждому файлу
    for bin_file in bin_files:
        try:
            with open(bin_file, 'rb') as f:
                # Переходим на указанное смещение
                f.seek(offset)
                # Читаем указанное количество байт
                data = f.read(size)
                
                if data:
                    print(f"\nФайл: {bin_file}")
                    print(f"Данные по смещению {offset}, размер {size} байт:")
                    print(f"Диапазон: {data_range} bytes")
                    print(f"Hex: {data.hex()}")
                    try:
                        # Пробуем декодировать как ASCII
                        print(f"ASCII: {data.decode('ascii', errors='ignore')}")
                    except:
                        pass
                    try:
                        # Пробуем интерпретировать как числа
                        if size == 4:
                            val = struct.unpack('i', data)[0]
                            print(f"Int32: {val}")
                        elif size == 8:
                            val = struct.unpack('q', data)[0]
                            print(f"Int64: {val}")
                    except:
                        pass
                        
        except Exception as e:
            print(f"Ошибка при чтении файла {bin_file}: {str(e)}")

# Пример использования:
search_pattern_in_bin()
