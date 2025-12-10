**Finance Advisor**

Video Demo : https://youtu.be/FGJkVxJe7y8?si=babVRwcfJt8eNhMN

Description:
Finance Advisor is a web application that helps people manage their money in a simple way. I built this project because I noticed that many people have trouble keeping track of their income and expenses. This tool makes it easy to see where your money is going and gives tips on how to save more.With this application, you can record all your financial transactions, check your current balance, and get simple advice about your spending. It works like a personal finance helper that is always available whenever you need it.


Each File Does:


***app.py :
This is the main file that runs the application. It is built using Flask, which is a Python web framework. The file manages all the website routes, like the dashboard, adding transactions, or seeing insights. It also handles the database and makes sure your financial data is saved safely.I chose SQLite for the database because it is simple and does not need a separate server. This makes the app easy to run for anyone. The database automatically creates tables for transactions and goals the first time you run the app.



***templates /dashboard.html :
This file shows the main dashboard where you can see your financial summary. There are three cards: Total Income, Total Expenses, and Current Balance. I used colors to make it easier to understand—green for income, red for expenses, and blue for balance.Below the cards, you can see your last 10 transactions. I limited it to 10 to keep the dashboard clean. If you want older transactions, you can use the API I built.



***templates / add_transaction.html:
This file contains the form to add new transactions. I included dropdown menus for transaction type and category so that data stays organized. Income categories are like Salary or Business, and expense categories are like Food or Transport.The description field is optional because sometimes you just want to quickly add a transaction without extra details.



**templates/ insights.html :
This page shows financial insights and tips. I wanted the app to do more than just track transactions—it should help people improve their money habits. The insights are based on your savings rate and spending patterns.I thought about using machine learning to make advanced tips, but I decided simple advice is better for this version because it is easier to understand and more practical.



**templates/ index.html :
This is the home page. I designed it to be simple and welcoming, so new users can easily understand the main features. The cards on this page explain what each section does.



**finance.db :
This is the database file where all your financial data is stored. I chose a local database instead of cloud storage to keep your information private and secure.



**requirements.txt :
This file lists all the Python packages needed to run the app. It includes Flask for the web framework, pandas for data analysis, and other libraries. This helps others install the same versions I used.



Design Choices and Challenges :
One challenge was handling different ways people might type data. For example, some might type "income" and others "Income". I solved this by making database queries case-insensitive.I also spent time making the interface simple but informative. Colors and clear labels help users quickly understand their finances.Another choice was to include both a web interface and API endpoints. The web interface is for normal users, and the API can be used by developers who want to build apps that connect to this system.The AI insights feature went through several changes. At first, I wanted to build a complex machine learning system, but I realized simple, clear advice is more useful. Now, it gives personalized tips based on your savings and spending patterns.



How to Run the Project :
To run this project, you need Python installed. Download all the project files and run the main file. The application will start, and you can open it in your browser at http://localhost:5000.
If you use GitHub Codespaces, you can open the project there and run the app. The system will automatically set up everything you need.Also This project was developed and tested in GitHub Codespaces.
Here is the temporary live development URL:
https://potential-space-eureka-q7g669w55r9439wq5-5000.app.github.dev/



Final Thoughts:
Building Finance Advisor taught me a lot about web development, databases, and user experience. I am proud of the dashboard, which gives users a clear picture of their finances in one glance.This project shows that simple solutions can be very useful. The main goal was to help people manage money better and save more, and I think this app achieves that.
