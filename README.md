# Library Usage in Seattle 2005-2020

#### *Note*: This project is in its early (data analysis) stages. 

## Summary
Using a dataset entitled [Checkouts by Title (Physical Items)](https://data.seattle.gov/Community/Checkouts-By-Title-Physical-Items-/5src-czff) (courtesy of [Seattle Open Data](https://data.seattle.gov/)), I explore how a library is used and which items are the most popular, with the ultimate goal of developing and building time series models to forecast future library usage. I have begun analyzing total checkouts, as well as more specific categories of checkouts, to see how those numbers fluctuate over time. This will be the basis for my eventual time series models.

The original dataset is incredibly large (over 106.5 million datapoints with 13 columns, as well as an additional 7 columns that could be added via the [data dictionary](https://data.seattle.gov/Community/Integrated-Library-System-ILS-Data-Dictionary/pbt3-ytbc), so dealing with that has been key to progressing through this project. I created a dataset that is 106.5 million datapoints and 7 columns and takes about 15 minutes to load, as compared to several hours.

## Objectives
1. Create a custom dataset with only necessary columns combined with the data dictionary indicating the format and categories of each item checkout.
2. Explore the most popular items, formats, categories, etc.
3. Look for any long-term and short-term trends as total checkouts relate to time.
4. Build a time series model to forecast library usage in the future, as well as ennumerate the pandemic's effect on the library.
5. Develop an interactive dashboard to display charts and forecasts.

## Findings
TBD

## Conclusions
TBD

## Next steps
The current dataset I'm working with was downloaded on December 15, 2020. The open data portal for this dataset is updated weekly, so in the future, I would like to add [API](https://dev.socrata.com/foundry/data.seattle.gov/5src-czff) calls into the pipeline, in order to quickly and easily add on the additional weekly data.

## Repo structure
```
.
|____01_data_cleaning.ipynb  # notebook to extract and transform original dataset
|____charts  # folder containing data visualizations
| |____total_checkouts_line.png
| |____format_subgroup_counts.png
| |____category_group_counts.png
| |____missing_values_year_bar.png
| |____yearly_percent_print_media_stackedbar.png
| |____checkouts_holiday_violin.png
| |____total_print_media_checkouts_yearly_2005-2020_line.png
| |____equipment_counts.png
| |____top25_books_adult_hbar.png
| |____top25_books_hbar.png
| |____checkouts_weekend_vs_weekday_violin.png
| |____age_group_counts.png
| |____total_checkouts_equipment_yearly_2015-2020_line.png
| |____yearly_weekday_average_bar.png
| |____missing_values_holiday.png
| |____missing_values_day_x_year_bar.png
| |____top25_books_adult_nonfiction_hbar.png
| |____greatest_hits_genre_counts.png
| |____format_group_counts.png
| |____missing_values_day_bar.png
| |____average_checkouts_day_bar.png
| |____missing_values_holiday_bar_stack.png
| |____yearly_total_print_media_stackedbar.png
| |____top25_books_adult_fiction_hbar.png
| |____total_checkouts_yearly_bar.png
| |____top25_books_teen_hbar.png
| |____top10_tapes_hbar.png
| |____top25_books_kids_hbar.png
| |____format_subgroup_counts_top6.png
| |____top25_movies_hbar.png
| |____percent_checkouts_equipment_yearly_bar.png
| |____total_checkouts.png
| |____top10_kids_movies_hbar.png
| |____total_checkouts_yearly_line.png
| |____top10_documentaries_hbar.png
|______init__.py  # file connecting to functions folder
|____README.md  # this file!
|____.gitignore  # files to ignore
|____02_eda.ipynb  # notebook to analyze and visualize data 
|____functions  # folder with custom functions
| |______init__.py  # file connecting to functions folder
| |____data_cleaning.py  # data cleaning and loading functions
| |____data_transform.py  # data transformation functions
```