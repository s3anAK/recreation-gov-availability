git clone https://github.com/s3anAK/recreation-gov-availibility.git
cd $(find ~/ -type d -name "recreation-gov-availibility")
rm -rf .git
cp example.secrets.py secrets.py
sed -i -E "s/''/'$1'/g" secrets.py
virtualenv .
source bin/activate
pip install -r requirements.txt
deactivate
