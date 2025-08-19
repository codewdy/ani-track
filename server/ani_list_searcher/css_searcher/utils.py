import inspect
from bs4 import BeautifulSoup
from bs4.element import NavigableString


def get_caller_info():
    frame = inspect.currentframe().f_back.f_back
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    function_name = frame.f_code.co_name

    # 获取调用方的类名
    class_name = None
    if "self" in frame.f_locals:
        class_name = frame.f_locals["self"].__class__.__name__

    if class_name:
        return f"{class_name}.{function_name}"
    else:
        return f"{function_name}"


async def request(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            raise RuntimeError(
                f"cannot get result status_code={response.status} caller={get_caller_info()}"
            )
        return BeautifulSoup(await response.text(), features="lxml")


def to_text(token):
    for child in token.children:
        if isinstance(child, NavigableString):
            return child.text.strip()
    return token.text.strip()
