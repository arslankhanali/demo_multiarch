from flask import Flask, render_template_string, request, jsonify
import platform
import requests

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

    # Define colors for each architecture
    arch_colors = {
        'x86': '#FFDDC1',
        'ARM': '#D4F4DD',
        'PPC': '#D4E4F4',
        'Mainframe': '#EAD4F4',
        'Unknown': '#FFFFFF'
    }
    bg_color = arch_colors.get(user_friendly_arch, arch_colors['Unknown'])

    # Gather additional system statistics
    system = platform.system()
    node = platform.node()
    release = platform.release()
    version = platform.version()
    processor = platform.processor()
    python_version = platform.python_version()

    other_arch = None
    other_endpoint = request.args.get('endpoint')
    if other_endpoint:
        try:
            response = requests.get(other_endpoint)
            if response.status_code == 200:
                other_arch = response.json().get('architecture')
            else:
                other_arch = f"Error: {response.text}"
        except Exception as e:
            other_arch = f"Error: {e}"

    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>System Architecture</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: {{ bg_color }}; }
            h1 { color: #d2232a; }
            p { font-size: 1.2em; }
            .stats { margin-top: 20px; }
            table { width: 50%; margin-top: 20px; border-collapse: collapse; }
            th, td { border: 1px solid #000; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>System Architecture</h1>
        <p>The architecture of this system is: <strong>{{ architecture }}</strong></p>
        <table>
            <tr>
                <th>Architecture</th>
                <th>Color</th>
            </tr>
            <tr>
                <td>x86</td>
                <td style="background-color: #FFDDC1;">Creme</td>
            </tr>
            <tr>
                <td>ARM</td>
                <td style="background-color: #D4F4DD;">Green</td>
            </tr>
            <tr>
                <td>PPC</td>
                <td style="background-color: #D4E4F4;">Blue</td>
            </tr>
            <tr>
                <td>Mainframe</td>
                <td style="background-color: #EAD4F4;">Purple</td>
            </tr>
            <tr>
                <td>Unknown</td>
                <td style="background-color: #FFFFFF;">Silver</td>
            </tr>
        </table>
        <div class="stats">
            <h2>Additional System Statistics</h2>
            <p><strong>System:</strong> {{ system }}</p>
            <p><strong>Node Name:</strong> {{ node }}</p>
            <p><strong>Release:</strong> {{ release }}</p>
            <p><strong>Version:</strong> {{ version }}</p>
            <p><strong>Processor:</strong> {{ processor }}</p>
            <p><strong>Python Version:</strong> {{ python_version }}</p>
        </div>
        <form method="get" action="/">
            <label for="endpoint">Other Container Endpoint:</label>
            <input type="text" id="endpoint" name="endpoint">
            <button type="submit">Check</button>
        </form>
        {% if other_arch %}
        <div class="stats">
            <h2>Other Container's Architecture</h2>
            <p>The architecture of the other container is: <strong>{{ other_arch }}</strong></p>
        </div>
        {% endif %}
    </body>
    </html>
    '''
    return render_template_string(html_content, architecture=user_friendly_arch, other_arch=other_arch, system=system, node=node, release=release, version=version, processor=processor, python_version=python_version, bg_color=bg_color)

@app.route('/architecture')
def architecture():
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
    return jsonify({'architecture': user_friendly_arch})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
