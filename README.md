# IE481_Data_Visualization

Visualization of KAIST people's daily life
---

### Developers

Chul Hyun Choi

Sangwon Lee

---

### How to run?

We use ABC+MSBAND data - which is is a data fronm KAIST people's smartphone and smartwatch(Microsoft band 2). After make "grouped.csv" from that data, we can run our code with below command.

```
python app.py
```

Our recent implementation : [http://ie481-group2.herokuapp.com/](http://ie481-group2.herokuapp.com/)

---

### About files

* preprocess.ipynb - Preprocess raw data and classify activities and will generate "dataset.csv"

* make_group_from_dataset.ipynb - From "dataset.csv", sort and group the data for each datetime and generate "grouped_dataset.csv"

* Map_visualization.ipynb - code for making map visualizatoin

* assets/map{}.html - map visualization code which is used in our page

* app.py - Used to run both Flask and Dash server

---

### Screenshot

Login Page

![login](https://user-images.githubusercontent.com/43778641/85352334-a8a2d700-b540-11ea-8420-985da4992cbf.JPG)

Main Page

![homepage](https://user-images.githubusercontent.com/43778641/85352338-ae98b800-b540-11ea-9b75-36c8cec999de.JPG)

---

### Requirements

Python 3.7.4

click==7.1.1

dash==1.11.0

dash-core-components==1.9.1

dash-html-components==1.0.3

dash-renderer==1.4.0

dash-table==4.6.2

Flask==1.1.2

Flask-Compress==1.4.0

future==0.18.2

itsdangerous==1.1.0

Jinja2==2.11.1

MarkupSafe==1.1.1

numpy==1.18.2

pandas==1.0.3

plotly==4.6.0

python-dateutil==2.8.1

pytz==2019.3

retrying==1.3.3

six==1.14.0

Werkzeug==1.0.1

xlrd==1.2.0

gunicorn==19.4.5.
