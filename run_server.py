from server import create_app


def main():
    app = create_app()
    app.run("0.0.0.0", 8000, debug=True)


if __name__ == "__main__":
    exit(main())
