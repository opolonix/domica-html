from typing import Optional, List, Protocol, TYPE_CHECKING
import contextvars

item_context: contextvars.ContextVar[List["node_container"]] = contextvars.ContextVar("item_context", default=[])

if TYPE_CHECKING:
    class node_container_rotocol(Protocol):
        def add_child(self, child: "node") -> None: ...
        def remove_child(self, child: "node") -> None: ...

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

    @parent.setter
    def parent(self, value: Optional["node_container_rotocol"]):
        self._parent = value

    def get_parent(self) -> Optional["node_container_rotocol"]:
        stack = item_context.get()
        return stack[-1] if stack else None

    def unpin_from_parent(self) -> Optional["node_container_rotocol"]:
        if self._parent:
            self._parent.remove_child(self)
            old_parent = self._parent
            self._parent = None
            return old_parent
        return None

    def __enter__(self):
        stack = item_context.get()
        stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        stack = item_context.get()
        stack.pop(-1)
        return False

    def __str__(self):
        return self.render()

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

    def render(self):
        inner = "".join(str(c) for c in self.children)
        return f"<node_container>{inner}</node_container>"