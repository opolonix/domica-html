from typing import Union

from .node import node_container, node
from .inctement import inc


class text(node_container):
    indent_prefix = None

    def __init__(
        self,
        *value: Union[str, node],
        anchor: bool = True,
        sep: str = ""
    ):
        self.value = value
        self.sep = sep
        super().__init__(anchor)

    async def render(self):
        with inc.final:
            sep = await self.render_item(self.sep)
            content = sep.join([await self.render_item(v) for v in self.value])

            if self.children:
                with inc:
                    content += await self.render_item(self.children)

            if self.indent_prefix is not None:
                return await self.render_item(self.indent_prefix) + content
            return content

class line(text):
    indent_prefix = inc.start_space
