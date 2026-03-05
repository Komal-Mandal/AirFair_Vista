
# AirFair_Vista


## Abstract:

Accurate prediction of flight prices plays a crucial role in the travel industry, enabling travelers to plan their journeys effectively and make informed decisions regarding their air travel expenses. This project utilizes data science techniques to predict flight prices based on a comprehensive dataset comprising various attributes and historical flight data. By leveraging the power of data analysis and predictive modeling, this study aims to provide valuable insights into the factors influencing flight prices. Through data exploration, feature engineering, and rigorous model training, this project develops a robust framework for estimating flight prices. While the specific algorithms and techniques employed in this project are not discussed in this abstract, the focus remains on the predictive power of the model and the potential benefits it offers to travelers and airlines alike. Accurate flight price predictions empower travelers to plan their trips more effectively, enabling them to budget and make informed choices regarding their flight bookings. Moreover, airlines can leverage these predictions to optimize revenue management, pricing strategies, and flight availability. By understanding the underlying patterns and trends in flight prices, airlines can better anticipate demand fluctuations and adjust fares accordingly. The project's findings shed light on the key factors influencing flight prices, such as departure location, destination, time of travel, seasonality, airline preferences, and flight duration. This understanding aids travelers in finding the best deals and optimizing their travel plans, while airlines can enhance their pricing strategies and maximize profitability.

# 📌 Project Overview

Airline ticket prices change frequently depending on many factors such as airline, travel date, duration, stops, and routes. Predicting flight prices can help travelers make better booking decisions.

The Flight Price Prediction System is a Machine Learning web application that predicts the price of a flight ticket based on several travel-related features.

This project demonstrates a complete end-to-end Machine Learning pipeline, including:

- Data preprocessing

- Feature engineering

- Exploratory Data Analysis (EDA)

- Model training

- Model evaluation

- Hyperparameter tuning

- Model deployment using Streamlit

- The final model is deployed through a user-friendly web interface where users can enter flight details and instantly receive a predicted ticket price.


# 🧠 Machine Learning Workflow

```
Data Collection
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Exploratory Data Analysis
        ↓
Encoding Categorical Variables
        ↓
Feature Selection
        ↓
Train-Test Split
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Hyperparameter Tuning
        ↓
Model Deployment (Streamlit)
```
# 📊 Dataset Description

The dataset contains historical flight booking information used to train the prediction model.

### Dataset Features

| Feature | Description |
|--------|-------------|
| Airline | Name of airline company |
| Source | Departure city |
| Destination | Arrival city |
| Date_of_Journey | Date of travel |
| Dep_Time | Flight departure time |
| Arrival_Time | Flight arrival time |
| Duration | Total flight duration |
| Total_Stops | Number of stops |
| Price | Flight ticket price |

# 🔍 Exploratory Data Analysis (EDA)

Before building the model, the dataset was analyzed using visualization libraries.

## Libraries used

- Matplotlib

- Seaborn

- Pandas

## Key insights discovered:

- Flights with less stops tend to be cheaper

- Airline company significantly affects ticket price

- Flight duration strongly influences price

- Prices vary depending on journey month and day

- Departure time and arrival time also impact prices

# 🧹 Data Preprocessing

Data preprocessing is one of the most important steps in machine learning.

The following preprocessing steps were performed:

#### Handling Missing Values

- Missing values were removed using:

- dropna()
#### Date Feature Extraction

- The Date_of_Journey column was converted into numerical features:

  - Journey Day
  - Journey Month

- This helps the model understand seasonal price patterns.

#### Time Feature Extraction

- From Departure Time and Arrival Time, the following features were extracted:

    - Departure Hour

    - Departure Minute

    - Arrival Hour

    - Arrival Minute

#### Duration Conversion

- Flight duration was originally in text format:

     - 2h 50m
     - 5h
     - 30m

- This was converted into two numerical features:

    - Duration Hours

     - Duration Minutes

# 🔄 Feature Engineering

- New useful features were created to improve model performance.

- Engineered features include:

    - Journey Day
    - Journey Month
    - Departure Hour
    - Arrival Hour
    - Duration Hours
    - Duration Minutes

Feature engineering helps the model learn hidden patterns in data.

# 🔢 Encoding Categorical Variables

- Machine learning models cannot understand text data.

- Categorical features like:

    - Airline
    - Source
    - Destination

converted using One Hot Encoding.

#### Example:

- Airline → Airline_Indigo, Airline_AirIndia, Airline_SpiceJet

- Each category becomes a binary column.

# 🧮 Feature Selection

- Feature importance was analyzed using:

    - Correlation Heatmap

    - ExtraTreesRegressor

- This helps identify which features influence the flight price the most.

#### Important features included:

- Duration

- Airline

- Total Stops

- Departure Time

# 🤖 Machine Learning Models Used

- Several regression algorithms were trained and compared:

| Model                       | Description                                       |
| --------------------------- | ------------------------------------------------- |
| Linear Regression           | Basic regression model                            |
| Decision Tree Regressor     | Tree-based model for nonlinear relationships      |
| Random Forest Regressor     | Ensemble model combining multiple decision trees  |
| Gradient Boosting Regressor | Boosting algorithm improving prediction accuracy  |
| Support Vector Regressor    | Uses hyperplanes for regression                   |
| XGBoost Regressor           | Advanced boosting algorithm with high performance |



# 📈 Model Evaluation

- Models were evaluated using standard regression metrics.

- Mean Absolute Error (MAE)

- Average absolute difference between predicted and actual price.

- Mean Squared Error (MSE)

- Average squared difference between predicted and actual price.

- Root Mean Squared Error (RMSE)

- Square root of MSE, providing error in original units.

- R² Score Measures how well the model explains variance in data.

- R² Score range: 0 → 1
- Higher value = Better model performance

# 🏆 Final Model Selection

- After testing multiple models, XGBoost Regressor produced the best performance.

#### Why XGBoost?

- High prediction accuracy

- Handles complex relationships

- Built-in regularization prevents overfitting

- Fast training speed

- Efficient for large datasets

- The trained model was saved using:

- joblib.dump()

# 💻 Streamlit Web Application

- The machine learning model was deployed using Streamlit, creating an interactive web interface.

- Users can input flight details and instantly receive predicted ticket prices.

### User Inputs

#### The application allows users to select:

- Airline

- Source

- Destination

- Journey Date

- Departure Time

- Arrival Time

- Total Stops

After entering details, the system predicts the estimated flight ticket price.

# ⚙️ Installation & Setup

Follow these steps to run the project locally.

1️⃣ Clone the Repository
```
git clone https://github.com/Komal-Mandal/AirFair_Vista.git

```

2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

3️⃣ run flightprice

4️⃣ Run the Streamlit Application
```
streamlit run app.py
```

The application will open in your browser.