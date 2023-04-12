<h1 align="center">ICS News Website</h1>
<p align="center">
  	<a href="https://icsizmir.com/">Live Website</a>
  	<br>
	<br>
	<a href="https://github.com/ICS-Izmir/News-Website/actions/workflows/codeql-analysis.yml"><img src="https://github.com/ICS-Izmir/News-Website/actions/workflows/codeql-analysis.yml/badge.svg"></a>
	|
	<a href="https://github.com/ICS-Izmir/News-Website/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ICS-Izmir/News-Website?color=blue"></a>
	|
	<a href="https://github.com/ICS-Izmir/News-Website/issues"><img src="https://img.shields.io/github/issues/ICS-Izmir/News-Website"></a>
	<br><br>
</p>
<br>

----
### Disclaimer: Website is still in development.

<br>

ICS News Website,<br>
Written with HTML 5, CSS 3, Bootstrap 5, and Python Flask.

## How to run localy :
1. Install the dependencies that are listed in the `requirements.txt` file.
2. Add this to your `hosts` file *1:<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `ics-news.ntw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `www.ics-news.ntw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `blog.ics-news.ntw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `account.ics-news.ntw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `admin.ics-news.ntw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `api.ics-news.ntw`<br>
	
3. In the `config.py` file, change `AppConfig(ProductionConfig)` to `AppConfig(LocalConfig)`
4. In the `config.py` file, change `ANALYTICS_TAG_ID` to your own Google Analytics G- ID. *2
5. In the `config.py` file, change `ANALYTICS_PROPERTY_ID` to your own Google Analytics property ID.
6. Put your Google Service Account credentials JSON file in a folder called `secrets`. Create this folder in the same directory as the `app.py` file. (Rename the file to `ga_creds.json`) *3
7. Create a `vars.env` file in the `secrets` folder that you created and add these to it (change the values to your values) *4:<br>
	`FLASK_SECRET_KEY = "A VERY SECRET STRING"`<br>
	`PASSWORD_ENCRYPT_SALT = "A VERY SECRET SALT"`<br>
	`MAILJET_API_KEY = "MAILJET API KEY"`<br>
	`MAILJET_API_SECRET = "MAILJET API SECRET"`<br>

8. Run the application with: `python app.py`
9. Go to: http://ics-news.ntw:5000/


<br>
*1: If you don't know how to modify your hosts file, take a look at this guide: https://www.howtogeek.com/howto/27350/beginner-geek-how-to-edit-your-hosts-file/<br>
<br>
*2: If you don't know how to get a Google Analytics tracking ID, take a look at this guide: https://support.google.com/analytics/answer/9304153?hl=en&ref_topic=9303319#zippy=%2Cfind-your-g--id-for-any-platform-that-accepts-a-g--id (NOTE: You will be creating the data stream for Web. In the 'Set up data collection' section, go down to 'Find your "G-" ID' then follow those steps and get your G- ID)<br>
<br>
*3: To get this file, create a 'Google Cloud Platform' project, enable the 'Analytics Data API' in the project, go to the 'Credentials' section, create a 'Service Account' and finally go to the 'Keys' tab on your Service Account page then create and download a JSON key.<br>
<br>
*4: To get the Mailjet credentials: Create a Mailjet account, go to 'Account Settings > API Key Management' then create an API key.<br>
<br>
Note: Python 3.11 is recommended.<br>
<br>

## Support :
If you think that you have found a bug please report it <a href="https://github.com/ICS-Izmir/News-Website/issues">here</a>.
<br>
<br>

## Credits :

| Role           | Name                                                                          |
| -------------- | ----------------------------------------------------------------------------- |
| Lead Developer | <a href="https://github.com/samyarsadat">Samyar Sadat Akhavi</a>              |

<br>
<br>

Copyright © 2023 Samyar Sadat Akhavi.
