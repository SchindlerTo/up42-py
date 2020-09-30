#pylint: skip-file

import math
import matplotlib.pyplot as plt
import io
import base64
from pathlib import Path

import up42


def define_env(env):
    """
    Hook function, define variables and macros here, see examples.

    Use {{ py_macro1() }} in markdown to integrate.
    Always requires mkdocs serve restart after a macro is edited.

    Basics: https://mkdocs-macros-plugin.readthedocs.io/en/latest/python/
    Advanced: https://mkdocs-macros-plugin.readthedocs.io/en/latest/advanced/

    # Examples:

        # add to the dictionary of variables available to markdown pages:
        env.variables['baz'] = "John Doe"

        @env.macro
        def bar(x):
            return (2.3 * x) + 7

        # If you wish, you can  declare a macro with a different name:
        def f(x):
            return x * x
        env.macro(f, 'barbaz')

        # or to export some predefined function
        env.macro(math.floor) # will be exported as 'floor'

        # Custom macros
        @env.macro
        def py_macro1(**kwargs):
            text = "abcdefg" * 2
            return text

    # Plot inline:
        # Inspired by https://github.com/fralau/mkdocs_macros_plugin/issues/37#issuecomment-636555341
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        html_string = f"<img alt='{alt_text}' width='{width}' height='{height}' src='data:image/png;base64,{data}'/>"
        return html_string

    """
    # Examples

    # add to the dictionary of variables available to markdown pages:
    # env.variables["baz"] = "John Doe"

    # @env.macro
    # def bar(x):
    #     return (2.3 * x) + 7

    # or to export some predefined function
    # env.macro(math.floor)  # will be exported as 'floor'

    # create a jinja2 filter
    # @env.filter
    # def reverse(x):
    #     "Reverse a string (and uppercase)"
    #     return x.upper()[::-1]

    @env.macro
    def get_template(template_name):
        return up42.get_templates()[template_name]


    @env.macro
    def plot_template(template_name, width=640, height=480):
        # Create plot
        import numpy as np
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        fig, ax = plt.subplots()
        ax.plot(t, s)
        ax.set(xlabel='time (s)', ylabel='voltage (mV)',
               title='About as simple as it gets, folks')
        ax.grid()

        # Plot inline
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        html_string = f"<img alt='{template_name}' width='{width}' height='{height}' src='data:image/png;base64,{data}'/>"
        return html_string

    # Custom macros
    # @env.macro
    # def py_macro1(**kwargs):
    #     text = "abcdefg" * 2
    #     return text

    # @env.macro
    # def up42_draw_aoi(**kwargs):
    #     print(up42.draw_aoi())

    # @env.macro
    # def up42_example_aoi(**kwargs):
    #     return up42.get_example_aoi(as_dataframe=True)

    # @env.macro
    # def button(label, url):
    #     "Add a button"
    #     url = "https://up42.com"
    #     HTML = """<a class='button' href="%s">%s</a>"""
    #     return HTML % (url, label)
    #
    # @env.macro
    # def download_button(path, icon="cloud_download"):
    #     """
    #     create a download button
    #     """
    #     repo_url = "repo_url"
    #     s3 = "s3"
    #
    #     if path.lower().startswith("http"):
    #         src_url = path
    #     else:
    #         # s3['object'] = "/".join(
    #         #     filter(None, [s3.get('prefix'), path])
    #         # )
    #
    #         # src_url = "https://s3.amazonaws.com/{bucket}/{object}".format(**s3)
    #         if repo_url.endswith("/"):
    #             repo_url = repo_url[:-1]
    #
    #         if path.startswith("/"):
    #             path = path[1:]
    #
    #         src_url = f"{repo_url}/blob/master/src/{path}"
    #
    #     return """
    #     <a href="{url}" target="_blank"><i class="material-icons">{icon}</i></a>
    #     """.format(
    #         icon=icon, url=src_url
    #     )
    #
    # @env.macro
    # def cfn_stack_row(name, stack_name, description):
    #     stack_url = "template"
    #
    #     return """
    #     | {name} | {description} | {download_button} |""".format(
    #         name=name,
    #         download_button=download_button(stack_url),
    #         description=description,
    #     )


def main():
    pass


if __name__ == "__main__":
    main()
