#!/usr/bin/python
import collections
import sys
from smtplib import SMTP
from email.MIMEText import MIMEText
import datetime
from dateutil.relativedelta import relativedelta

SMTPserver = 'smtp.example.com'
SENDER = 'Oncall@example.com'
RECEIVER = 'list@example.com'
SUBTYPE = 'plain'
ONCALL = "/path/to/oncallList"
now = datetime.datetime.now()
nextweek = now + relativedelta ( weeks =+ 1)
oncallRange = now.strftime("%Y-%m-%d") + " to " +  nextweek.strftime("%Y-%m-%d")
SUBJECT = 'Oncall rotation for ' + oncallRange

myFile=open(ONCALL, 'r+')
onCall=collections.deque(myFile)
# Strip date
onCall.popleft()
onCall.rotate(-1)
myFile.seek(0)
myFile.write(oncallRange + "\n")
while True:
  try:
    holder=onCall.popleft()
    myFile.write(holder)
  except IndexError:
    break
myFile.seek(0)
message = myFile.read()
myFile.close()

try:
  msg = MIMEText(message, SUBTYPE)
  msg['Subject'] = SUBJECT 
  msg['From'] = SENDER
  msg['To'] = RECEIVER

  conn = SMTP(SMTPserver)
  try:
    conn.sendmail(SENDER, [RECEIVER], msg.as_string())
  finally:
    conn.close()

except Exception, exc:
  sys.exit("mail failed; %s" % str(exc) )
exit(1)
