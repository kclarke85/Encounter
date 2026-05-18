from flask import Flask, render_template, jsonify, request, redirect, abort
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_change_in_production")

# ── Load mock data once at startup ──────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'sentinel-mock-data.json')

try:
    with open(DATA_PATH) as f:
        sentinel_data = json.load(f)
except FileNotFoundError:
    sentinel_data = {"devices": [], "alerts": [], "network": {}}


# ── Auth helper ─────────────────────────────────────────────────
# After Authelia verifies a request, Nginx injects these headers.
# We read them to know who's logged in.

def get_current_user():
    """Extract authenticated user info injected by Nginx/Authelia."""
    return {
        "username": request.headers.get("Remote-User", None),
        "name": request.headers.get("Remote-Name", None),
        "groups": request.headers.get("Remote-Groups", ""),
    }


def authelia_required(f):
    """
    Decorator: returns 401 if no Remote-User header is present.
    In production this should never trigger because Nginx/Authelia
    blocks unauthenticated requests before they reach Flask.
    This is a defence-in-depth check for direct Flask access.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user["username"]:
            abort(401)
        return f(*args, **kwargs)
    return decorated


# ── Routes ──────────────────────────────────────────────────────

@app.route('/')
def home():
    """Encounter Engineering marketing site — public."""
    return render_template('index.html', user=get_current_user())


@app.route('/sentinel')
@authelia_required
def sentinel():
    """Sentinel monitoring portal — protected by Authelia."""
    user = get_current_user()
    return render_template('sentinel.html', user=user)


@app.route('/logout')
def logout():
    """
    Redirects to Authelia's logout endpoint.
    Authelia clears the session cookie, then redirects to /.
    The actual session invalidation happens in Authelia, not Flask.
    """
    return redirect('/auth/logout')


# ── API endpoints (all protected by Authelia via Nginx) ─────────

@app.route('/api/sentinel-data')
@authelia_required
def api_sentinel_data():
    """Returns full Sentinel JSON data."""
    return jsonify(sentinel_data)


@app.route('/api/devices')
@authelia_required
def api_devices():
    """Returns device array."""
    return jsonify(sentinel_data.get('devices', []))


@app.route('/api/alerts')
@authelia_required
def api_alerts():
    """Returns active alerts only."""
    alerts = [a for a in sentinel_data.get('alerts', []) if a.get('status') == 'active']
    return jsonify(alerts)


@app.route('/api/network')
@authelia_required
def api_network():
    """Returns network summary stats."""
    return jsonify(sentinel_data.get('network', {}))


@app.route('/api/whoami')
@authelia_required
def api_whoami():
    """Debug endpoint — shows current Authelia-authenticated user."""
    return jsonify(get_current_user())


# ── Error handlers ───────────────────────────────────────────────

@app.errorhandler(401)
def unauthorized(e):
    """Redirect unauthenticated users to Authelia login."""
    return redirect(f'/auth?rd={request.url}'), 302


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', user=get_current_user()), 403


# ── Run ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    # In Docker the app is served by Gunicorn, not this block.
    app.run(host='0.0.0.0', port=5000, debug=False)
