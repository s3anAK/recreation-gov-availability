cd $(find ~/ -type d -name "recreation-gov-availability")
rm -rf .git
cp example.secrets.py secrets.py
sed -i -E "s/''/'$1'/g" secrets.py
virtualenv .
source bin/activate
pip install -r requirements.txt
deactivate
