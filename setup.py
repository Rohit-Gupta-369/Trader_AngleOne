from setuptools import setup, find_packages

setup(
    name='TraderAngleOne',
    version="1.3",
    packages= find_packages(),
    install_requires=[
        # pandas>=2.0.0,
        # numpy>=1.24.0,
        # pyotp>=2.9.0,
        # smartapi-python>=1.5.5,
        # requests>=2.31.0,
        # websocket-client>=1.6.0,
        # logzero>=1.7.0,
    ]
)

# py setup.py sdist bdist_wheel
# pip install dist/TraderAngleOne-1.1-py3-none-any.whl
"""
pip install build
python -m build
pip install dist/TraderAngleOne-1.3-py3-none-any.whl
"""
