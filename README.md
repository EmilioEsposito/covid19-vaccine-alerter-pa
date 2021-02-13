# COVID-19 Vaccine Appointment Text Alert System - Allegheny County
Author: Emilio Esposito

This is a simple python script that will send an SMS text when vaccine appointments in Allegheny County Pennsylvania (and other various PA locations) are available. 

Currently, the script scrapes the following sites to check for vaccine appointments:

* [Allegheny County Health Department](https://www.alleghenycounty.us/Health-Department/Resources/COVID-19/COVID-19-Vaccine-Information.aspx)
* [Armstrong Center for Medicine & Health](https://acmh.appointlet.com/)
* [RiteAid](https://sr.reportsonline.com/sr/riteaid/PS2021)

**Disclaimer: Please don't rely on this as your only source of trying to schedule a vaccine appointment. I'm trying to keep it as up to date as possible but the landscape is changing very quickly. Please still consult the PA state website regularly:**

https://www.health.pa.gov/topics/disease/coronavirus/Vaccine/Pages/Vaccine.aspx#map

Pull Requests are welcome if you want to improve it or add more sites to scrape. You can request new mobile numbers be added to the list via this [Google Form](https://forms.gle/VTMbCTuKnQwB6cSi9)

This script is currently running on AWS EC2 via a cron job that I can set to run every X minutes (currently every 10 minutes). The EC2 instance is owned by my rental business (Sernia Capital LLC), which can bear all hosting/SMS costs (Twilio is relatively cheap, we can handle over 100k messages before the cost would become material).


