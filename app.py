from flask import Flask, render_template_string
import platform

app = Flask(__name__)

@app.route('/')
def index():
    architecture = platform.machine()
    # Mapping the platform.machine() output to more user-friendly architecture names
    arch_map = {
        'x86_64': 'x86',
        'AMD64': 'x86',
        'i386': 'x86',
        'i686': 'x86',
        'armv7l': 'ARM',
        'aarch64': 'ARM',
        'ppc64': 'PPC',
        'ppc64le': 'PPC',
        's390': 'Mainframe',
        's390x': 'Mainframe',
    }
    user_friendly_arch = arch_map.get(architecture, architecture)

    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>System Architecture</title>
    </head>
    <body>
        <h1>System Architecture</h1>
        <p>The architecture of this system is: <strong>{{ architecture }}</strong></p>
    </body>
    </html>
    '''
    return render_template_string(html_content, architecture=user_friendly_arch)

if __name__ == '__main__':
    app.run(debug=True)