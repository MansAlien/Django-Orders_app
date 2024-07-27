# components/button.py
from django_components import component
from django.urls import reverse
from django.utils.safestring import mark_safe

@component.register("button")
class Button(component.Component):
    template_name = "button.html"

    def get_context_data(self, label, style="default", hx_target=None, hx_swap="none", hx_trigger=None, 
                         url_name=None, url_params=None, hx_post=None, hx_get=None, hyper=None, **kwargs):
        styles = {
            "default": "text-white bg-blue-600 hover:bg-blue-700 focus:ring-blue-800",
            "alternative": "text-gray-400 bg-gray-800 border border-gray-600 hover:text-white hover:bg-gray-700",
            "dark": "text-white bg-gray-800 hover:bg-gray-700 focus:ring-gray-700 border-gray-700",
            "light": "text-white bg-gray-800 border border-gray-600 hover:bg-gray-700 hover:border-gray-600 focus:ring-gray-700",
            "green": "text-white bg-green-600 hover:bg-green-700 focus:ring-green-800",
            "red": "text-white bg-red-600 hover:bg-red-700 focus:ring-red-900",
            "yellow": "text-white bg-yellow-400 hover:bg-yellow-500 focus:ring-yellow-900",
            "purple": "text-white bg-purple-600 hover:bg-purple-700 focus:ring-purple-900",
        }

        # Handle URL generation
        if url_name:
            if url_params is None:
                url_params = []
            elif not isinstance(url_params, (list, tuple)):
                url_params = [url_params]

            # Use reverse to generate the URL
            try:
                url = reverse(url_name, args=url_params)
            except:
                # If reverse fails (e.g., due to template variables), fall back to template tag
                params_str = " ".join(str(param) for param in url_params)
                url = mark_safe("{% url '" + url_name + "' " + params_str + " %}")

            if not (hx_post or hx_get):
                hx_get = url
            elif hx_post is True:
                hx_post = url
            elif hx_get is True:
                hx_get = url

        return {
            "label": label,
            "style": styles.get(style, styles["default"]),
            "hx_target": hx_target,
            "hx_swap": hx_swap,
            "hx_trigger": hx_trigger,
            "hx_post": hx_post,
            "hx_get": hx_get,
            "hyper": hyper,
            **kwargs
        }
