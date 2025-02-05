import pathlib

req_file                = tdu.expandPath(ipar.ExtPython.Pyreqs)
install_target          = tdu.expandPath(ipar.ExtPython.Target)
install_script_path     = pathlib.Path(install_target).parents[0]

win_file                = install_script_path / 'dep_install_windows.cmd'
mac_file                = install_script_path / 'dep_install_mac.sh'

# windows template
win_txt = '''
:: update pip
python -m pip install --user --upgrade pip


:: install from requirements file
py -3.5 -m pip install -r "{reqs}" --target="{target}"
'''

# mac template
mac_txt = '''
#!/bin/bash 

dep=$(dirname "$0")
pythonDir=/python

# Check architecture
if [ "$(uname -m)" == "x86_64" ]; then
    echo "Installing for Intel Mac..."
elif [ "$(uname -m)" == "arm64" ]; then
    echo "Installing for Apple Silicon Mac..."
else
    echo "Unsupported architecture."
    exit 1
fi

# fix up pip with python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Update dependencies
# make sure pip is up to date
pip3 install --user --upgrade pip

# install requirements
pip3 install -r "{reqs}" --target="{target}"
'''

formated_win_txt = win_txt.format(reqs=req_file, target=install_target)
formated_mac_txt = mac_txt.format(reqs=req_file, target=install_target)

with open(str(win_file), "w+") as win_script:
    win_script.write(formated_win_txt)

with open(str(mac_file), "w+") as mac_script:
    mac_script.write(formated_mac_txt)