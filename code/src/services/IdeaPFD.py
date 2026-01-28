import json
import os
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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

import requests
from PIL import Image as PILImage
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

idea_pdf_router = APIRouter(prefix="/idea_pdf_router")

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

class PDFGenerator:
    def __init__(self, json_data: Dict[str, Any], output_filename: Optional[str] = None):
        """
        Инициализация генератора PDF с данными из JSON
        """
        self.data = json_data
        self.buffer = BytesIO()
        
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
        
        # Фамилия (первое слово из ФИО)
        full_name = self.data.get('full_name', '').split()
        surname = full_name[0] if full_name else ''
        
        # Дата
        date_str = datetime.now().strftime("%Y%m%d")
        
        # Генерируем имя файла как в примере
        filename = f"Идея_{idea_number}_{safe_title[:50]}.pdf"
        return filename
    
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
            
            # Создаем маску для круглой обрезки
            mask = PILImage.new('L', (200, 200), 0)
            # В реальной реализации нужно нарисовать круг
            
            # Сохраняем в буфер
            buffer = BytesIO()
            img.save(buffer, format='PNG', quality=95)
            buffer.seek(0)
            
            return buffer
        except Exception as e:
            print(f"Ошибка обработки изображения: {e}")
            return image_stream
    
    def draw_header(self, canvas_obj: canvas.Canvas):
        """Отрисовка заголовка страницы"""
        # Заголовок справа
        canvas_obj.setFont("Helvetica", 12)
        canvas_obj.setFillColor(black)
        
        # Позиция как в оригинале
        title_y = self.page_height - 20 * mm
        title_x = self.page_width - 15 * mm
        
        canvas_obj.drawRightString(title_x, title_y, "Интранет: Есть идея!")
        
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
        canvas_obj.setFont("Helvetica", 8)
        footer_y = 6 * mm
        footer_text = f"Страница {page_num}/{total_pages}"
        canvas_obj.drawCentredString(self.page_width / 2, footer_y, footer_text)
    
    def generate_pdf(self) -> BytesIO:
        """Генерация PDF документа"""
        # Создаем буфер для PDF
        pdf_buffer = BytesIO()
        
        # Создаем документ
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=self.right_margin,
            leftMargin=self.left_margin,
            topMargin=self.top_margin,
            bottomMargin=self.bottom_margin
        )
        
        # Стили
        styles = getSampleStyleSheet()
        
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
        full_name = self.data.get('full_name', '')
        name_style = ParagraphStyle(
            'NameStyle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=5*mm
        )
        story.append(Paragraph(full_name, name_style))
        
        # Должность и отделы
        position = self.data.get('position', '')
        department = self.data.get('department', '')
        subdepartment = self.data.get('subdepartment', '')
        directorate = self.data.get('directorate', '')
        
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
            fontName='Helvetica',
            fontSize=9,
            alignment=TA_CENTER,
            spaceAfter=20*mm
        )
        story.append(Paragraph(dept_html, dept_style))
        
        # Название идеи с номером
        idea_number = str(self.data.get('idea_number', '000')).zfill(3)
        idea_title = self.data.get('idea_title', '')
        title_text = f"№{idea_number}. {idea_title}"
        
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading2'],
            fontName='Helvetica',
            fontSize=10,
            alignment=TA_CENTER,
            textColor=black,
            spaceBefore=0,
            spaceAfter=40,
            leading=14
        )
        title_style.fontName = 'Helvetica'  # Не жирный
        
        story.append(Paragraph(title_text, title_style))
        
        # Текст идеи
        idea_text = self.data.get('idea_text', '').replace('\n', '<br/>')
        
        text_style = ParagraphStyle(
            'TextStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            alignment=TA_JUSTIFY,
            leading=12,
            firstLineIndent=20
        )
        
        story.append(Paragraph(idea_text, text_style))
        
        # QR-код
        # story.append(Spacer(1, 20*mm))
        
        # qr_url = 'https://intranet.emk.ru/'
        # try:
        #     qr_code = qr.QrCodeWidget(qr_url)
        #     bounds = qr_code.getBounds()
        #     width = bounds[2] - bounds[0]
        #     height = bounds[3] - bounds[1]
            
        #     d = Drawing(30*mm, 30*mm, transform=[30*mm/width, 0, 0, 30*mm/height, 0, 0])
        #     d.add(qr_code)
            
        #     qr_buffer = BytesIO()
        #     c = canvas.Canvas(qr_buffer, pagesize=(30*mm, 30*mm))
        #     renderPDF.draw(d, c, 0, 0)
        #     c.save()
        #     qr_buffer.seek(0)
            
        #     qr_img = RLImage(qr_buffer, width=30*mm, height=30*mm)
        #     qr_img.hAlign = 'LEFT'
        #     story.append(qr_img)
        # except Exception as e:
        #     print(f"Ошибка при создании QR-кода: {e}")
        
        # Собираем документ
        doc.build(
            story,
            onFirstPage=self._add_header_footer,
            onLaterPages=self._add_header_footer
        )
        
        pdf_buffer.seek(0)
        return pdf_buffer
    
    def _add_header_footer(self, canvas_obj: canvas.Canvas, doc: SimpleDocTemplate):
        """Добавление header и footer на каждую страницу"""
        self.draw_header(canvas_obj)
        self.draw_footer(canvas_obj, canvas_obj.getPageNumber(), doc.page)
    
    
    def get_pdf_bytes(self) -> bytes:
        """Получение PDF как байтов"""
        pdf_buffer = self.generate_pdf()
        return pdf_buffer.getvalue()
    
    def get_pdf_stream(self) -> BytesIO:
        """Получение PDF как BytesIO потока"""
        return self.generate_pdf()


# Инициализация FastAPI приложения
# app = FastAPI(
#     title="PDF Generator API",
#     description="API для генерации PDF документов с идеями",
#     version="1.0.0"
# )


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





