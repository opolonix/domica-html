Библиотека для декларативного формирования HTML-структуры на Python.

Текущая версия использует асинхронный рендер. Основной публичный API для получения HTML теперь `await render()`.

Актуальная версия проекта: `0.2.1`.

## Установка

```bash
pip install domica-html
```

Установка конкретной версии напрямую из GitHub:

```bash
pip install git+https://github.com/opolonix/domica-html.git@v0.2.1
```

Для локальной разработки:

```bash
pip install -e .[dev]
```

## Пример
```python
import asyncio

from domica_html import html, div

async def main():
    doc = html()

    with doc:
        div("hello world")

    print(await doc.render())

asyncio.run(main())
```
output:
```txt
<html>
    <div>
        hello world
    </div>
</html>
```

## Реализация собственного компонента
```python
import asyncio

from domica_html import html, div, inc, node_container, script, line
from contextvars import ContextVar
from collections import defaultdict
from typing import Type

external_tags: ContextVar[dict[Type, list["external_container"]]] = ContextVar("external_tags", default=defaultdict(list))

class external_container(node_container):
    def __init__(self, *, anchor=False):
        super().__init__(anchor=anchor)
        if not anchor:
            tags = external_tags.get()
            tags[self.__class__].append(self)

    async def render(self):
        tags = external_tags.get()

        for child in tags[self.__class__]:
            if child is self: continue
            self.add_child(child)

        return await super().render()

class global_script(external_container): ...

async def main():
    doc = html()

    with doc:
        with div():
            div("Hello world with some script", onclick="hello_on_click")
            with global_script():
                line("const hello_on_click = () => {")
                line(inc.char, "alert('hello!');")
                line("}")

        with script():
            global_script(anchor=True)

    print(await doc.render())

asyncio.run(main())

```
output:
```txt
<html>
    <div>
        <div onclick="hello_on_click">  
            Hello world with some script
        </div>
    </div>
    <script>
        const hello_on_click = () => {  
            alert('hello!');
        }
    </script>
</html>
```

## Релизы

- `0.2.1`: текущий релиз асинхронного рендера через `await render()`
- `0.2.0`: первый релиз с асинхронным рендером через `await render()`
- `0.1.5`: финальная стабильная синхронная версия ветки `0.1.x`
