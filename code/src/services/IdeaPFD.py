import json
import os
import tempfile
from io import BytesIO
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import uuid

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Flowable
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

import requests
from PIL import Image as PILImage
import qrcode
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

# Попробуем импортировать PyPDF2 для работы с UTF-8
try:
    from PyPDF2 import PdfReader, PdfWriter
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False
    print("PyPDF2 не установлен. Установите: pip install PyPDF2")

idea_pdf_router = APIRouter(prefix="/idea_pdf")

# Функция для работы с кириллицей в PDF
def setup_pdf_encoding():
    """Регистрация шрифтов, доступных в системе"""
    try:
        # Проверяем, какие шрифты доступны
        available_fonts = []
        
        # Список возможных путей к шрифтам
        font_search_paths = [
            # Windows
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/times.ttf",
            "C:/Windows/Fonts/cour.ttf",  # Courier
            # Linux
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            # Mac
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            # Общие пути (может быть установлен в проект)
            "./fonts/arial.ttf",
            "./fonts/DejaVuSans.ttf",
            "/app/fonts/arial.ttf",  # Для Docker
        ]
        
        for font_path in font_search_paths:
            if os.path.exists(font_path):
                try:
                    font_name = os.path.basename(font_path).split('.')[0]
                    
                    # Регистрируем обычный и жирный варианты
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    
                    # Для шрифтов, у которых есть отдельные файлы для жирного
                    bold_path = font_path.replace('.ttf', '-Bold.ttf').replace('.ttc', 'Bold.ttc')
                    if os.path.exists(bold_path):
                        pdfmetrics.registerFont(TTFont(f'{font_name}-Bold', bold_path))
                    
                    available_fonts.append(font_name)
                    print(f"Найден шрифт: {font_name} по пути {font_path}")
                    
                except Exception as e:
                    print(f"Не удалось загрузить шрифт {font_path}: {e}")
        
        # Если не нашли шрифты, используем стандартные PDF шрифты
        if not available_fonts:
            print("Не найдены системные шрифты, использую стандартные PDF шрифты")
            # Стандартные PDF шрифты (не требуют файлов)
            return 'Helvetica'  # Это стандартный PDF шрифт
        
        # Предпочитаем Arial или DejaVu как наиболее распространенные
        for preferred in ['Arial', 'DejaVuSans', 'LiberationSans', 'Ubuntu', 'FreeSans']:
            if preferred in available_fonts:
                print(f"Использую шрифт: {preferred}")
                return preferred
        
        # Иначе первый найденный
        print(f"Использую первый найденный шрифт: {available_fonts[0]}")
        return available_fonts[0]
        
    except Exception as e:
        print(f"Ошибка при настройке шрифтов: {e}")
        return 'Helvetica'  # Fallback на стандартный PDF шрифт

# Модель для входных данных
class IdeaData(BaseModel):
    full_name: str = Field(..., description="ФИО пользователя")
    photo_url: Optional[str] = Field(None, description="Ссылка на фото пользователя")
    position: str = Field(..., description="Должность")
    department: str = Field(..., description="Отдел")
    subdepartment: Optional[str] = Field(None, description="Подотдел")
    directorate: Optional[str] = Field(None, description="Дирекция")
    idea_title: str = Field(..., description="Название идеи")
    idea_text: str = Field(..., description="Текст идеи")
    idea_number: Optional[str] = Field("000", description="Номер идеи")
    )

class RobustPDFGenerator:
    """Универсальный генератор PDF с гарантированной поддержкой кириллицы"""
    
    def __init__(self, json_data: Dict[str, Any], output_filename: Optional[str] = None):
        """
        Инициализация генератора PDF с данными из JSON
        """
        self.data = json_data
        self.buffer = BytesIO()
        
        # Настраиваем шрифты
        self.font_name = setup_pdf_encoding()
        
        # Размеры страницы A4 в мм
        self.page_width = 210 * mm
        self.page_height = 297 * mm
        
        # Настройки полей
        self.left_margin = 15 * mm
        self.right_margin = 15 * mm
        self.top_margin = 30 * mm
        self.bottom_margin = 20 * mm
        
        # Имя файла для сохранения
        if output_filename:
            self.output_filename = output_filename
        else:
            self.output_filename = self._generate_filename()
    
    def _generate_filename(self) -> str:
        """Генерация имени файла на основе данных"""
        # Безопасное название идеи
        title = self.data.get('idea_title', 'Идея')
        safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
        
        # Номер идеи
        idea_number = str(self.data.get('idea_number', '000')).zfill(3)
        
        # Генерируем имя файла как в примере
        filename = f"Idea_{idea_number}_{safe_title[:50]}.pdf"
        return filename
    
    def _safe_unicode(self, text: str) -> str:
        """Безопасная обработка Unicode текста"""
        if not text:
            return ""
        
        try:
            # Проверяем, что текст можно закодировать в UTF-8
            text.encode('utf-8')
            return text
        except UnicodeEncodeError:
            # Заменяем проблемные символы
            return text.encode('utf-8', 'replace').decode('utf-8')
    
    def download_image(self, url: str) -> Optional[BytesIO]:
        """Скачивание изображения по URL"""
        try:
            if not url:
                return None
                
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BytesIO(response.content)
        except Exception as e:
            print(f"Ошибка загрузки изображения {url}: {e}")
            return None
    
    def create_placeholder_image(self) -> BytesIO:
        """Создание placeholder изображения"""
        img = PILImage.new('RGB', (200, 200), color=(220, 220, 220))
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
    
    def create_circular_image(self, image_stream: BytesIO) -> BytesIO:
        """Создание круглого изображения с обрезкой"""
        try:
            # Открываем изображение
            img = PILImage.open(image_stream)
            
            # Конвертируем в RGB если нужно
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGB')
            
            # Обрезаем до квадрата
            width, height = img.size
            min_dimension = min(width, height)
            left = (width - min_dimension) // 2
            top = (height - min_dimension) // 2
            right = left + min_dimension
            bottom = top + min_dimension
            
            img = img.crop((left, top, right, bottom))
            
            # Масштабируем
            img = img.resize((200, 200), PILImage.Resampling.LANCZOS)
            
            # Сохраняем в буфер
            buffer = BytesIO()
            img.save(buffer, format='PNG', quality=95)
            buffer.seek(0)
            
            return buffer
        except Exception as e:
            print(f"Ошибка обработки изображения: {e}")
            return image_stream
    
    def create_qr_code_image(self, data: str, size: int = 200) -> BytesIO:
        """Создание QR-кода"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img = qr_img.convert('RGB')
            
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            buffer.seek(0)
            return buffer
        except Exception as e:
            print(f"Ошибка создания QR-кода: {e}")
            placeholder = PILImage.new('RGB', (size, size), color='white')
            buffer = BytesIO()
            placeholder.save(buffer, format='PNG')
            buffer.seek(0)
            return buffer
    
    def generate_pdf_with_canvas(self) -> BytesIO:
        """Генерация PDF с использованием canvas напрямую (наиболее надежный способ)"""
        try:
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            
            # Устанавливаем UTF-8 кодировку для canvas
            c._doc.info.producer = "PDF Generator (UTF-8)"
            
            width, height = A4
            
            # Заголовок
            c.setFont(self.font_name, 12)
            header_text = self._safe_unicode("Интранет: Есть идея!")
            c.drawRightString(width - 15*mm, height - 20*mm, header_text)
            c.setLineWidth(0.4)
            c.line(0, height - 24*mm, width, height - 24*mm)
            
            # Фото пользователя (центрируем)
            photo_stream = None
            # if self.data.get('photo_url'):
            #     photo_stream = self.download_image(self.data['photo_url'])
            
            if not photo_stream:
                photo_stream = self.create_placeholder_image()
            
            if photo_stream:
                try:
                    # Конвертируем фото
                    img = PILImage.open(photo_stream)
                    img_buffer = BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    
                    # Рисуем фото
                    photo_width = 60 * mm
                    photo_height = 60 * mm
                    photo_x = (width - photo_width) / 2
                    photo_y = height - 90 * mm
                    
                    c.drawImage(ImageReader(img_buffer), photo_x, photo_y, 
                               width=photo_width, height=photo_height, 
                               mask='auto')
                except Exception as e:
                    print(f"Ошибка при добавлении фото: {e}")
            
            # ФИО пользователя
            c.setFont(self.font_name + '-Bold' if self.font_name == 'Helvetica' else self.font_name, 10)
            full_name = self._safe_unicode(self.data.get('full_name', ''))
            text_width = c.stringWidth(full_name, self.font_name, 10)
            c.drawString((width - text_width) / 2, height - 155*mm, full_name)
            
            # Должность и отделы
            c.setFont(self.font_name, 9)
            position = self._safe_unicode(self.data.get('position', ''))
            department = self._safe_unicode(self.data.get('department', ''))
            subdepartment = self._safe_unicode(self.data.get('subdepartment', ''))
            directorate = self._safe_unicode(self.data.get('directorate', ''))
            
            # Формируем иерархию
            dept_parts = []
            if directorate:
                dept_parts.append(directorate)
            if subdepartment:
                dept_parts.append(subdepartment)
            if department:
                dept_parts.append(department)
            dept_parts.append('НПО ЭМК')
            
            # Рисуем отделы
            y_pos = height - 165*mm
            for part in dept_parts:
                if part.strip():
                    text_width = c.stringWidth(part, self.font_name, 9)
                    c.drawString((width - text_width) / 2, y_pos, part)
                    y_pos -= 5*mm
            
            # Должность жирным
            c.setFont(self.font_name + '-Bold' if self.font_name == 'Helvetica' else self.font_name, 9)
            text_width = c.stringWidth(position, self.font_name, 9)
            c.drawString((width - text_width) / 2, y_pos, position)
            
            # Название идеи с номером
            y_pos -= 15*mm
            c.setFont(self.font_name, 10)
            idea_number = str(self.data.get('idea_number', '000')).zfill(3)
            idea_title = self._safe_unicode(self.data.get('idea_title', ''))
            title = self._safe_unicode(f"№{idea_number}. {idea_title}")
            
            # Разбиваем заголовок если длинный
            max_title_width = width - 30*mm
            title_width = c.stringWidth(title, self.font_name, 10)
            
            if title_width > max_title_width:
                # Простой перенос
                words = title.split()
                lines = []
                current_line = []
                
                for word in words:
                    current_line.append(word)
                    test_line = ' '.join(current_line)
                    test_width = c.stringWidth(test_line, self.font_name, 10)
                    
                    if test_width > max_title_width:
                        if len(current_line) == 1:
                            lines.append(test_line)
                            current_line = []
                        else:
                            current_line.pop()
                            lines.append(' '.join(current_line))
                            current_line = [word]
                
                if current_line:
                    lines.append(' '.join(current_line))
                
                for line in lines:
                    text_width = c.stringWidth(line, self.font_name, 10)
                    c.drawString((width - text_width) / 2, y_pos, line)
                    y_pos -= 5*mm
            else:
                text_width = c.stringWidth(title, self.font_name, 10)
                c.drawString((width - text_width) / 2, y_pos, title)
                y_pos -= 5*mm
            
            # Текст идеи
            y_pos -= 10*mm
            c.setFont(self.font_name, 9)
            idea_text = self._safe_unicode(self.data.get('idea_text', ''))
            
            # Перенос текста
            paragraphs = idea_text.split('\n')
            max_text_width = width - 30*mm
            
            for paragraph in paragraphs:
                if paragraph.strip():
                    words = paragraph.split()
                    current_line = []
                    
                    for word in words:
                        current_line.append(word)
                        test_line = ' '.join(current_line)
                        test_width = c.stringWidth(test_line, self.font_name, 9)
                        
                        if test_width > max_text_width:
                            if len(current_line) == 1:
                                # Слово слишком длинное, рисуем как есть
                                c.drawString(15*mm, y_pos, test_line)
                                y_pos -= 4*mm
                                current_line = []
                            else:
                                # Рисуем предыдущую строку
                                current_line.pop()
                                line_text = ' '.join(current_line)
                                c.drawString(15*mm, y_pos, line_text)
                                y_pos -= 4*mm
                                current_line = [word]
                        
                        # Проверяем место на странице
                        if y_pos < 50*mm:
                            c.showPage()
                            y_pos = height - 30*mm
                            c.setFont(self.font_name, 9)
                    
                    # Рисуем остаток параграфа
                    if current_line:
                        line_text = ' '.join(current_line)
                        c.drawString(15*mm, y_pos, line_text)
                        y_pos -= 4*mm
                    
                    # Отступ между абзацами
                    y_pos -= 2*mm
            
            # # QR-код
            # qr_url = self.data.get('qr_code_url', 'https://portal.emk.ru/intranet/editor/feedback/')
            # try:
            #     qr_buffer = self.create_qr_code_image(qr_url, size=200)
            #     qr_img = PILImage.open(qr_buffer)
            #     qr_img_buffer = BytesIO()
            #     qr_img.save(qr_img_buffer, format='PNG')
            #     qr_img_buffer.seek(0)
                
            #     qr_size = 30 * mm
            #     qr_x = 15 * mm
            #     qr_y = 20 * mm
                
            #     c.drawImage(ImageReader(qr_img_buffer), qr_x, qr_y, 
            #                width=qr_size, height=qr_size, mask='auto')
            # except Exception as e:
            #     print(f"Ошибка при добавлении QR-кода: {e}")
            
            # Подвал
            c.setLineWidth(0.4)
            c.line(0, 10*mm, width, 10*mm)
            c.setFont(self.font_name, 8)
            footer_text = self._safe_unicode("Страница 1/1")
            text_width = c.stringWidth(footer_text, self.font_name, 8)
            c.drawString((width - text_width) / 2, 6*mm, footer_text)
            
            c.save()
            buffer.seek(0)
            
            # Если есть PyPDF2, улучшаем кодировку
            if HAS_PYPDF2:
                try:
                    buffer = self._improve_pdf_encoding(buffer)
                except Exception as e:
                    print(f"Не удалось улучшить кодировку PDF: {e}")
            
            return buffer
            
        except Exception as e:
            print(f"Критическая ошибка при генерации PDF: {e}")
            raise
    
    def _improve_pdf_encoding(self, pdf_buffer: BytesIO) -> BytesIO:
        """Улучшение кодировки PDF с помощью PyPDF2"""
        if not HAS_PYPDF2:
            return pdf_buffer
        
        try:
            # Читаем PDF
            pdf_buffer.seek(0)
            reader = PdfReader(pdf_buffer)
            writer = PdfWriter()
            
            # Копируем все страницы
            for page in reader.pages:
                writer.add_page(page)
            
            # Добавляем метаданные UTF-8
            writer.add_metadata({
                '/Producer': 'PDF Generator with UTF-8',
                '/Title': self._safe_unicode(self.data.get('idea_title', '')),
                '/Author': self._safe_unicode(self.data.get('full_name', '')),
                '/Creator': 'Python PDF Generator',
                '/CreationDate': datetime.now().strftime("D:%Y%m%d%H%M%S"),
            })
            
            # Сохраняем в новый буфер
            output_buffer = BytesIO()
            writer.write(output_buffer)
            output_buffer.seek(0)
            
            return output_buffer
            
        except Exception as e:
            print(f"Ошибка при улучшении PDF: {e}")
            pdf_buffer.seek(0)
            return pdf_buffer
    
    def generate_pdf(self) -> BytesIO:
        """Основной метод генерации PDF"""
        return self.generate_pdf_with_canvas()
    
    def save_to_file(self, filename: Optional[str] = None, 
                    directory: Optional[str] = None) -> str:
        """
        Сохранение PDF в файл
        """
        try:
            # Определяем директорию
            if directory is None:
                directory = tempfile.gettempdir()
            
            # Создаем директорию если её нет
            os.makedirs(directory, exist_ok=True)
            
            # Определяем имя файла
            if filename is None:
                filename = self.output_filename
            
            # Полный путь к файлу
            filepath = os.path.join(directory, filename)
            
            # Генерируем PDF
            pdf_buffer = self.generate_pdf()
            
            # Сохраняем в файл
            with open(filepath, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            
            print(f"PDF сохранен: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            raise
    
    def get_pdf_bytes(self) -> bytes:
        """Получение PDF как байтов"""
        pdf_buffer = self.generate_pdf()
        return pdf_buffer.getvalue()
    
    def get_pdf_stream(self) -> BytesIO:
        """Получение PDF как BytesIO потока"""
        return self.generate_pdf()

# Эндпоинты API
@idea_pdf_router.post("/generate-pdf", response_class=Response)
async def generate_pdf_endpoint(data: IdeaData):
    """
    Генерация PDF документа на основе переданных данных
    """
    try:
        # Конвертируем Pydantic модель в словарь
        json_data = data.dict()
        
        # Создаем генератор PDF
        generator = RobustPDFGenerator(json_data)
        
        # Получаем PDF как поток
        pdf_stream = generator.get_pdf_stream()
        pdf_content = pdf_stream.getvalue()
        
        # Формируем имя файла
        filename = generator.output_filename
        
        # Возвращаем PDF как файл
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf",
                "Content-Length": str(len(pdf_content))
            }
        )
    
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка генерации PDF: {error_msg}")
        # Более информативное сообщение об ошибке
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {str(e)}")


@idea_pdf_router.post("/generate-pdf-save")
async def generate_pdf_and_save(data: IdeaData, 
                               directory: Optional[str] = None):
    """
    Генерация PDF документа и сохранение его в файл
    """
    try:
        # Конвертируем Pydantic модель в словарь
        json_data = data.dict()
        
        # Создаем генератор PDF
        generator = RobustPDFGenerator(json_data)
        
        # Сохраняем в файл
        filepath = generator.save_to_file(directory=directory)
        
        # Возвращаем путь к файлу
        return {
            "status": "success",
            "message": "PDF успешно сгенерирован",
            "filename": os.path.basename(filepath),
            "filepath": filepath,
            "size": os.path.getsize(filepath),
            "download_url": f"/idea_pdf/download-pdf/{os.path.basename(filepath)}"
        }
    
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка генерации PDF: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {error_msg}")


@idea_pdf_router.get("/download-pdf/{filename}")
async def download_pdf(filename: str, directory: Optional[str] = None):
    """
    Скачивание ранее сгенерированного PDF файла
    """
    try:
        if directory is None:
            directory = tempfile.gettempdir()
        
        filepath = os.path.join(directory, filename)
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Файл не найден")
        
        # Получаем размер файла
        file_size = os.path.getsize(filepath)
        
        # Открываем файл для чтения в бинарном режиме
        def iterfile():
            with open(filepath, "rb") as f:
                yield from f
        
        return StreamingResponse(
            iterfile(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(file_size)
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка при загрузке файла: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке файла: {error_msg}")


@idea_pdf_router.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# Простой тестовый эндпоинт
@idea_pdf_router.post("/test")
async def test_pdf_generation():
    """Тестирование генерации PDF с русским текстом"""
    test_data = {
        "full_name": "Иванов Иван Иванович",
        "photo_url": "https://via.placeholder.com/200",
        "position": "Инженер-разработчик",
        "department": "Отдел разработки",
        "subdepartment": "Группа веб-разработки",
        "directorate": "Дирекция информационных технологий",
        "idea_title": "Тестовая идея на русском языке",
        "idea_text": """Это тестовый текст на русском языке для проверки генерации PDF.

Вторая строка текста.
Третья строка с русскими символами: привет, мир!

Теперь проверим длинный текст, который должен переноситься на новую строку автоматически при достижении конца строки на странице PDF документа.""",
        "idea_number": "999"
    }
    
    try:
        generator = RobustPDFGenerator(test_data)
        pdf_stream = generator.generate()
        pdf_content = pdf_stream.getvalue()
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=test_russian.pdf",
                "Content-Type": "application/pdf"
            }
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Тестовая ошибка: {str(e)}")


def create_pdf_from_json(json_data: Dict[str, Any], 
                        output_file: Optional[str] = None,
                        directory: Optional[str] = None) -> str:
    """
    Функция для использования вне FastAPI
    """
    generator = RobustPDFGenerator(json_data, output_file)
    return generator.save_to_file(directory=directory)


# Тестовый код при прямом запуске
if __name__ == "__main__":
    print("=" * 60)
    print("Тестирование генерации PDF с русским текстом")
    print("=" * 60)
    
    # Тестовые данные
    test_data = {
        "full_name": "Высоцкая Мария Сергеевна",
        "photo_url": "https://via.placeholder.com/200",
        "position": "Специалист по продажам, подбору оборудования и клиентскому сервису",
        "department": "Коммерческая дирекция",
        "subdepartment": "Дирекция по продажам",
        "directorate": "",
        "idea_title": "Краны с кламповым присоединением",
        "idea_text": """В течении года от химических предприятий поступает все больше запросов на краны шаровые с кламповым присоединением, в основном материал корпуса- нержавеющая сталь, PN до 1,6Мпа, DN 20-50. Со слов заказчиков в РФ изготовителей подобных изделий нет, пользуются импортом. Основным преимуществом с их слов, является высокая скорость монтажа/демонтажа. Предлагаю провести аналитику данного рынка, изучить потребности всех КО, работающих с хим.предприятиями. В случае выявление потребностей, проработать возможность изготовление кранов САЗ с данным присоединением.""",
        "idea_number": "301"
    }
    
    try:
        # Создаем генератор
        generator = RobustPDFGenerator(test_data)
        
        # Тестируем сохранение
        filepath = generator.save_to_file(directory="./test_output")
        print(f"✓ PDF успешно создан: {filepath}")
        
        # Проверяем размер файла
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✓ Размер файла: {file_size} байт")
        
        print("\n✓ Тестирование завершено успешно!")
        
    except Exception as e:
        print(f"✗ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()