import rbcore


def main():
    radiobretzel_core = rbcore.create_app()
    radiobretzel_core.run(debug=True, use_reloader=False, host='0.0.0.0')

if __name__ == '__main__':
    main()
