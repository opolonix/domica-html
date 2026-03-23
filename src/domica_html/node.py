from typing import Optional, List, Protocol, TYPE_CHECKING
from .inctement import inc
import contextvars
import inspect

item_context: contextvars.ContextVar[Optional[List["node_container"]]] = contextvars.ContextVar("item_context", default=None)

if TYPE_CHECKING:
    class node_container_rotocol(Protocol):
        def add_child(self, child: "node") -> None: ...
        def remove_child(self, child: "node") -> None: ...


class node_base:
    @staticmethod
    async def render_item(value) -> str:
        if isinstance(value, (list, tuple)):
            return "".join([await node_base.render_item(v) for v in value])

        if isinstance(value, node):
            result = value.render()
            return await node_base.render_item(result)

        if hasattr(value, "re_render") and callable((to_call := getattr(value, "re_render"))):
            result = to_call()
            return await node_base.render_item(result)

        if inspect.isawaitable(value):
            return await node_base.render_item(await value)

        return str(value)
            


class node:
    def __init__(self, anchor: bool = False):
        self._parent: Optional["node_container_rotocol"] = None

        if anchor:
            parent = self.get_parent()
            if parent:
                parent.add_child(self)

    @property
    def parent(self) -> Optional["node_container_rotocol"]:
        return self._parent
    
    async def render_item(self, value):
        return await node_base.render_item(value)

    @parent.setter
    def parent(self, value: Optional["node_container_rotocol"]):
        self._parent = value

    def get_parent(self) -> Optional["node_container_rotocol"]:
        stack = item_context.get()
        if stack is None:
            return None
        return stack[-1] if stack else None

    def unpin_from_parent(self) -> Optional["node_container_rotocol"]:
        old_parent = self._parent
        if old_parent:
            old_parent.remove_child(self)
            return old_parent
        return None


    def __enter__(self):
        stack = item_context.get()
        if stack is None:
            stack = []
            item_context.set(stack)
        stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        stack = item_context.get()
        if stack is None:
            return False
        stack.pop(-1)
        if not stack:
            item_context.set(None)
        return False

    def render(self):
        return "<node/>"

class node_container(node):
    def __init__(self, anchor: bool = False):
        super().__init__(anchor)
        self.children: List[node] = []

    def add_child(self, child: node):
        child.unpin_from_parent()
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: node):
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    async def render(self):
        with inc.final:
            return await self.render_item(self.children)
