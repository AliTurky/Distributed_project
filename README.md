# Distributed_project
-Image processing distributed system using grpc
Project Setup Instructions
Follow these steps to set up and run the project:

Step 1: Download the Files
Client File: Download the client file to your local machine that will function as the client.
Slave Files: Download the slave files to the instances designated as slaves.
Master File: Download the master file to the instances designated as masters.


Step 2: Install Necessary Libraries
Ensure that all required libraries are installed on each instance (masters, slaves) and on your local machine. You can typically install these libraries using pip:

bash
Copy code
pip install -r requirements.txt
Step 3: Run the Masters and Slaves
On the instances that will function as masters and slaves, start the respective scripts by running:

bash
Copy code
python file.py
Step 4: Run the Client
On your local machine, run the client script. Once the client is running, you can start using the application.

Note
Ensure all necessary libraries are installed on each instance and on your local machine to avoid any runtime issues.
By following these steps, you should be able to set up and run the project successfully.
