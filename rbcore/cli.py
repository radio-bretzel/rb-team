from rbcore import create_app

def main():
    radiobretzel_core = create_app()
    radiobretzel_core.run(debug=True, use_reloader=False, host='0.0.0.0')
