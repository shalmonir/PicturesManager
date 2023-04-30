from src import create_app

app = create_app()


if __name__ == "__main__":
    context = ('local.crt', 'local.key')
    app.run(host="0.0.0.0", debug=True, use_reloader=False, ssl_context=context)
