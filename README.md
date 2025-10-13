# Harvard Artifacts Dashboard

**Version:** 0.0.6
**Release Date:** 13-10-2025
**Author:** Prasath RK
**Contact:** [LinkedIn](https://www.linkedin.com/in/prasath-rk-552076258/)

---

## Overview

The **Harvard Artifacts Dashboard** is a Streamlit-based application that provides a full **ETL (Extract, Transform, Load) pipeline** for exploring, storing, and analyzing artifact data from the [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api).

This dashboard allows researchers, students, and art enthusiasts to **fetch, visualize, and analyze metadata, media, and color information** for thousands of artifacts in an interactive, user-friendly interface.

---

## 🔹 Key Features

### 1. Dynamic Data Extraction

* Connects securely to the Harvard Art Museums API using your API key.
* Supports paginated data retrieval with **start and end page selection**.
* Filters artifacts by **classification**, now dynamically populated with **live object counts** from the API.
* Shows progress bars and success notifications during data fetching.

### 2. Data Transformation

* Structures API responses into three main DataFrames:

  * **artifact_metadata** – general artifact details (title, culture, period, medium, etc.)
  * **artifact_media** – media statistics (image count, rank, date range, etc.)
  * **artifact_colors** – color composition (hue, spectrum, percent coverage, etc.)
* Stores data in `st.session_state` for instant display and database insertion.

### 3. Data Loading

* Inserts cleaned data into a **local SQLite database** (`harvard_db.sqlite3`).
* Avoids duplicates using `INSERT OR IGNORE`.
* Displays real-time metrics for each table (metadata, media, colors) using **styled cards**.

### 4. Reporting & Analytics

* Generates **main and sub-reports** with SQL queries from the sidebar:

  * Byzantine Artifacts (11th Century)
  * Department-wise Artifact Counts
  * Average Media Rank
  * Color-based Analysis (Hue, Frequency, Percent Coverage)
  * Join reports across Metadata, Media, and Color tables
* Supports dynamic charting:

  * Century-wise artifact counts
  * Classification distribution
  * Average color coverage per classification

### 5. User Interface Enhancements

* Interactive sidebar for classification, page selection, and report generation.
* Version and API status displayed in sidebar.
* Optimized loading and streamlined UI for a smooth user experience.

---

## 🔹 What’s New in v0.0.6

* **Dynamic Classification Selector:** Populates dropdown with real-time data from API including object counts.
* **UI Improvements:** Sidebar, header, and metrics sections updated for clarity and usability.
* **Performance Optimization:** Faster loading of data and rendering in Streamlit.

---

## 🛠️ Dependencies

* Python 3.8+
* [Streamlit](https://streamlit.io/)
* [Requests](https://docs.python-requests.org/)
* [Pandas](https://pandas.pydata.org/)
* [SQLite3](https://docs.python.org/3/library/sqlite3.html)

Install dependencies using:

```bash
pip install streamlit requests pandas
```

---

## ⚙️ Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/harvard-artifacts-dashboard.git
cd harvard-artifacts-dashboard
```

2. Run the Streamlit app:

```bash
streamlit run harvard_artifacts_dashboard.py
```

3. Enter your **Harvard API key** in the sidebar.
4. Select classification, start/end page, and collect data.
5. View data in **JSON** or **DataFrame** formats.
6. Insert into **SQLite DB** and generate reports.
7. Explore charts and analytics via the sidebar options.

---

## 📊 Database Schema

| Table             | Description                                          |
| ----------------- | ---------------------------------------------------- |
| artifact_metadata | General artifact info (title, culture, period, etc.) |
| artifact_media    | Media stats linked by object ID                      |
| artifact_colors   | Color composition linked by object ID                |

---

## 📄 Footer / Credits

* Built with 🌍 by **Prasath Rk**
* Data Source: [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api)
* Version 0.0.6 – Release Date: 13-10-2025
