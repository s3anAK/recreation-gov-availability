cd $(find ~/ -type d -name "recreation-gov-availability")
rm -rf .git
virtualenv .
source bin/activate
pip install -r requirements.txt

# Populate .env last so it's the last output on the screen.
if [[ ! -e .env ]]; then
  printf "\n"
  read -p "Enter the Gmail account to send notifications from: " FROM_GMAIL
  read -p "Enter the associated Gmail App Password: " FROM_GMAIL_APP_PASSWORD
  read -p "Enter your ridb.recreation.gov API key: " API_KEY

  printf "\n"
  if [[ ! -z "$FROM_GMAIL" ]]; then
    echo "FROM_GMAIL=$FROM_GMAIL" >> .env
  else
    echo "No Gmail entered. See README.md and update .env manually"
  fi

  if [[ ! -z "$FROM_GMAIL_APP_PASSWORD" ]]; then
    echo "FROM_GMAIL_APP_PASSWORD=$FROM_GMAIL_APP_PASSWORD" >> .env
  else
    echo "No Gmail App Password entered. See README.md and update .env manually"
  fi

  if [[ ! -z "$API_KEY" ]]; then
    echo "API_KEY=$API_KEY" >> .env
  else
    echo "No API key entered. See README.md and update .env manually"
  fi
else
  printf "Skipping .env configuration as .env already exists.\n\n"
fi

deactivate
chmod +x permit.sh
