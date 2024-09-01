"""Generate and process HTML content.

References
----------
- [HTML Living Standard](https://html.spec.whatwg.org/)
- [HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
- [HTML document structure](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started#anatomy_of_an_html_element)
"""
from typing import TYPE_CHECKING as _TYPE_CHECKING

from htmp.comment import Comment
from htmp.container import Container
import htmp.display
from htmp.document import Document

from htmp.element import Element, create as element
from htmp import el, gel, spec

if _TYPE_CHECKING:
    from htmp.protocol import ContentType, ContentInputType


def container(
    *unlabeled_contents: ContentType,
    **labeled_contents: ContentType,
) -> Container:
    return Container(*unlabeled_contents, **labeled_contents)


def container_from_object(content: ContentInputType = None) -> Container:
    if not content:
        return Container()
    if isinstance(content, dict):
        return Container(**content)
    if isinstance(content, (list, tuple)):
        return Container(*content)
    return Container(content)


def comment(
    *unlabeled_contents: ContentType,
    **labeled_contents: ContentType
) -> Comment:
    return Comment(content=container(*unlabeled_contents, **labeled_contents))



