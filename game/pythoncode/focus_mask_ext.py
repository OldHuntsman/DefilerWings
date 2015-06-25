# coding=utf-8

import renpy.exports as renpy

import pygame
import struct
import re

# Путь к файлу из которого будем грузить координаты во время игры.
COORDINATES_FILE_PATH = "img/map/coordinates.bin"

# Определяет насколько уменьшить исходные изображения. Их данные в полном размере нам не нужны.
# Чем меньше число (но не менее 1), тем выше точность определения нажатия.
RESOLUTION_DIVIDER = 3

# Regexp при помощи которого будем делать выборку нужных изображений для последующей генерации данных.
REGEXP_FILTER_BUTTONS = re.compile('img/map/button_.*_idle.png')
    
# Все бинарные форматы принудительно используют big-endian на всех платформах.    
# Это необходимо для переносимости файла с координатами.
    
# Бинарный формат для размера пути кнопки.
STRUCT_IMAGE_PATH_LEN = '> H'
STRUCT_IMAGE_PATH_LEN_SIZE = struct.calcsize(STRUCT_IMAGE_PATH_LEN)

# Бинарный формат для пути кнопки. Количество символов в пути подставляется позже.
STRUCT_IMAGE_PATH = '> %ds'

# Бинарный формат для количества найденных координат в файле.
STRUCT_COORDINATES_COUNT = '> L'
STRUCT_COORDINATES_COUNT_SIZE = struct.calcsize(STRUCT_COORDINATES_COUNT)

# Бинарный формат для одной координаты.
STRUCT_COORDINATE = '> HH'
STRUCT_COORDINATE_SIZE = struct.calcsize(STRUCT_COORDINATE)
    
def create_focus_mask_data(output_path):    
    buttons_list = filter(REGEXP_FILTER_BUTTONS.match, renpy.list_files())

    buttons_coordinates = extract_coordinates(buttons_list)
                    
    write_coordinates(buttons_coordinates, output_path)
     
def get_shrinked_surface(button_image_path):
    button_image_file = renpy.file(button_image_path)
    button_surface = pygame.image.load(button_image_file, button_image_path)
    button_size = button_surface.get_size()
    return pygame.transform.scale(button_surface, (button_size[0]/RESOLUTION_DIVIDER, button_size[1]/RESOLUTION_DIVIDER))    
              
def extract_coordinates(buttons_list):       
    buttons_coordinates = {}
           
    for button_image_path in buttons_list:
        button_surface = get_shrinked_surface(button_image_path)
        button_size = button_surface.get_size()            
        
        # Фильтрация всех точек изображения с alpha > 0.
        coordinates = filter(lambda (x, y): button_surface.get_at((x, y)).a > 0, [(x, y) for y in range(button_size[1]) for x in range(button_size[0])])
        
        buttons_coordinates[button_image_path] = coordinates    
        
    return buttons_coordinates   
        
# Функция записывает данные координат в бинарном формате. Таким образом мы получим хорошую компактность хранения и скорость загрузки.         
def write_coordinates(buttons_coordinates, output_path):     
    output_file = open(output_path, "wb")
    
    for button_image_path, coordinates_set in buttons_coordinates.iteritems():
        # Несмотря на то, что в пути у нас только латинские символы для надёжности закодируем.
        button_image_path_encoded = button_image_path.encode('utf-8')
        button_image_path_encoded_len = len(button_image_path_encoded)
        
        # Записываем длину строки в которой хранится путь к файлу.
        output_file.write(struct.pack(STRUCT_IMAGE_PATH_LEN, button_image_path_encoded_len))
        
        # Записываем строку в которой хранится путь к файлу.
        output_file.write(struct.pack(STRUCT_IMAGE_PATH % button_image_path_encoded_len, button_image_path_encoded))
        
        # Записываем количество координат.
        output_file.write(struct.pack(STRUCT_COORDINATES_COUNT, len(coordinates_set)))
        
        # Записываем координаты.
        for coordinate in buttons_coordinates[button_image_path]:
            output_file.write((struct.pack(STRUCT_COORDINATE, coordinate[0], coordinate[1])))
            
    output_file.close()             
         
def load_focus_mask_data():    
    coordinates_dict = {}

    coordinates_file = renpy.file(COORDINATES_FILE_PATH)
    coordinates_buffer = coordinates_file.read()
    coordinates_file.close()

    # Положение в буфере, начиная с которого читаем данные. Придётся двигать вручную.
    offset = 0

    while offset < len(coordinates_buffer):
        # Читаем длину строки в которой хранится путь к файлу.
        button_image_path_len = struct.unpack_from(STRUCT_IMAGE_PATH_LEN, coordinates_buffer, offset)[0]
        offset += STRUCT_IMAGE_PATH_LEN_SIZE

        # Читаем путь к файлу.
        button_image_path = struct.unpack_from(STRUCT_IMAGE_PATH % button_image_path_len, coordinates_buffer, offset)[0].decode('utf-8')
        offset += button_image_path_len

        coordinates_set = set()
        coordinates_dict[button_image_path] = coordinates_set

        # Читаем количество координат.
        coordinates_count = struct.unpack_from(STRUCT_COORDINATES_COUNT, coordinates_buffer, offset)[0]
        offset += STRUCT_COORDINATES_COUNT_SIZE

        # Читаем все координаты.
        for coordinate_index in range(0, coordinates_count):
            coordinates = struct.unpack_from(STRUCT_COORDINATE, coordinates_buffer, offset)
            offset += STRUCT_COORDINATE_SIZE

            coordinates_set.add(coordinates)

    FocusMaskCallable.coordinates_dict = coordinates_dict        
        
class FocusMaskCallable:
    
    def __init__(self, target):
        self.button_image_path = "img/map/button_%s_idle.png" % target
        
    def __call__(self, x, y):
        coordinates = FocusMaskCallable.coordinates_dict[self.button_image_path]
        return (x // RESOLUTION_DIVIDER, y // RESOLUTION_DIVIDER) in coordinates