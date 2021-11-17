This project grabs stock data from the marketwatch api and creates a csv with the current price and how many shares I own of each stock, (using placeholders for now) Merril lynch doesn't have a good stock api so I created this to visualize my data.
There are two versions one using airflow, one not using airflow. Airflow requires some dockerconfigs from the user in order to retrieve the csv's and is really not needed, you can schedule with cron or windows scheduler. 
There is alot of  over-engeering and this could be way more effiecnt than it is, but its a side project for fun so that's intentional.
Plan to visualize with powerbi or python once I have a few couple months of data.
