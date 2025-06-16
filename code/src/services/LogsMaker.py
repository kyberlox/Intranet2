from tqdm import tqdm

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

    def error_message(self, message: str) -> None:
        """Выводит сообщение об ошибке красным цветом в консоль"""
        print(f"\033[91m[ERROR] {message}\033[0m")  # 91 - красный цвет

    def warning_message(self, error: Exception) -> None:
        """Выводит предупреждение/ошибку желтым цветом в консоль"""
        error_msg = str(error)
        print(f"\033[93m[WARNING] {error_msg}\033[0m")  # 93 - желтый цвет

    async def auth_error_template(
        self, 
        request: Request, 
        error_message: str = "Ошибка авторизации",
        login_url: str = "/user/auth"
    ) -> HTMLResponse:
        """Возвращает HTML шаблон с ошибкой авторизации"""
        context = {
            "request": request,
            "error_message": error_message,
            "login_url": login_url
        }
        return self.templates.TemplateResponse("auth_error.html", context)
