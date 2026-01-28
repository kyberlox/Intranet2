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
from reportlab.lib.colors import black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Flowable
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.graphics.renderPDF import draw
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import requests
from PIL import Image as PILImage
import qrcode
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

idea_pdf_router = APIRouter(prefix="/idea_pdf")

# Загрузка шрифтов для поддержки кириллицы
def register_fonts():
    """Регистрация шрифтов для поддержки кириллицы"""
    try:
        # Попробуем загрузить DejaVu Sans (обычно есть в системах Linux)
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans.ttf",
            "C:/Windows/Fonts/arial.ttf",  # Windows
            "C:/Windows/Fonts/times.ttf",  # Windows
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
                    print(f"Шрифт зарегистрирован: {font_path}")
                    return 'DejaVuSans'
                except:
                    continue
        
        # Если не нашли DejaVu, используем Helvetica с кодировкой
        print("Используем стандартный шрифт Helvetica")
        return 'Helvetica'
        
    except Exception as e:
        print(f"Ошибка при регистрации шрифтов: {e}")
        return 'Helvetica'

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
    qr_code_url: Optional[str] = Field(
        "https://portal.emk.ru/intranet/editor/feedback/",
        description="URL для QR-кода"
    )

class PDFGenerator:
    def __init__(self, json_data: Dict[str, Any], output_filename: Optional[str] = None):
        """
        Инициализация генератора PDF с данными из JSON
        """
        self.data = json_data
        self.buffer = BytesIO()
        
        # Регистрируем шрифты
        self.font_name = register_fonts()
        
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
        filename = f"Идея_{idea_number}_{safe_title[:50]}.pdf"
        return filename
    
    def _safe_text(self, text: str) -> str:
        """Безопасное преобразование текста для PDF"""
        if not text:
            return ""
        
        # Заменяем специальные символы HTML
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        
        # Убедимся, что текст в правильной кодировке
        try:
            text.encode('utf-8')
            return text
        except:
            # Если есть проблемы с кодировкой, удаляем не-ASCII символы
            return text.encode('ascii', 'ignore').decode('ascii')
    
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
        """Создание QR-кода с использованием библиотеки qrcode"""
        try:
            # Создаем QR-код
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Создаем изображение
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Конвертируем в RGB
            qr_img = qr_img.convert('RGB')
            
            # Сохраняем в буфер
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            buffer.seek(0)
            
            return buffer
        except Exception as e:
            print(f"Ошибка создания QR-кода: {e}")
            # Создаем placeholder для QR-кода
            placeholder = PILImage.new('RGB', (size, size), color='white')
            buffer = BytesIO()
            placeholder.save(buffer, format='PNG')
            buffer.seek(0)
            return buffer
    
    def draw_header(self, canvas_obj: canvas.Canvas):
        """Отрисовка заголовка страницы"""
        # Заголовок справа
        canvas_obj.setFont(self.font_name, 12)
        canvas_obj.setFillColor(black)
        
        # Позиция как в оригинале
        title_y = self.page_height - 20 * mm
        title_x = self.page_width - 15 * mm
        
        # Безопасный текст для заголовка
        header_text = "Интранет: Есть идея!"
        canvas_obj.drawRightString(title_x, title_y, header_text)
        
        # Линия под заголовком
        canvas_obj.setLineWidth(0.4)
        line_y = title_y - 4 * mm
        canvas_obj.line(0, line_y, self.page_width, line_y)
    
    def draw_footer(self, canvas_obj: canvas.Canvas, page_num: int, total_pages: int):
        """Отрисовка подвала страницы"""
        # Линия над номером страницы
        line_y = 10 * mm
        canvas_obj.setLineWidth(0.4)
        canvas_obj.line(0, line_y, self.page_width, line_y)
        
        # Номер страницы по центру
        canvas_obj.setFont(self.font_name, 8)
        footer_y = 6 * mm
        footer_text = f"Страница {page_num}/{total_pages}"
        canvas_obj.drawCentredString(self.page_width / 2, footer_y, footer_text)
    
    def generate_pdf(self) -> BytesIO:
        """Генерация PDF документа"""
        try:
            # Создаем буфер для PDF
            pdf_buffer = BytesIO()
            
            # Создаем документ с UTF-8 кодировкой
            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=A4,
                rightMargin=self.right_margin,
                leftMargin=self.left_margin,
                topMargin=self.top_margin,
                bottomMargin=self.bottom_margin,
                encoding='utf-8'  # Важно для поддержки кириллицы
            )
            
            # Создаем стили с правильным шрифтом
            styles = getSampleStyleSheet()
            
            # Переопределяем стиль Normal для использования нашего шрифта
            normal_style = styles['Normal']
            normal_style.fontName = self.font_name
            normal_style.encoding = 'utf-8'
            
            # Создаем элементы для документа
            story = []
            
            # Фото пользователя
            photo_stream = None
            if self.data.get('photo_url'):
                photo_stream = self.download_image(self.data['photo_url'])
            
            if not photo_stream:
                photo_stream = self.create_placeholder_image()
            
            if photo_stream:
                try:
                    circular_photo = self.create_circular_image(photo_stream)
                    user_photo = RLImage(circular_photo, width=60*mm, height=60*mm)
                    user_photo.hAlign = 'CENTER'
                    story.append(user_photo)
                    story.append(Spacer(1, 10*mm))
                except Exception as e:
                    print(f"Ошибка при добавлении фото: {e}")
                    story.append(Spacer(1, 70*mm))
            
            # ФИО пользователя
            full_name = self._safe_text(self.data.get('full_name', ''))
            name_style = ParagraphStyle(
                'NameStyle',
                parent=styles['Normal'],
                fontName=self.font_name + '-Bold' if self.font_name == 'Helvetica' else self.font_name,
                fontSize=10,
                alignment=TA_CENTER,
                spaceAfter=5*mm,
                encoding='utf-8'
            )
            story.append(Paragraph(full_name, name_style))
            
            # Должность и отделы
            position = self._safe_text(self.data.get('position', ''))
            department = self._safe_text(self.data.get('department', ''))
            subdepartment = self._safe_text(self.data.get('subdepartment', ''))
            directorate = self._safe_text(self.data.get('directorate', ''))
            
            # Формируем иерархию как в оригинале
            dept_parts = []
            if directorate:
                dept_parts.append(directorate)
            if subdepartment:
                dept_parts.append(subdepartment)
            if department:
                dept_parts.append(department)
            dept_parts.append('НПО ЭМК')
            
            # HTML-like строка
            dept_html = f"<b>{position}</b><br/>" + "<br/>".join(dept_parts)
            
            dept_style = ParagraphStyle(
                'DeptStyle',
                parent=styles['Normal'],
                fontName=self.font_name,
                fontSize=9,
                alignment=TA_CENTER,
                spaceAfter=20*mm,
                encoding='utf-8'
            )
            story.append(Paragraph(dept_html, dept_style))
            
            # Название идеи с номером
            idea_number = str(self.data.get('idea_number', '000')).zfill(3)
            idea_title = self._safe_text(self.data.get('idea_title', ''))
            title_text = f"№{idea_number}. {idea_title}"
            
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading2'],
                fontName=self.font_name,
                fontSize=10,
                alignment=TA_CENTER,
                textColor=black,
                spaceBefore=0,
                spaceAfter=40,
                leading=14,
                encoding='utf-8'
            )
            story.append(Paragraph(title_text, title_style))
            
            # Текст идеи
            idea_text = self._safe_text(self.data.get('idea_text', '')).replace('\n', '<br/>')
            
            text_style = ParagraphStyle(
                'TextStyle',
                parent=styles['Normal'],
                fontName=self.font_name,
                fontSize=9,
                alignment=TA_JUSTIFY,
                leading=12,
                firstLineIndent=20,
                encoding='utf-8'
            )
            
            story.append(Paragraph(idea_text, text_style))
            
            # QR-код
            story.append(Spacer(1, 20*mm))
            
            qr_url = self.data.get('qr_code_url', 'https://portal.emk.ru/intranet/editor/feedback/')
            try:
                # Создаем QR-код как изображение
                qr_buffer = self.create_qr_code_image(qr_url, size=200)
                qr_image = RLImage(qr_buffer, width=30*mm, height=30*mm)
                qr_image.hAlign = 'LEFT'
                story.append(qr_image)
            except Exception as e:
                print(f"Ошибка при создании QR-кода: {e}")
                # Добавляем placeholder
                story.append(Spacer(1, 30*mm))
            
            # Собираем документ
            doc.build(
                story,
                onFirstPage=self._add_header_footer,
                onLaterPages=self._add_header_footer
            )
            
            pdf_buffer.seek(0)
            return pdf_buffer
            
        except Exception as e:
            print(f"Критическая ошибка при генерации PDF: {e}")
            raise
    
    def _add_header_footer(self, canvas_obj: canvas.Canvas, doc: SimpleDocTemplate):
        """Добавление header и footer на каждую страницу"""
        try:
            self.draw_header(canvas_obj)
            self.draw_footer(canvas_obj, canvas_obj.getPageNumber(), doc.page)
        except Exception as e:
            print(f"Ошибка в _add_header_footer: {e}")
    
    def save_to_file(self, filename: Optional[str] = None, 
                    directory: Optional[str] = None) -> str:
        """
        Сохранение PDF в файл
        
        Args:
            filename: Имя файла (если None, будет сгенерировано автоматически)
            directory: Директория для сохранения (если None, временная директория)
        
        Returns:
            str: Полный путь к сохраненному файлу
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
    
    def save_to_file_streaming(self, filename: Optional[str] = None,
                              directory: Optional[str] = None) -> BytesIO:
        """
        Сохранение PDF в файл и возврат BytesIO потока
        """
        # Сохраняем в файл
        filepath = self.save_to_file(filename, directory)
        
        # Читаем файл обратно в BytesIO
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Очищаем временный файл
        try:
            os.remove(filepath)
        except:
            pass
        
        return BytesIO(content)
    
    def get_pdf_bytes(self) -> bytes:
        """Получение PDF как байтов"""
        pdf_buffer = self.generate_pdf()
        return pdf_buffer.getvalue()
    
    def get_pdf_stream(self) -> BytesIO:
        """Получение PDF как BytesIO потока"""
        return self.generate_pdf()




@idea_pdf_router.post("/generate-pdf", response_class=Response)
async def generate_pdf_endpoint(data: IdeaData):
    """
    Генерация PDF документа на основе переданных данных
    
    Возвращает PDF файл для скачивания
    """
    try:
        # Конвертируем Pydantic модель в словарь
        json_data = data.dict()
        
        # Создаем генератор PDF
        generator = PDFGenerator(json_data)
        
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
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "application/pdf",
                "Content-Length": str(len(pdf_content))
            }
        )
    
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка генерации PDF: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {error_msg}")


@idea_pdf_router.post("/generate-pdf-save")
async def generate_pdf_and_save(data: IdeaData, 
                               directory: Optional[str] = None):
    """
    Генерация PDF документа и сохранение его в файл
    
    Возвращает информацию о сохраненном файла
    """
    try:
        # Конвертируем Pydantic модель в словарь
        json_data = data.dict()
        
        # Создаем генератор PDF
        generator = PDFGenerator(json_data)
        
        # Сохраняем в файл
        filepath = generator.save_to_file(directory=directory)
        
        # Возвращаем путь к файлу
        return {
            "status": "success",
            "message": "PDF успешно сгенерирован",
            "filename": os.path.basename(filepath),
            "filepath": filepath,
            "size": os.path.getsize(filepath),
            "download_url": f"/download-pdf/{os.path.basename(filepath)}"
        }
    
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка генерации PDF: {error_msg}")
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
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(file_size)
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка при загрузке файла: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке файла: {error_msg}")





def create_pdf_from_json(json_data: Dict[str, Any], 
                        output_file: Optional[str] = None,
                        directory: Optional[str] = None) -> str:
    """
    Функция для использования вне FastAPI
    """
    generator = PDFGenerator(json_data, output_file)
    return generator.save_to_file(directory=directory)


# Альтернативная реализация с использованием reportlab.pdfgen.canvas напрямую
class SimplePDFGenerator:
    """Простой генератор PDF для обхода проблем с кодировкой"""
    
    def __init__(self, json_data: Dict[str, Any]):
        self.data = json_data
        
    def generate(self) -> BytesIO:
        """Генерация простого PDF"""
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Ширина и высота страницы
        width, height = A4
        
        # Заголовок
        c.setFont("Helvetica", 12)
        c.drawRightString(width - 15*mm, height - 20*mm, "Интранет: Есть идея!")
        c.setLineWidth(0.4)
        c.line(0, height - 24*mm, width, height - 24*mm)
        
        # ФИО
        c.setFont("Helvetica-Bold", 10)
        full_name = self.data.get('full_name', '')
        c.drawCentredString(width/2, height - 100*mm, full_name)
        
        # Должность и отдел
        c.setFont("Helvetica", 9)
        position = self.data.get('position', '')
        department = self.data.get('department', '')
        subdepartment = self.data.get('subdepartment', '')
        directorate = self.data.get('directorate', '')
        
        dept_parts = []
        if directorate:
            dept_parts.append(directorate)
        if subdepartment:
            dept_parts.append(subdepartment)
        if department:
            dept_parts.append(department)
        dept_parts.append('НПО ЭМК')
        
        y_pos = height - 110*mm
        for part in dept_parts:
            if part.strip():
                c.drawCentredString(width/2, y_pos, part)
                y_pos -= 5*mm
        
        # Должность жирным
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(width/2, y_pos, position)
        
        # Название идеи
        y_pos -= 15*mm
        c.setFont("Helvetica", 10)
        idea_number = str(self.data.get('idea_number', '000')).zfill(3)
        idea_title = self.data.get('idea_title', '')
        title = f"№{idea_number}. {idea_title}"
        
        # Разбиваем длинный заголовок
        if len(title) > 50:
            words = title.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                if len(test_line) > 50:
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            for line in lines:
                c.drawCentredString(width/2, y_pos, line)
                y_pos -= 5*mm
        else:
            c.drawCentredString(width/2, y_pos, title)
            y_pos -= 5*mm
        
        # Текст идеи
        y_pos -= 10*mm
        c.setFont("Helvetica", 9)
        idea_text = self.data.get('idea_text', '')
        
        # Простой перенос текста
        text_lines = []
        for paragraph in idea_text.split('\n'):
            words = paragraph.split()
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                if c.stringWidth(test_line, "Helvetica", 9) > (width - 30*mm):
                    if len(current_line) == 1:
                        text_lines.append(' '.join(current_line))
                        current_line = []
                    else:
                        text_lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
            
            if current_line:
                text_lines.append(' '.join(current_line))
            text_lines.append('')  # Пустая строка между абзацами
        
        # Отрисовка текста
        for line in text_lines:
            if y_pos < 50*mm:  # Если осталось мало места
                c.showPage()
                y_pos = height - 30*mm
            if line.strip():
                c.drawString(15*mm, y_pos, line)
                y_pos -= 4*mm
            else:
                y_pos -= 2*mm
        
        # Подвал
        c.setLineWidth(0.4)
        c.line(0, 10*mm, width, 10*mm)
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, 6*mm, "Страница 1/1")
        
        c.save()
        buffer.seek(0)
        return buffer


# Дополнительный эндпоинт с простым генератором
@idea_pdf_router.post("/generate-pdf-simple", response_class=Response)
async def generate_pdf_simple_endpoint(data: IdeaData):
    """
    Простая генерация PDF (альтернатива для обхода проблем с кодировкой)
    """
    try:
        json_data = data.dict()
        generator = SimplePDFGenerator(json_data)
        pdf_stream = generator.generate()
        pdf_content = pdf_stream.getvalue()
        
        # Формируем имя файла
        title = data.idea_title
        safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
        idea_number = str(data.idea_number or "000").zfill(3)
        filename = f"Идея_{idea_number}_{safe_title[:50]}.pdf"
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "application/pdf"
            }
        )
    
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка простой генерации PDF: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {error_msg}")




@idea_pdf_router.post("/generate-pdf", response_class=Response)
async def generate_pdf_endpoint(data: IdeaData):
    """
    Генерация PDF документа на основе переданных данных
    
    Возвращает PDF файл для скачивания
    """
    try:
        # Конвертируем Pydantic модель в словарь
        json_data = data.dict()
        
        # Создаем генератор PDF
        generator = PDFGenerator(json_data)
        
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
                "Content-Type": "application/pdf"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {str(e)}")





