Boston Crash Modeling
===================

Outline:
-----------------------
 1. Project Vision
 2. How
 3. Connect
 4. Details
 5. Data Sources
 6. Getting Started

 
Project Vision
-----------------------
On Jan 25th, 2017, [9 pedestrians were hit in Boston by vehicles](http://www.bostonherald.com/news/local_coverage/2017/01/battle_for_safer_streets_nine_pedestrians_hit_in_boston_in_1_day). While this was a particularly dangerous day, there were 21 fatalities and over 4000 severe injuries due to crashes in 2016 alone, representing a public health issue for all those who live, work, or travel in Boston. The City of Boston would like to partner with Data For Democracy to help develop a dynamic prediction system that they can use to identify potential trouble spots to help make Boston a safer place for its citizens by targeting timely interventions to prevent crashes before they happen. 

This is part of the City's long-term [Vision Zero initiative](http://www.visionzeroboston.org/), which is committed to the goal of zero fatal and serious traffic crashes in the city by 2030. The Vision Zero concept was first conceived in Sweden in 1997 and has been widely credited with a significant reduction in fatal and serious crashes on Sweden’s roads in the decades since then. Cities across the United States are adopting bold Vision Zero initiatives that share these common principles. 

> Children growing up today deserve...freedom and mobility. Our seniors should be able to safely get around the communities they helped build and have access to the world around them. Driving, walking, or riding a bike on Boston’s streets should not be a test of courage.
> 
> — Mayor Martin J. Walsh


Connect
-----------------------
Join our [Slack channel](https://datafordemocracy.slack.com/messages/p-boston-crash-model) on the D4D Slack. If you haven't joined our Slack yet, fill out [this contact form](http://datafordemocracy.org/contact.html)!

Leads:
 - our project manager Cat Murdock [@catsinthecloud](https://datafordemocracy.slack.com/messages/@catsinthecloud)
 - Alex Chen (CoB) [@alchenist](https://datafordemocracy.slack.com/messages/@alchenist)
 - Ben Batorsky (CoB) [@bpben](https://datafordemocracy.slack.com/messages/@bpben)
 
**Maintainers**: Maintainers have write access to the repository. They are responsible for reviewing pull requests, providing feedback and ensuring consistency.
 - {Your name here?}


Getting Started
-----------------------
### Contributing:
- **"First-timers" are welcome!** Whether you're trying to learn data science, hone your coding skills, or get started collaborating over the web, we're happy to help. If you have any questions feel free to pose them on our Slack channel, or reach out to one of the team leads. If you have questions about Git and GitHub specifically, our [github-playground repo](https://github.com/Data4Democracy/github-playground) and the [#github-help](https://datafordemocracy.slack.com/messages/github-help) Slack channel are good places to start.
- **Feeling comfortable with GitHub, and ready to dig in?** Check out our GitHub issues and projects. This is our official listing of the work that we are planning to get done.
- **This README is a living document:** If you see something you think should be changed, feel free to edit and submit a pull request. Not only will this be a huge help to the group, it is also a great first PR!
- **Got an idea for something we should be working on?** You can submit an issue on our GitHub page, mention your idea on Slack, or reach out to one of the project leads.

### Dependencies:
Most of the work on this project so far has been done in Python, in Jupyter notebooks. 
- Python 2.7 (we recommend [Anaconda](https://www.continuum.io/downloads)) 
- conda (included with Anaconda)

### Environment:
You'll want to reproduce the packages and package versions required to run code in this repo, ideally in a virtual environment to avoid conflicts with other projects you may be working on. We've tested the environment.yml file on a Windows 64-bit machine and Linux and have done our best to ensure cross-platform compatibility, but if it doesn't work for you, please file an issue.

    $ conda env create -f environment.yml
    $ activate boston-crash-model
    
### Data:
Building off of [Vision Zero crash data](http://app01.cityofboston.gov/VisionZero) & the [Vision Zero concerns map](http://app01.cityofboston.gov/VZSafety).