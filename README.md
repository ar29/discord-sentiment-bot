# Discord Sentiment Analysis Bot with Google Docs Reporting

This project is a Discord bot that performs sentiment analysis on user messages within a Discord server. The bot saves messages, analyzes their sentiment (Positive, Neutral, Negative), and generates reports in a Google Docs file, which can be shared with administrators. The bot also allows for dynamic credit systems based on sentiment scores and includes automatic garbage collection to manage memory.

## Features

- **Sentiment Analysis:** Automatically analyzes and stores the sentiment of Discord messages.
- **Dynamic Credit System:** Rewards users based on the sentiment of their messages.
- **Report Generation:** Creates Google Docs reports summarizing sentiment statistics.
- **PostgreSQL Integration:** Database for storing user data and sentiment scores.
- **Google Docs API Integration:** Exports sentiment data into Google Docs with proper user permissions.
- **Docker Support:** Dockerized environment for easy deployment.
- **AWS Elastic Beanstalk Deployment:** Configured to be deployed to AWS Elastic Beanstalk using Docker.

## Prerequisites

- **Python 3.8+**
- **PostgreSQL Database**
- **Docker**
- **AWS Elastic Beanstalk (for deployment)**
- **Google Cloud Account** (for Google Docs API)

## Local Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/discord-sentiment-bot.git
cd discord-sentiment-bot
```

### Step 2: Set Up Virtual Environment
Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a .env file in the root of the project directory and add the following environment variables:

```bash
DISCORD_TOKEN=<your_discord_bot_token>
POSTGRES_DB=<your_db_name>
POSTGRES_USER=<your_db_user>
POSTGRES_PASSWORD=<your_db_password>
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
GOOGLE_API_CREDENTIALS_PATH=<path_to_credentials_json>
```

### Step 4: Create a Google Cloud Project and OAuth Credentials
1. Visit Google Cloud Console.
2. Create a project and enable the Google Docs and Google Drive APIs.
3. Go to APIs & Services > Credentials, create OAuth 2.0 credentials, and download the credentials.json file.
4. Place the credentials.json file in your project root directory.


### Step 5: Database Setup
Make sure you have PostgreSQL running locally or use a cloud-based instance. Run the following commands to create the necessary tables and migrate the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Running the Bot Locally
Run the bot locally using the Django management command:
```bash
python manage.py run_discord_bot
```
This will start the Discord bot and connect it to your specified server.


### Step 7: Google Docs Integration
When the bot generates a Google Docs report, it will automatically use the provided OAuth credentials to create and manage documents. Make sure the service account created has proper permissions to access and modify Google Docs.

## Running with Docker
### Step 1: Build and Run the Docker Container
You can build and run the bot using Docker for easier management and deployment:

```bash
docker-compose up --build
```
This will set up the entire project, including the PostgreSQL database, and run the bot in a containerized environment.

### Step 2: Accessing the Logs
You can view logs from the running Docker containers using:

```bash
docker-compose logs -f
```

## Deployment to AWS Elastic Beanstalk
### Step 1: Set Up AWS Elastic Beanstalk
Install the AWS Elastic Beanstalk CLI:

```bash
Copy code
pip install awsebcli
```
Initialize your Elastic Beanstalk environment:

```bash
eb init
```
### Step 2: Configure AWS Resources
Ensure you have the appropriate IAM roles for Elastic Beanstalk to use, and make sure your AWS credentials are properly configured in your environment.

### Step 3: Deploy the Application
Deploy the application to AWS Elastic Beanstalk:

```bash
eb create discord-sentiment-app
eb deploy
```
### Step 4: Monitor Deployment
Monitor your Elastic Beanstalk environment:

```bash
eb status
eb logs
```

## Google Docs Report Generation
The bot will automatically generate a Google Docs file containing a report of the sentiment data. Make sure your Google Cloud service account has permissions to create and share Google Docs files.

## Administrative Access
You can log in to the Django admin panel to view and manage user sentiment data by navigating to:

``` bash
http://localhost:8000/admin
```
Use the superuser account you create during the setup.

### Creating a Superuser
```bash
python manage.py createsuperuser
```

### Troubleshooting
#### Common Issues
Bot not connecting to Discord: Double-check your Discord bot token in the .env file.
Database connection errors: Ensure your PostgreSQL credentials and Docker volumes are correctly configured.
Google Docs Access Issues: Ensure your OAuth 2.0 credentials are set up correctly and that the Google service account has sufficient permissions to manage Google Docs.
#### Logs and Debugging
Use docker-compose logs -f to view logs from your Docker containers.
For AWS Elastic Beanstalk deployments, use eb logs to fetch logs from the deployed environment.
Contributing
If you would like to contribute, feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License.


### **Explanation of Sections:**
- **Features:** A clear list of key features provided by the bot.
- **Prerequisites:** Outlines the necessary tools and services to run the bot locally and in production.
- **Setup Instructions:** Guides the user through setting up a virtual environment, configuring environment variables, running migrations, and deploying to Docker and AWS Elastic Beanstalk.
- **Google Docs Integration:** Ensures clarity on how Google Docs reports are created and shared, with steps for setting up OAuth.
- **Docker Instructions:** Helps users who prefer Docker to set up the bot easily.
- **AWS Deployment:** Detailed Elastic Beanstalk deployment steps for users who want to run the bot in a production environment.
- **Troubleshooting:** Provides tips to address common setup or runtime issues.