Библиотека для формирования штмл структуры

```python
from domica_html import html, div, inc

doc = html()

with doc:
    div("hello world")

with inc(0, char="    "):
    print(doc.render())
```
output:
```txt
<html>
    <div>
        hello world
    </div>
</html>
```

Реализация собственного компонента:
```python
from domica_html import html, div, inc, node_container, script, indent_text
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

    def render(self):
        tags = external_tags.get()

        for child in tags[self.__class__]:
            if child is self: continue
            self.add_child(child)

        return super().render()

class global_script(external_container): ...

doc = html()
with doc:
    with div():
        div("Hello world with some script", onclick="hello_on_click")
        with global_script():
            indent_text("const hello_on_click = () => {")
            indent_text("    alert('hello!');")
            indent_text("}")

    with script():
        global_script(anchor=True)

with inc(indent=0, char="    "):
    print(doc.render())
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

