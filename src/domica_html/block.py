from typing import Union

from .node import node_container, node
from .inctement import inc


class text(node_container):
    indent_prefix: bool = False

    def __init__(
        self,
        *value: Union[str, node],
        anchor = True
    ):
        self.value = value
        super().__init__(anchor)

    def render(self):
        content = self.value_sync(self.value)
        if self.children:
            with inc:
                content += self.value_sync(self.children)

        if self.indent_prefix:
            return inc.enter_space + content
        return content

class line(text):
    indent_prefix: bool = True
