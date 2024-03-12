from cartesify import CartesifyBackend
from cartesify import CartesifyOptions


if __name__ == '__main__':
    options = CartesifyOptions("abc", True)
    cartesify = CartesifyBackend()
    cartesify.create_app(options)
