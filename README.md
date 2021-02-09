# covid19-vaccine-alerter-pa

A simple python script that will send an SMS text when a vaccine appointment in Pennsylvania is available. 

Currently, it scrapes the following sites to check for vaccine appointments:

* https://www.alleghenycounty.us/Health-Department/Resources/COVID-19/COVID-19-Vaccine-Information.aspx
* https://sr.reportsonline.com/sr/riteaid/PS2021

PRs are welcome if you want to improve it or add more sites to check. You can email me at emilio@serniacapital.com with a list of phone numbers you would like to add to the SMS recipient alert list (I hope to soon automate the addition of numbers via a Google Form).

This script is running on AWS EC2 instance owned by my rental business (Sernia Capital LLC), which can bear all hosting/SMS costs (Twilio is relatively cheap, we can handle over 100k messages the cost would become material). 
