# Send Mail project

Trung D. Nguyen (trungnguyen@wustl.edu)

### Problem
I choose the "Email Service" project as a full-stack project. The main focus is back-end track while front-end is minimal.

### Solution Overview
The SendMail service is designed to provide a service to users to send mail via either a web-based interface or RESTful API. The service requires the following input:
+ From email: a valid email address, required
+ To email: a valid email address, required
+ CC email(s): an email or a list of email addresses separated by comma, optional
+ BCC email(s): an email or a list of email addresses separated by comma, optional
+ Subject: non-empty string, cannot exceed 1000 characters
+ Content: non-empty string, cannot exceed 10000 characters

The website has a form to allow users to enter the above information. Website: http://trunghello.azurewebsites.net/

The RESTful API accepts above information in JSON format and returns result in JSON format as well. Endpoint: http://trunghello.azurewebsites.net/api/sendmail. Use GET command to see help and sample input/output and use POST command to send emails.

#### Technology choices
The project is designed as a web service with loosly couped components in mind.

- Front end: Very simple and easy to use web page for the user to send email.
- Back end: This is the main service to send email based on data in requests.
 
+ Flask framework with Python: it's lightweight and easy to use and deploy. It seems well-fit for the purpose of this challenge as well. Other available technologies such as Windows Communication Foundation using Microsoft.NET or Java web service can be used as well but Python is just way faster and simpler for this project.
+ Pattern design use:
In the project, inversion of control pattern to choose email sender service is implemented with dependency injection to create a loosely coupled system. This helps
increase modularity, future extensibility, maintainability, and testability.

The service is hosted on Microsoft Azure.

#### Files I wrote
Under FlaskWebProject directory:
- index.html
- site.css (only added few css rules)
- config.py 
- email_service.py
- email_senders.py
- end_to_end_test.ps1
- views.py
- requirements.txt

Other files are generated by Flask framework.

### Testing
Due to my time constraints, I was able to do only manual test for the website and end-to-end test for RESTful APIs using PowerShell script. There is no unit tests or UI automation tests yet.

### Future improvements
+ Add unit tests and UI automation test (very important)
+ On client side (of the website), we can do some basic validation using JavaScript such as emails, lengths of subject and content without the need to send all request to the server.
+ Improve User Interface (error, requirements marked up, etc. ) to make the website looks more attractive and easier to use.
+ Currently we are sending email synchronously. We can try to send mails asynchronously to increase scalability of the system.
+ On server side, usage and reliability loggings should be done for later data analytic and service health monitoring. Based on loggings, we can find out how to improve our service (such as which email sender is more reliable or detect and blacklist spammers, etc.)
+ Add more features to the project such as support sending attachments or scheduling sending emails, etc.

### Links
#### Other codes that I'm proud of
Below is the sample project I did for my Master thesis research (from 2008 - 2011):
+ Full description: http://www.cse.wustl.edu/~nguyent/atlasbuilder.htm
+ Source code: https://code.google.com/p/meshedit/source/browse/

The code is very old but it is a much bigger example of my work over longer period of time.

#### Resume
https://www.dropbox.com/s/z6202sxjp3l1xxx/Trung%20D%20Nguyen%20resume.pdf?dl=0

