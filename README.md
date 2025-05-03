CO2 Refrigeration Data Analysis
Overview
This repository contains Python scripts for analyzing refrigeration system data, specifically focusing on CO₂-based systems. The code processes time-series data from various sensors, computes thermodynamic properties, and applies polynomial models for efficiency analysis.

Key components include:

Data processing with Pandas and NumPy.

Reading and cleaning CSV files containing refrigeration system parameters.

Implementing thermodynamic calculations using TDN and PSI modules.

Applying polynomial models for compressor efficiency estimation.

Moving average smoothing for enhanced data analysis.

Time synchronization and adjustments between datasets.

Dependencies
To run the scripts, ensure the following Python packages are installed:

bash
pip install pandas numpy
Additionally, the TDN and PSI modules must be available for thermodynamic calculations.

Data Structure
The script processes CSV files containing refrigeration system data. Key variables include:

Temperature sensors: Suction, discharge, intercooler, evaporation temperatures.

Pressure readings: Compressor suction and discharge pressures.

Mass flow rates: Refrigerant flow across different system sections.

Power consumption: Compressor power draw at various stages.

Functionality
Reads and cleans CSV data using pandas.

Computes enthalpy and thermodynamic properties.

Evaluates compressor efficiency with polynomial models.

Performs moving average smoothing on key variables.

Writes processed data to new CSV files for further analysis.

Usage
To run the data analysis:

python
python main.py
Modify the dataset paths and parameters in main.py as needed to analyze different refrigeration system configurations.

License
This project is intended for research and development purposes within the framework of Horizon 2020. 


![image](https://github.com/user-attachments/assets/c2bf8054-e439-4b91-bddf-c8dffc0eba33)
