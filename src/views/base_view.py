import logging
import os
from typing import Any

from jinja2 import FileSystemLoader, Environment

from views.template_name import TemplateName

logger = logging.getLogger(__name__)


class BaseView:
    def __init__(self) -> None:
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        loader = FileSystemLoader(searchpath=template_path, encoding='utf-8')
        self.env = Environment(loader=loader, autoescape=True)
        logger.debug(f"Initialized Jinja2 Environment with template path: {template_path}")

    def render_template(self, template_name: TemplateName, context: dict[str, Any] | None = None) -> str:
        """
        Renders a template based on the given TemplateName enum.

        :param template_name: The TemplateName enum member representing the template to render.
        :param context: A dictionary containing the data to be passed to the template.
        :return: A string containing the rendered HTML, or an error message if the template is not found.
        """
        context = context or {}
        try:
            template = self.env.get_template(template_name.value)
            return template.render(**context)
        except Exception:
            logger.critical(f"Template not found: {template_name.value}")
            return "Error rendering template"

    def render_error_page(self, context: dict[str, str | None]) -> str:
        return self.render_template(TemplateName.ERROR_PAGE, context)
