# Inyo National Forest Permit Checker

![Glacier Divide in the High Sierra](https://user-images.githubusercontent.com/56090826/187283263-a51866d9-29f2-472a-a528-5160ea6e934f.jpg)

This is a simple python program that offers additional functionality for reserving Inyo National Forest permits from [recreation.gov](https://www.recreation.gov). These features include searching for several permits at once, searching for several date ranges at once, and an automatic email when your desired permits are found. This program is intended to run on a Linux machine in order to harness cronjobs to make full use of the email notification service.

## Prerequisites
1. An API key from [ridb.recreation.gov](https://ridb.recreation.gov), which you can get in a few clicks with your existing [recreation.gov](https://www.recreation.gov) account.
1. A Gmail account for sending out updates from this script and an associated [App Password](https://support.google.com/accounts/answer/185833?hl=en) for it.

## Installation

 - Clone the repo onto your local machine using:
```
git clone https://github.com/s3anAK/recreation-gov-availability.git
```	
 - Run the following commands in the terminal: 
```
cd recreation-gov-availability
chmod +x setup.sh
./setup.sh
```
- The setup script will prompt you to enter your API key, the Gmail account you wish to use for sending out any updates from this script, and associated Gmail app password (which is **NOT** your regular password; it is a special one that you can generate [here](https://myaccount.google.com/apppasswords)) These can also be manually entered into `.env`, which you will need to create within the directory containing this script.

`.env` contents:
```sh
API_KEY=api_key_here
FROM_GMAIL=some_email@gmail.com
FROM_GMAIL_APP_PASSWORD=the_app_password
```

**Note**: for compatibility with an external secret manager that can populate environment variables, `checker.py` will look for `API_KEY`, `FROM_GMAIL`, and `FROM_GMAIL_APP_PASSWORD` as environment variables first, and fall back to `.env` if the environment variables are not present. Therefore, `.env` is not needed if `API_KEY`, `FROM_GMAIL`, and `FROM_GMAIL_APP_PASSWORD` are present as environment variables.

The above commands will install all the necessary libraries and environments for the program. Assuming this runs sans errors, you are ready to go.

## Usage
 - To run the program, run `./permit.sh` from whichever directory you installed the program to. 
	 - There will be no output to the console when the program is run. If your desired permits are available, you will receive an email notifying you of this.
	 - Each time the program runs, a log of every query (one for each trip listed in `trips.json`) will be appear in `logs.txt`. You can use this to ensure that the program is running successfully, even if you are not receiving emails because your desired permits are not available.
 - All trips are contained in the `trips.json` file. Each time the program runs, you may query an unlimited number of trailheads and trips per trailhead. Simply follow the syntax of the template trips provided.
	 - `trailhead` is your desired entry trailhead. You do not need specific permits beyond your entry trailhead (excepting the Whitney Zone).
		 - `name` is simply the name of the trailhead. This is not used in any queries, but rather to make the notification email more digestable as opposed to using the trailhead ID.
		 - `ID` refers to the recreation.gov-defined ID of your desired entry trailhead. You can access the list of IDs [here](https://www.fs.usda.gov/Internet/FSE_DOCUMENTS/fseprd922360.pdf). They are under the "Trail Codes" column. 
		 - `trips` refers to different trips from one trailhead. This could be trips that have different entry date ranges, trips with different group sizes, or trips with different notification emails.
			 - `starting_entry_date` and `ending_entry_date` refer to the range of days that you could possibly enter at your desired trailhead. Since you only need a permit for your entry trailhead and day, this does **not** refer to your entry and exit dates. For example, imagine you are planning a trip and you could enter either Thursday (10/1), Friday (10/2) or Saturday (10/3). This means that `starting_entry_date` should be 10/1 and `ending_entry_date` should be 10/3.
			 - `group_size` is the amount of people that will be using your permit.
			 - `email` is the email address you wish to be notified at if your desired permits are available. Note that the default emails in in `trips.json` are not real emails and must be changed to your preferred email before the notification service will work.
- This program is most powerful when combined with a cron job to automatically search for available permits every x minutes. You may, of course, setup any cron job to work for your specific needs, but this is an example of one that runs every 5 minutes:

	`*/5 * * * * cd $(find ~/ -type d -name "recreation-gov-availability") && ./permit.sh`

## Limitations

 - Of note is that this program does not actually reserve any permits for you. It is simply a tool to either lookup bulk availability for permits or to continually check for last minute cancellations of popular permits. You still must go to [recreation.gov](https://www.recreation.gov) to reserve your permits.
 - Due to inconsistent standards among various parks on recreation.gov, this program only works for the Inyo National Forest. Functionality may be added later to accommodate SEKI (Sequoia and Kings Canyon National Parks), but the Inyo National Forest covers permits for dozens of the Eastern Sierra's most stunning trailheads that should satisfy backpackers, climbers, fishermen, and wandering ascetics alike.

## Credits

 - Thanks to [github.com/schlosser/yosemite-scraper](https://github.com/schlosser/yosemite-scraper) for providing the inspiration to create this project.
 - All data for searching for permits is taken from [ridb.recreation.gov](https://ridb.recreation.gov).
