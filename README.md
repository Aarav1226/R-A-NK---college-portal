Rank Portal

An interactive, data-driven Rank Portal application designed to track, analyze, and visualize ranking metrics efficiently. Built with Python and Streamlit, this portal provides an intuitive user interface for seamless data interaction.

Features

Interactive Dashboards: Real-time visualization of ranking metrics and performance data.

Dynamic Filtering: Sort and filter data based on custom parameters.

Responsive UI: Clean and accessible interface powered by Streamlit.

Secure Configuration: Centralized management for environment variables and secrets.

Built With

Python

Streamlit

Pandas (Assuming data manipulation)

Configuration Management

This project uses standard Python environment management and Streamlit's built-in configuration tools to ensure smooth deployment and execution.

Dependencies: All required packages are pinned in the requirements.txt file to ensure reproducible builds across different environments.

Environment Variables & Secrets:

If your application requires API keys or database credentials, Streamlit manages these via the .streamlit/secrets.toml file.

Note: The secrets.toml file should NEVER be committed to version control. Ensure it is added to your .gitignore.

Streamlit Config: UI and server settings (like themes, port configurations, and file watcher types) can be managed in .streamlit/config.toml.

Getting Started

Follow these instructions to set up and run the Rank Portal on your local machine.

Prerequisites

Python 3.8 or higher installed on your system.

Git for cloning the repository.

Installation

Clone the repository:

git clone https://github.com/Aarav1226/R-A-NK---college-portal.git
cd rank-portal


Create a virtual environment:

python -m venv venv


Activate the virtual environment:

On Windows: venv\Scripts\activate

On macOS/Linux: source venv/bin/activate

Install required dependencies:

pip install -r requirements.txt


Set up configuration (if applicable):

Create a .streamlit folder in the root directory.

Add a secrets.toml file inside it for any private API keys or database URIs required by the app.

Running the Application

Once the setup is complete, you can launch the Streamlit app using the following command:

streamlit run app.py


(Note: Replace app.py with the actual name of your main Python file if it is different).
