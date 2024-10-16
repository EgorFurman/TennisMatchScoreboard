import os
from abc import ABC, abstractmethod

from jinja2 import Environment, FileSystemLoader


TEMPLATES_DIR = f'{os.getcwd()}/resources/templates'


class BaseView(ABC):
    @classmethod
    @abstractmethod
    def render_template(cls, template_name: str, *args, **kwargs):
        pass


class ViewToHTML(BaseView):
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR)
    )

    @classmethod
    def render_template(cls, template_name: str, *args, **kwargs) -> str:
        return cls.env.get_template(template_name).render(*args, **kwargs)


#print(os.path.abspath('resources/favicon.png'))
