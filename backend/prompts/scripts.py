import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment

# Путь к папке с изображениями
image_folder = 'backend/prompts/media/images'

def average_color(image):
    image = image.convert('RGB')
    img_array = np.array(image)
    avg_color = img_array.mean(axis=(0, 1))
    return avg_color

# Чтение изображений из папки
images = []
colors = []
image_paths = []
filenames = []

for filename in os.listdir(image_folder):
    if filename.endswith(('jpg', 'jpeg', 'png')):
        image_path = os.path.join(image_folder, filename)
        image = Image.open(image_path).convert('RGB')  # Ensure images are in RGB mode
        images.append(image)
        colors.append(average_color(image))
        image_paths.append(image_path)
        filenames.append(filename)

# Преобразование списка средних цветов в массив NumPy
colors = np.array(colors)

# Вычисление матрицы расстояний между цветами
dists = squareform(pdist(colors, 'euclidean'))

# Решение задачи упорядочивания изображений
row_ind, col_ind = linear_sum_assignment(dists)

# Упорядочивание изображений по найденному пути
ordered_images = [images[i] for i in col_ind]
ordered_filenames = [filenames[i] for i in col_ind]

# Параметры для сетки
image_width, image_height = ordered_images[0].size
grid_width = 5  # Number of images per row
grid_height = (len(ordered_images) + grid_width - 1) // grid_width

# Создание пустого изображения для сетки
grid_image = Image.new('RGB', (grid_width * image_width, grid_height * image_height))

# Настройка шрифта для заголовков
try:
    font = ImageFont.truetype("arial.ttf", 12)  # Уменьшите размер шрифта
except IOError:
    font = ImageFont.load_default()

# Функция для создания закругленного фона
def create_rounded_rectangle(width, height, radius, color):
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([radius, 0, width - radius, height], fill=255)
    draw.rectangle([0, radius, width, height - radius], fill=255)
    draw.pieslice([0, 0, radius * 2, radius * 2], 180, 270, fill=255)
    draw.pieslice([width - radius * 2, 0, width, radius * 2], 270, 360, fill=255)
    draw.pieslice([0, height - radius * 2, radius * 2, height], 90, 180, fill=255)
    draw.pieslice([width - radius * 2, height - radius * 2, width, height], 0, 90, fill=255)
    rounded_background = Image.new('RGB', (width, height), color)
    rounded_background.putalpha(mask)
    return rounded_background

# Расположение изображений в сетке с заголовками
for idx, img in enumerate(ordered_images):
    row = idx // grid_width
    col = idx % grid_width

    # Создание нового изображения с заголовком на изображении
    new_img = img.copy()
    draw = ImageDraw.Draw(new_img)
    text = ordered_filenames[idx]
    
    # Получение размеров текста
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Настройка фона под текстом
    background_width = image_width // 2  # Фон должен быть половиной ширины изображения
    padding = 5
    text_background_height = text_height + 2 * padding
    text_background = create_rounded_rectangle(background_width, text_background_height, 10, (0, 0, 0))  # Черный фон с закругленными углами
    
    # Пересчитать текстовые размеры с учетом нового фона
    text_x = padding
    text_y = padding

    # Рисовать текст на фоне
    draw_text_background = ImageDraw.Draw(text_background)
    draw_text_background.text((text_x, text_y), text, fill=(255, 255, 255), font=font)  # Белый текст на черном фоне

    # Определение позиции текста на изображении
    text_x = image_width - background_width  # Поместить текст на правой стороне изображения
    text_y = image_height - text_background_height  # Поместить текст в нижней части изображения

    # Убедитесь, что background (фон текста) имеет альфа-канал
    text_background = text_background.convert('RGBA')

    # Вставка черного фона с текстом на изображение
    new_img.paste(text_background, (text_x, text_y), text_background)

    # Вставка нового изображения в сетку
    grid_image.paste(new_img, (col * image_width, row * image_height))