Folder map
CodeAlpha_All_Projects.zip
|
|-- CodeAlpha_NetworkSniffer/        (Task 1, GitHub repo 1)
|   |-- sniffer.py                   main program, captures and prints packets
|   |-- find_iface.py                helper, finds the adapter that has traffic
|   |-- requirements.txt             just "scapy"
|   |-- README.md
|
|-- CodeAlpha_PhishingAwareness/     (Task 2, GitHub repo 2)
|   |-- index.html                   whole module: lessons + quiz in one file
|   |-- README.md
|
|-- CodeAlpha_SecureCodingReview/    (Task 3, GitHub repo 3)
    |-- vulnerable_app.py            app with 8 planted flaws (demo only)
    |-- audit.py                     scanner that finds the flaws
    |-- REPORT.md                    findings table and fixes
    |-- secure_app.py                same app, all flaws fixed
    |-- README.md
How each one flows
Task 1:  network traffic --> sniffer.py --> printed lines + summary
                                ^
                          find_iface.py picks the right adapter

Task 2:  index.html --> lessons (read) --> quiz (click) --> score

Task 3:  vulnerable_app.py --> audit.py --> REPORT.md --> secure_app.py
         (bad code)          (find)         (explain)     (fix)
Quick overview
	Task 1 Sniffer	Task 2 Phishing	Task 3 Code review
Topic	How data travels	How people get tricked	How code gets hacked
Language	Python (Scapy)	HTML, CSS, JavaScript	Python (Flask)
Run it	python -u sniffer.py -c 20 (as Administrator)	Open index.html	python audit.py vulnerable_app.py
What you show	Packets, ports, DNS, handshake	Lessons, then the quiz	8 findings, then the fixed code
Key idea	Packets are layered, HTTPS hides the payload	Urgency and fake domains are the giveaways	Never trust user input
Status	Works on your machine	Not opened in a browser by me	Scanner tested: 8 findings on the bad app, 0 on the fixed one
