cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name='axomicdb',
    version='0.1.0',
    packages=find_packages(),
    description='A Python database library with import/export features to store your data for different-device use!',
    author='Your Name',
    author_email='noemail@protonmail',
    url='https://github.com/axom0022/axomicdb',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
EOF
