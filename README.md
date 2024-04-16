# BetterCalendar

### This is Better Calendar! A program that connects to your Google Calendar, designed to make your scheduling experience as easy as possible. It automatically sets reminders for upcoming events, so you never have to worry about when you should leave for your next appointment. 

## Why?
 As a commuter in college, I always worried about being late to class. I constantly calculated in my head how much time it would take for me to get to school and when I needed to leave to make it on time. It stressed me out in the morning and I couldn't account for traffic. 

I created this project so that me, and many others could wake up in peace and end up being late to class anyways.

## How to Use
 1. Clone the repository
 2. Install the required dependencies. Ensure you have Python installed on your machine.
```
pip install -r requirements.txt
```
 4. Obtain your Google Calendar API credentials
   * Go to the Google Developers Console.
   * Create a new project.
   * Enable the Google Calendar API for your project.
   * Create credentials (OAuth 2.0 client ID).
   * Download the credentials JSON file and rename the file to crendentials.json
   * Create a .credentials folder in the root directory of the project
   * Store the credentials.json file in the .credentials folder
  5. Create a config.py file
   * Create a config.py file in the root directory of the project.
   * In the config.py file, Create a variable named key and set it to your API key from Google Maps (Refer back to step 4 but do it for Google Maps API)
   * In config.py
```python
key = "your_api_key_here"
```
  6. Run the application
   * In powershell command line
```
python app.py
```
  7. In your Google Calendar event description, follow these formats:
   * To set a default location:
```
!Default Location: (Address of location)!
```
   * To add extra time before an event:
```
!Extra Time: (# of minutes)!
```
***
> [!IMPORTANT]
> The program only works on the upcoming event. It will not work on any past future events(past the next event)
***
###### Report any bugs or issues in the [Issues](https://github.com/Youssup/BetterCalendar/issues) section of this repository.
