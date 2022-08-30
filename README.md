# Inyo National Forest Permit Checker

![Glacier Divide in the High Sierra](https://user-images.githubusercontent.com/56090826/187283263-a51866d9-29f2-472a-a528-5160ea6e934f.jpg)

This is a simple python program that offers additional functionality for reserving Inyo National Forest permits from [recreation.gov](recreation.gov). These features include searching for several permits at once, searching for several date ranges at once, and an automatic email when your desired permits are found. This program is intended to run on a Linux machine in order to harness cronjobs to make full use of the email notificaton service.

## Installion

 - Clone the repo onto your local machine using:
```
git clone https://github.com/s3anAK/recreation-gov-availability.git
```	
 - Run the following commands in the terminal: 
```
chmod +x setup.sh
./setup.sh API_KEY
```
where `API_KEY` is your recreation.gov api key. This can be obtained from ridb.recreation.gov. 

These commands will install all the necessary libaries and environments for the program. Assuming this runs sans errors, you are ready to go.
## Usage
 - To run the program, run `./permit.sh` from whichever directory you installed the program to. 
	 - There will be no output to the console when the program is run. If your desired permits are available, you will receive an email notifying you of this.
	 - Each time the program runs, a log of every query (one for each trip listed in `trips.json`) will be appear in `logs.txt`. You can use this to ensure that the program is running successfully, even if you are receiving emails because your desired permits are not available.
 - All trips are contained in the `trips.json` file. Each time the program runs, you may query an unlimited number of trailheads and trips per trailhead. Simply follow the syntax of the template trips provided.
	 - `trailhead` is your desired entry trailhead. You do not need specific permits beyond your entry trailhead (excepting the Whitney Zone).
		 - `name` is simply the name of the trailhead. This is not used in any queries, but rather to make the notification email more digestable as opposed to using the trailhead ID.
		 - `ID` refers to the recreation.gov-defined ID of your desired entry trailhead. You can access the list of IDs [here](https://www.fs.usda.gov/Internet/FSE_DOCUMENTS/fseprd922360.pdf). They are under the "Trail Codes" column. 
		 - `trips` refers to different trips from one trailhead. This could be trips that have different entry date ranges, trips with different group sizes, or trips with different notification emails.
			 - `starting_entry_date` and `ending_entry_date` refer to the range of days that you could possibly enter at your desired trailhead. Since you only need a permit for your entry trailhead and day, this does **not** refer to your entry and exit dates. For example, imagine you are planning a trip and you could enter either Thursday (10/1), Friday (10/2) or Saturday (10/3). This means that `starting_entry_date` should be 10/1 and `ending_entry_date` should be 10/3.
			 - `group_size` is the amount of people that will be using your permit.
			 - `email` is the email address you wish to be notified at if your desired permits are available.
- This program is most powerful when combined with a cron job to automatically search for available permits every x minutes. You may, of course, setup any cron job to work for your specific needs, but this one is simple and runs every 5 minutes:

	`*/5 * * * * cd $(find ~/ -type d -name "recreation-gov-availability") && ./permit.sh`

## Limitations

 - Of note is that this program does not actually reserve any permits for you. It is simply a tool to either lookup bulk availability for permits or to continually check for last minute cancellations of popular permits. You still must go to [recreation.gov](recreation.gov) to reserve your permits.
 - Due to inconsistent standards among various parks on recreation.gov, this program only works for the Inyo National Forest. Functionality may be added later to accomodate SEKI (Sequoia and Kings Canyon National Parks), but the Inyo National Forest covers permits for dozens of the Eastern Sierra's most stunning trailheads that should satisfy backpackers, climbers, fishermen, and wandering ascetics alike.

## Credits

 - Thanks to github.com/schlosser/yosemite-scraper for providing the inspiration to create this project.
 - All data for searching for permits is taken from ridb.recreation.gov.
