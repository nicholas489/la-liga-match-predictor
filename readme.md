# La Liga Match Predictor

This repository predicts the outcomes of La Liga football matches using machine learning and provides tools to scrape and prepare the necessary match data.

---

## Features

- **Data Scraping**:  
  - `data_scraper.py` uses Selenium and BeautifulSoup to automatically scrape historical La Liga match data (including advanced stats) from [fbref.com](https://fbref.com).
  - Scrapes multiple seasons and teams, merges match and shooting stats, and saves the results to `matches.csv`.

- **Machine Learning Prediction**:  
  - `machine_learning.py` loads the scraped data, performs feature engineering (including rolling averages and categorical encoding), and trains a Random Forest classifier to predict match outcomes (win/loss).
  - Outputs model precision and a confusion matrix for evaluation.

---

## How It Works

### 1. Data Scraping (`data_scraper.py`)

- Uses Selenium to navigate `fbref.com` and BeautifulSoup to parse HTML.
- For each of the last 3 seasons:
  - Finds all La Liga teams and their match results.
  - Scrapes both match results and detailed shooting stats.
  - Merges these datasets and appends them to a master DataFrame.
- Saves the combined data as `matches.csv` for use in model training.

### 2. Machine Learning (`machine_learning.py`)

- Loads `matches.csv` and processes the data:
  - Encodes categorical features (venue, opponent).
  - Extracts time and day-of-week features.
  - Computes rolling averages for key match statistics (goals, shots, distance, etc.).
- Splits the data into training and test sets based on date.
- Trains a Random Forest classifier to predict match outcomes.
- Evaluates the model and prints precision and a confusion matrix.

---

## Usage

### 1. Install Dependencies

Make sure you have Python 3. Install the required libraries:

```
pip install -r requirements.txt
```

You will also need:
- [Firefox browser](https://www.mozilla.org/firefox/)
- [Geckodriver](https://github.com/mozilla/geckodriver/releases) (for Selenium)

### 2. Scrape Data

Run the scraper to generate `matches.csv`:

```
python data_scraper.py
```

> **Note:** Scraping may take several minutes and requires an internet connection.

### 3. Run the Predictor

Once `matches.csv` is available, run the machine learning script:

```
python machine_learning.py
```

This will output the model's precision and a confusion matrix.

---

## Customization

- **Scraper**:  
  - Adjust the number of seasons or stats scraped in `data_scraper.py`.
- **Model**:  
  - Tune hyperparameters or add new features in `machine_learning.py` for better accuracy.

---

## Requirements

- pandas
- scikit-learn
- selenium
- beautifulsoup4

(See `requirements.txt` for the full list.)

---