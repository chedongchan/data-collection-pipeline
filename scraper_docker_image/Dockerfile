# Specify image:tag
# single line for RUN commands.
FROM python:3.9
RUN pip install --no-cache-dir --upgrade pip

# Download and install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
    apt-get update && apt-get -y install google-chrome-stable

#Download and install ChromeDriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
    apt-get install -yqq unzip &&\
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Copy data from docker context
COPY . .

# Install the required modules for scraper.
RUN pip install -r requirements.txt

# Afterwards, we run container with this command
ENTRYPOINT ["python3", "scraper/main.py"]

