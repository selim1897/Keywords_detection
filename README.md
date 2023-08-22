# Keywords Detection Web App

The Keywords Detection Web App is a Streamlit-based web application designed to help users find synonym words in Excel files. It provides a simple and user-friendly interface for detecting keywords based on a customizable dictionary (JSON file).

## Overview

Many times, keywords can be written in various ways, and it's essential to identify these variations for tasks like data analysis, content optimization, or search engine optimization (SEO). For example, the term "Google Ads" can appear in multiple forms, such as "googleads," "google ads," "adwords," "google advertising," "search ads," and "google ad campaign." This app helps users detect and standardize such keywords.

## Features

- **Customizable Dictionary**: The app relies on a dictionary (provided as a JSON file) that users can easily modify through the data interface. This allows users to adapt the keyword detection to their specific needs.

- **User-Friendly Interface**: The web app provides an intuitive user interface, making it accessible to users with various levels of technical expertise.

## Usage

To run this project, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/selim1897/Keywords_detection.git

2. Install the required dependencies

   ```
   pip install streamlit pandas mass-analytics
   ```

3. Navigate to the project directory:

   ```
   cd keywords_detection
   ```
4. Execute the following command to start the Streamlit app:

   ```
   streamlit run input.py
   ```
