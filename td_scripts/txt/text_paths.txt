import sys

python_ext = tdu.expandPath(ipar.ExtPython.Target)

if python_ext not in sys.path:
    sys.path.append(python_ext)