from tqdm import tqdm
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./front_jinja")

class LogsMaker:
    def __init__(self):
        self.logs = []

    def progress(self, this_list, title=None, **kwargs):
        #bar_format = "{l_bar}%s{bar}%s{r_bar}" % ("\033[33m", "\033[0m")
        color_code = 208 #оранжевый
        bar_format = (
            f"{'{desc}: ' if title else ''}"
            f"{'{percentage:3.0f}%|'}"
            f"\033[38;5;{color_code}m{{bar}}\033[0m| "
            f"{{n_fmt}}/{{total_fmt}} [{{elapsed}}<{{remaining}}, {{rate_fmt}}{{postfix}}]"
        )
        if title is not None:
            kwargs["desc"] = title

        return tqdm(this_list, bar_format=bar_format, **kwargs)

    async def error_message(self, error: Exception) -> None:
        """Выводит сообщение об ошибке красным цветом в консоль"""
        error_msg = str(error)
        print(f"\033[91m[ERROR] {error_msg}\033[0m")  # 91 - красный цвет
        return {"err" : error_msg}

    async def warning_message(self, message: str) -> None:
        """Выводит предупреждение/ошибку желтым цветом в консоль"""
        print(f"\033[93m[WARNING] {message}\033[0m")  # 93 - желтый цвет
        return {"warn" : message}

    async def auth_error_template(
        self, 
        request: Request, 
        error_message: str = "Ошибка авторизации",
        help_url: str = "/user/auth"
    ) -> HTMLResponse:
        """Возвращает HTML шаблон с ошибкой авторизации"""
        context = {
            "request": request,
            "error_message": error_message,
            "help_url": help_url
        }
        return templates.TemplateResponse("auth_error.html", context)
