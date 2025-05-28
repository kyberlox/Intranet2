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


