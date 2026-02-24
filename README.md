#What Makes a Painting Display-Worthy at the Met?
#Predicting Gallery Display Likelihood at The Metropolitan Museum of Art

This project uses data from The Met Museum's open-access collection to investigate which paintings end up on gallery walls and which remain in storage. It combines data collection via API, data cleaning and feature engineering, exploratory data analysis using SQL, classification modelling, and hypothesis testing to identify the key drivers of display likelihood across 9,005 paintings.

It was completed as the final project for the Ironhack Data Analytics Bootcamp (February 2026). It was a genuinely enjoyable project to work on, and the hope is that the findings and tools here are useful to anyone working in collection management or curatorial planning who wants to understand what patterns drive display decisions at scale.

---

#Project Structure

```
met_paintings_display_analysis/
│
├── data/
│   ├── raw/                        # Raw dataset from notebook 01
│   ├── clean/                      # Cleaned dataset from notebook 02
│   └── viz/                        # Exported CSVs for Tableau visualisation
│       ├── tableau_paintings.csv
│       ├── tableau_departments.csv
│       ├── tableau_tags.csv
│       ├── tableau_tags_top20.csv
│       ├── tableau_tags_bottom20.csv
│       ├── tableau_acquisition.csv
│       ├── tableau_size.csv
│       └── tableau_collection_age.csv
│
├── images/                         # Charts and visualisations from EDA
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_cleaning_and_features.ipynb
│   ├── 03_eda_and_sql.ipynb
│   ├── 04_modelling.ipynb
│   ├── 05_hypothesis_testing.ipynb
│   └── 06_louvre_comparison.ipynb
│
├── met_paintings_display_analysis.twbx   # Tableau workbook
├── painting_assessor.py                  # Interactive display likelihood tool
└── README.md
```

---

#Notebooks Overview

Of 9,005 paintings identified in the CSV, 7,333 were successfully enriched via the live API (81.4% coverage). The remaining 18.6% had missing height and width data, reflecting a combination of potential deaccessions since the CSV was published and API retrieval failures. Analysis proceeds on the 9,005 painting dataset with median imputation applied to missing numeric values in notebook 02.

01_data_collection.ipynb
Downloads The Met Museum's full collection CSV from GitHub (approximately 470,000 objects), filters to paintings only, then enriches each painting with structured measurements and subject tags via The Met's Collection API. Creates the is_on_display target variable from live API gallery number data only — the CSV is not used as a fallback, since it is up to three years old and display status changes regularly. Saves the raw dataset for cleaning.

Output: data/raw/met_paintings_raw.csv

Note: this notebook makes approximately 9,005 API calls with a 100ms delay between requests and takes around two hours to complete. The raw CSV download from GitHub is approximately 300MB. Both are one-time operations. If you already have the raw dataset, skip directly to notebook 02.

02_cleaning_and_features.ipynb
Takes the raw dataset and prepares it for analysis and modelling. Handles missing values using department-grouped medians rather than global medians, cleans and standardises existing columns, and engineers new features including painting age, years in collection, area in cm², log-transformed size features, aspect ratio, portrait orientation flag, artist work count, acquisition type, historical era, cultural origin group, recently acquired flag, accession year unknown flag, and collaborative work flag. Encodes categorical variables for modelling. Saves the clean dataset.

Output: data/clean/met_paintings_clean.csv

03_eda_and_sql.ipynb
Loads the clean dataset into SQLite and uses SQL queries alongside pandas and matplotlib to explore display patterns across departments, nationalities, mediums, sizes, and time periods. Identifies the most promising features for modelling and documents key findings. Saves charts to the images folder.

Output: EDA charts in images/

04_modelling.ipynb
Builds three classification models (decision tree, logistic regression, random forest) to predict whether a painting is on display. Explicitly excludes gallery_number from features to prevent data leakage. Includes statistical feature testing, model comparison, hyperparameter tuning via GridSearchCV, and cross-validation. Documents model performance and feature importances.

Output: model performance metrics, feature importance rankings, odds ratios

05_hypothesis_testing.ipynb
Tests five specific hypotheses about display likelihood using Mann-Whitney U tests, chi-squared tests, and tag-level analysis. Constructs a composite profile of the ideal display-worthy painting. Exports clean CSVs for Tableau visualisation.

Output: data/viz/ — all Tableau export files

06_louvre_comparison.ipynb
Collects and cleans a dataset of 10,673 Louvre paintings via the Louvre's public API and web scraping. Compares display patterns between the two institutions across acquisition type, collection age, geographic origin, and gallery space. Includes chi-squared tests and Cramér's V calculations for both datasets.

Output: comparative statistics and charts

---

#Painting Assessor Tool

The repository includes an interactive command-line tool that estimates the likelihood of a painting being displayed at either the Met or the Louvre, based on its characteristics.

To run it, open a terminal in the project directory and run:

```bash
python painting_assessor.py
```

The tool asks seven questions covering acquisition type, period, medium, geographic origin, subject matter, size, and condition. It then produces a display likelihood score for each institution alongside a comparison to their respective collection averages. It is a heuristic tool derived from statistical patterns in the collection data rather than a guarantee of any curatorial decision, but it is a useful way to explore how different characteristics interact and to make the findings tangible.

---

#Key Findings

Overall display rate: Only 15.3% of Met paintings are on display at any given time. The remaining 84.7% are in storage.

Hypothesis 1 — proved: Displayed paintings are statistically significantly larger than stored ones, with a median area of 4,839 cm² versus 3,434 cm². Very small paintings are at the greatest disadvantage.

Hypothesis 2 — proved: Acquisition type is a significant predictor of display status (Cramér's V 0.257). Bequests have a display rate of 29.3%, more than double that of gifts at 9.1%, despite gifts accounting for 55% of the collection.

Hypothesis 3 — proved with caveat: Paintings held longer are more likely to be on display (point-biserial correlation 0.109), but the relationship is non-linear. Display likelihood dips in the 21–40 year band before rising steadily, peaking at 22.2% for paintings held 81–100 years.

Hypothesis 4 — not proved: The nationality group with the highest display rate is Italian (53.6%), not American. French (43.2%) and Flemish (41.3%) follow. A composite profile of the ideal Met painting can be constructed, but its predicted display probability is only 19.1%, confirming that display-worthiness is multifactorial.

Hypothesis 5 — proved: Christian religious subjects are displayed at four to five times the overall average rate. Jesus (69.8%), Virgin Mary (61.4%), and multiple saints all exceed 60%. Non-Western religious and cultural subjects including Buddhist and Hindu iconography returned display rates of 0–2.6% despite sufficient sample sizes. This is arguably the strongest qualitative finding in the project.

Met vs Louvre comparison: The Louvre displays 26.7% of its paintings, compared to 15.3% at the Met. This gap is not explained by gallery space — the Met actually allocates 67% more floor space per displayed painting than the Louvre, suggesting the difference is driven by curatorial policy and collection management decisions rather than physical capacity. Acquisition type is a stronger predictor of display at the Met (Cramér's V 0.257) than at the Louvre (0.133 once category fragmentation is controlled for).

Best model: The tuned random forest achieved 90.2% accuracy and an F1 score of 71.0% on the test set, correctly identifying 77.9% of displayed paintings at a precision of 65.2%.

---

#Tableau Visualisation

The project includes a Tableau workbook (met_paintings_display_analysis.twbx) with four dashboards covering an interactive overview of the Met collection, display rates by department, predictive feature breakdowns, and a subject matter analysis showing the dominance of Christian iconography versus near-zero display rates for non-Western subjects.

To open the workbook, download Tableau Public (free) from https://public.tableau.com and open the .twbx file directly. All data sources are embedded within the file.

---

#Setup and Installation

This project requires Python 3.9 or above. Install dependencies with:

```bash
pip install pandas numpy requests matplotlib seaborn scikit-learn scipy jupyter
```

Run the notebooks in order, as each one saves its output for the next to load:

```bash
jupyter notebook
```

Then open and run each notebook from 01 to 06 in sequence.

---

#Data Sources

The Met Museum Open Access CSV — full collection metadata published by The Met on GitHub, covering approximately 470,000 objects. Licence: Creative Commons Zero (CC0). Source: https://github.com/metmuseum/openaccess

The Met Collection API — used to enrich each painting with structured measurements and subject tags, and to derive the live is_on_display target variable from gallery number data. Documentation: https://metmuseum.github.io/

Louvre collection data — collected via the Louvre's public API and web scraping for the comparative analysis in notebook 06.

Note: the is_on_display field reflects the state of the collection at the point of data collection and will have changed since.

---

#Limitations

The target variable is a snapshot in time and does not account for paintings rotating on and off display. No data was available on physical condition, conservation status, loan activity, or curatorial strategy, all of which are likely significant factors. Department may act as a proxy for institutional gallery space rather than painting quality. Class imbalance (15.3% displayed) means the model is better at identifying stored paintings than displayed ones. The subject matter analysis reflects tagged paintings only and may not be representative of the full collection. Findings apply to paintings only and cannot be generalised to other object types in either collection.

---

#Creator

Ross Wilson 
Data Analytics Bootcamp
Ironhack
February 2026
