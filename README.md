Dudash Daily Brief
Automation setup — prep for Thursday's call

Goal for Thursday: confirm four open decisions below, then paste the credentials into GitHub together. The code is written and attached; nothing needs to be read line by line.
Locked In  vs.  Decide on the Call
Already decided	Needs your call
•	Claude (Anthropic API) writes the script
•	6 free, verified news feeds; FRED grounds macro figures
•	ElevenLabs converts script to audio
•	Gmail sends the finished MP3 + summary	•	Which ElevenLabs voice
•	SMTP App Password vs. Gmail API
•	Test recipient, and for how long
•	Who owns the twice-a-year time change
Credentials to Have Ready
Enter these live on the call, directly into GitHub's encrypted Secrets, not by email.
Secret	Source	Purpose
ANTHROPIC_API_KEY	Anthropic Console	Writes the script
ELEVENLABS_API_KEY	ElevenLabs -> API Keys	Generates audio
ELEVENLABS_VOICE_ID	ElevenLabs -> Voice Library	Which voice is used
FRED_API_KEY	fred.stlouisfed.org (free)	Verifies macro figures
GMAIL_ADDRESS / APP_PASSWORD	Company mailbox -> App Passwords	Sends the email
RECIPIENT_EMAIL	Whoever receives it	The “To” address
Attached Files
•	dudash_brief.py  —  the program: gathers news, writes the script, makes the audio, sends the email
•	daily-brief.yml  —  the schedule; runs the program automatically every weekday
•	requirements.txt  —  the two small libraries the program needs
Call Agenda
1.  Confirm the four open decisions (5 min)
2.  Add the three files to the GitHub repo
3.  Enter the credentials as GitHub Secrets
4.  Run one manual test, confirm the email arrives
5.  Agree on the review window before Steve goes live
