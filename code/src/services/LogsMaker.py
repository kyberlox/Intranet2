import logging
from tqdm import tqdm
import json
from datetime import datetime



class LogsMaker:
    def __init__(self):
        self.logging = logging
        self.logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%d.%m.%Y %H:%M:%S",
            filename="./logs/fastapi-logs.log",
            filemode="a",
        )

    # ---- новый метод для отправки JSON в stdout ----
    def _log_to_loki(self, level: str, message: str, log_type: str = None) -> None:
        """Отправляет структурированный лог в stdout для Loki"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.upper(),
            "message": str(message),
            "type": log_type or level.lower(),
            "logger": "LogsMaker"
        }
        # Выводим JSON в stdout (без ANSI-кодов)
        print(json.dumps(log_entry, ensure_ascii=False))
        # Существующий цветной print и logging остаются нетронутыми

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

    def fatal_message(self, message: str) -> None:
        """Выводит сообщение о критической ошибке в консоль"""
        error_msg = str(message)
        logging.error(f"🔥 {error_msg}")
        print(f"🔥 \033[91m[FATAL ERROR] 🔥 {error_msg}\033[0m")  # 91 - красный цвет
        self._log_to_loki("fatal", error_msg, log_type="fatal")
        return {"status" : "error", "message" : error_msg}

    def error_message(self, error: Exception) -> None:
        """Выводит сообщение об ошибке красным цветом в консоль"""
        error_msg = str(error)
        logging.error(f"❌ {error_msg}")
        print(f"❌ \033[91m[ERROR] ❌ {error_msg}\033[0m")  # 91 - красный цвет
        self._log_to_loki("error", error_msg, log_type="error")
        return {"status" : "error", "message" : error_msg}

    def warning_message(self, message: str) -> None:
        """Выводит предупреждение/ошибку желтым цветом в консоль"""
        logging.warning(f"⚠️ {message}")
        error_msg = str(message)
        print(f"⚠️ \033[93m[WARNING] ⚠️ {message}\033[0m")  # 93 - желтый цвет
        self._log_to_loki("warning", error_msg, log_type="warning")
        return {"status" : "warning", "message" : message}

    def info_message(self, message: str) -> None:
        """Выводит информационное сообщение синим цветом в консоль"""
        logging.info(f"ℹ️ {message}")
        print(f"ℹ️ \033[94m[INFO] ℹ️ {message}\033[0m")  # 94 - голубой цвет
        return {"status" : "info", "message" : message}

    def ready_status_message(self, message: str) -> None:
        """Выводит статус успешного выполения программы в зеленом цвете в консоль"""
        logging.debug(f"✅ {message}")
        print(f"✅ \033[92m[READY] ✅ {message}\033[0m")  # 92 - зеленый цвет
        return {"status" : "ready", "message" : message}
