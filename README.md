# captchaAI

This program is designed to crawl and automatically information on the tax website.

The primary objective is to handle captcha challenges and ensure accurate form submissions.

Before running the program, make sure you have installed the required libraries.

## install

1. Install necessary packages

```bash
pip install requests
pip install pillow
pip install selenium
pip install pytesseract
```

2. Installing Tesseract may be a bit challenging
   1. go to the [tesseract website](https://digi.bib.uni-mannheim.de/tesseract/) and download the latest version.
   2. Install the downloaded executable.
   3. Locate the Tesseract-OCR folder in Local/Program Files and save the tesseract.exe and tessdata directory.
   4. Add these two directories to the system's environment variables.
   5. Restart your computer.
3. Install ChromeDriver
   1. Ensure that your Chrome browser and ChromeDriver versions match. You can find a suitable version on the [ChromeDriver download page.](https://chromedriver.chromium.org/downloads)

## User Guide

You only need to use tesseract-web.py and tesseract-web-many.py. Below are the usage instructions.

- tesseract-web
  - Simply modify the variable `number` with the desired value and execute the script. If the process is unexpectedly interrupted, you can restart it.
- tesseract-web-many
  - This script allows you to scrape multiple business registration numbers at once and save the results to a txt file.

If you have any problem, just email me.

## License

This project is licensed under the terms of the [LICENSE](https://github.com/hakuei0115/captchaAI/blob/master/LICENSE.txt).
