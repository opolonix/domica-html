from .node import node
from .inctement import inc


class text(node):
    indent_prefix: bool = False

    def __init__(
        self,
        value: str | node,
        anchor = True
    ):
        self.value = value
        super().__init__(anchor)

    def render(self):
        if self.indent_prefix:
            return inc.enter_space + str(self.value)
        return str(self.value)
    

class indent_text(text):
    indent_prefix: bool = True