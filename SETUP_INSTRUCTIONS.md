# Sasya-Mitra Setup Instructions

This document provides step-by-step instructions to set up Sasya-Mitra with your agricultural datasets.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- Node.js 14 or higher
- npm (Node Package Manager)

## Step 1: Install Python Dependencies

Run the dependency installer to ensure all required Python packages are installed:

```bash
python install_dependencies.py
```

This will install:
- pandas (for data processing)
- numpy (for numerical computations)
- scikit-learn (for machine learning)
- xgboost (for gradient boosting models)
- joblib (for model serialization)

## Step 2: Place Your Datasets

Place all your CSV files in the `data/` directory. The required files are:

1. `Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv`
2. `1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv`
3. `All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv`
4. `All India level Area Under Principal Crops from 2001-02 to 2015-16.csv`
5. `Production of principle crops.csv`
6. `price.csv`

## Step 3: Verify Dataset Processing

Test that your datasets can be loaded and processed correctly:

```bash
python data/test_dataset_processing.py
```

This script will:
- Check that all required files are present
- Load each dataset and display basic information
- Verify that the data can be processed correctly

## Step 4: Install Node Dependencies

Install all required Node.js dependencies:

```bash
npm install
```

## Step 5: Process Your Datasets

Run the dataset processing script to prepare your data for AI model training:

```bash
npm run model:process-data
```

This will:
- Load all your datasets
- Extract relevant features
- Prepare data for machine learning

## Step 6: Train AI Models with Your Data

Train the AI models using your specific datasets:

```bash
npm run model:train-user
```

This will:
- Train yield prediction models using Random Forest and XGBoost
- Train ROI prediction models
- Save trained models to `models/saved_models/`

## Step 7: Start the Web Application

Start the Sasya-Mitra web application:

```bash
npm run dev
```

The application will be available at http://localhost:5173

## Step 8: Use AI-Powered Recommendations

Once the application is running:
1. Select your preferred language
2. Log in or create an account
3. Navigate to the AI Planner section
4. Enter your farm details
5. Receive personalized recommendations based on your datasets

## Troubleshooting

### Missing Python Packages
If you encounter errors about missing Python packages, run:
```bash
pip install pandas numpy scikit-learn xgboost joblib
```

### Dataset Loading Errors
If datasets fail to load:
1. Verify all required CSV files are in the `data/` directory
2. Check that file names match exactly (including special characters)
3. Ensure CSV files are properly formatted

### Model Training Issues
If model training fails:
1. Ensure you have at least 2-3 data points in your datasets
2. Check that your datasets contain the expected columns
3. Verify that numeric data is properly formatted

## Next Steps

After successful setup:
1. Explore the AI recommendations in the web application
2. Review model performance in the console output
3. Customize the models based on your specific needs
4. Add more datasets to improve prediction accuracy

For any issues or questions, please refer to the documentation or contact support.