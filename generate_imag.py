from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
from path import logos_khl, logos_nhl, name_template_khl, name_template_nhl, name_font_path
from points import points_less_six_khl, points_more_six_khl, points_less_six_nhl, points_more_six_nhl,\
    result_points_less_six_khl, result_points_more_six_khl, result_points_less_six_nhl, result_points_more_six_nhl


def image_khl(teams, results):
    # Формируем ссылку на шрифт
    font_path = os.path.join('data', 'font', name_font_path)

    # Формируем ссылку на фон
    template_path_khl = os.path.join('data', 'background', name_template_khl)

    # Открыть шаблон изображения
    template_image_khl = Image.open(template_path_khl)

    # Создание объекта ImageDraw для рисования текста на изображении-шаблоне
    draw_khl = ImageDraw.Draw(template_image_khl)

    # Размеры для масштабирования логотипов
    logo_size = (100, 100)

    # Выбор списка координат в зависимости от количества команд
    if len(teams) < 12:
        points = points_less_six_khl
    else:
        points = points_more_six_khl

    # Размещение логотипов на основе-шаблоне
    for team, point in zip(teams, points):
        lowercase_team = team.lower()  # Приведение имени команды к нижнему регистру
        name_logo_path = logos_khl.get(lowercase_team)
        if not name_logo_path:
            raise ValueError("Логотип для команды не найден")
        else:
            # Определяем путь к изображению относительно текущего файла
            logo_path = os.path.join('data', 'logo_khl', name_logo_path)
            if logo_path:
                logo_image = Image.open(logo_path)
                logo_image.thumbnail(logo_size)
                template_image_khl.paste(logo_image, (point["x"], point["y"]), logo_image)

    if len(results) < 6:
        result_points = result_points_less_six_khl
    else:
        result_points = result_points_more_six_khl

    # Установка времени
    font_data = ImageFont.truetype(font_path, size=25)
    current_date = datetime.now().date().strftime("%d-%m-%Y")
    draw_khl.text((480, 208), str(current_date), fill="black", font=font_data)

    # Инициализация переменной result_index
    result_index = 0

    # Размеры шрифтов для разных типов результатов
    font_size_number = 50
    font_size_abc = 20

    for result, point in zip(results, result_points):
        if " " in result:
            score, result_type = result.split(" ")  # Разделение строки по пробелу
            # Установка нужного размера шрифта для score и result_type
            score_font_size = font_size_number
            result_type_font_size = font_size_abc
        else:
            score = result  # score остается без изменений
            result_type = ""  # result_type устанавливается пустой строкой
            # Установка нужного размера шрифта для score и result_type
            score_font_size = font_size_number
            result_type_font_size = font_size_number

        # Установка нужного шрифта, размера и цвета для чисел
        draw_khl.text((point["x"], point["y"]), score, fill="#dda419",
                      font=ImageFont.truetype(font_path, size=score_font_size))
        # Установка нужного шрифта, размера и цвета для result_type
        draw_khl.text((point["x"] + 80, point["y"] + 32), result_type, fill="#dda419",
                      font=ImageFont.truetype(font_path, size=result_type_font_size))

        result_index += 1  # Увеличение индекса для списка result_points

    # Путь для финальной картинки
    results_path = os.path.join('data', 'results', 'game_result_khl.png')

    print("Результаты КХЛ успешно сформированны")
    template_image_khl.save(results_path)

    # Получаем абсолютный путь к файлу изображения
    # image_path = os.path.abspath("game_result_khl.png")

    # Возвращаем относительный путь к файлу изображения относительно директории скрипта
    return results_path


def image_nhl(teams, results):
    # Формируем ссылку на шрифт
    font_path = os.path.join('data', 'font', name_font_path)

    # Формируем ссылку на фон
    template_path_nhl = os.path.join('data', 'background', name_template_nhl)

    # Открыть шаблон изображения
    template_image_nhl = Image.open(template_path_nhl)

    # Создание объекта ImageDraw для рисования текста на изображении-шаблоне
    draw_nhl = ImageDraw.Draw(template_image_nhl)

    # Размеры для масштабирования логотипов
    logo_size = (100, 100)

    # Выбор списка координат в зависимости от количества команд
    if len(teams) < 12:
        points = points_less_six_nhl
    else:
        points = points_more_six_nhl

    # Размещение логотипов на основе-шаблоне
    for team, point in zip(teams, points):
        lowercase_team = team.lower()  # Приведение имени команды к нижнему регистру
        name_logo_path = logos_nhl.get(lowercase_team)
        if not name_logo_path:
            raise ValueError("Логотип для команды не найден")
        else:
            # Определяем путь к изображению относительно текущего файла
            logo_path = os.path.join('data', 'logo_nhl', name_logo_path)
            if logo_path:
                logo_image = Image.open(logo_path)
                logo_image.thumbnail(logo_size)
                template_image_nhl.paste(logo_image, (point["x"], point["y"]), logo_image)

    # Проверка на количество переданных числовых результатов игр и выбор координат
    if len(results) < 6:
        result_points = result_points_less_six_nhl
    else:
        result_points = result_points_more_six_nhl

    # Установка времени
    font_data = ImageFont.truetype(font_path, size=25)
    current_date = datetime.now().date().strftime("%d-%m-%Y")
    draw_nhl.text((480, 208), str(current_date), fill="black", font=font_data)

    # Инициализация переменной result_index
    result_index = 0

    # Размеры шрифтов для разных типов результатов
    font_size_number = 50
    font_size_abc = 20

    for result, point in zip(results, result_points):
        if " " in result:
            score, result_type = result.split(" ")  # Разделение строки по пробелу
            # Установка нужного размера шрифта для score и result_type
            score_font_size = font_size_number
            result_type_font_size = font_size_abc
        else:
            score = result  # score остается без изменений
            result_type = ""  # result_type устанавливается пустой строкой
            # Установка нужного размера шрифта для score и result_type
            score_font_size = font_size_number
            result_type_font_size = font_size_number

        # Установка нужного шрифта, размера и цвета для чисел
        draw_nhl.text((point["x"], point["y"]), score, fill="#dda419",
                      font=ImageFont.truetype(font_path, size=score_font_size))
        # Установка нужного шрифта, размера и цвета для result_type
        draw_nhl.text((point["x"] + 80, point["y"] + 32), result_type, fill="#dda419",
                      font=ImageFont.truetype(font_path, size=result_type_font_size))

        result_index += 1  # Увеличение индекса для списка result_points

    # Путь для финальной картинки
    results_path = os.path.join('data', 'results', 'game_result_nhl.png')

    # Сохранение картинки
    print("Результаты НХЛ успешно сформированны")
    template_image_nhl.save(results_path)

    # Получаем абсолютный путь к файлу изображения
    # image_path = os.path.abspath("game_result_nhl.png")

    # Возвращаем относительный путь к файлу изображения относительно директории скрипта
    return results_path