"""
==========================================================================================
 Script Name   : harvard_artifacts_dashboard.py
 Description   :
    This Streamlit application provides an interactive dashboard for exploring,
    storing, and analyzing artifacts from the Harvard Art Museums public API.

    The app performs a full ETL (Extract, Transform, Load) pipeline with integrated
    data visualization and SQL-based reporting features.

    🔹 Key Functionalities:
        1. **Extract (API Data Collection)**
           - Connects to the Harvard Art Museums API using an API key.
           - Fetches paginated artifact data including metadata, media info, and color data.
           - Supports filtering by classification type (e.g., Paintings, Sculptures, etc.).
        
        2. **Transform (Data Processing)**
           - Structures API response data into pandas DataFrames for three main datasets:
             • artifact_metadata
             • artifact_media
             • artifact_colors
           - Displays data in both JSON and DataFrame views.
        
        3. **Load (Database Integration)**
           - Inserts processed data into a local SQLite database (`harvard_db.sqlite3`).
           - Avoids duplicates using `INSERT OR IGNORE` logic.
           - Displays total record counts dynamically for each table.
        
        4. **Reports and Analytics**
           - Allows selection of main and sub-reports from sidebar menus.
           - Generates dynamic SQL queries for insights such as:
               • Byzantine Artifacts (11th Century)
               • Department-wise Artifact Counts
               • Average Media Rank
               • Color-based Analysis (Hue, Frequency, Percent coverage)
               • Multi-table JOIN reports (Metadata + Media + Color)
           - Displays report results as Streamlit DataFrames.

    🔹 Additional Features:
        - Version and release info displayed in sidebar.
        - Progress bars and success notifications for better UX.
        - Sidebar-driven UI for data fetching, inserting, and report generation.

    Database Schema:
        artifact_metadata → General information about each artifact.
        artifact_media     → Media-related statistics linked via objectid.
        artifact_colors    → Color composition details linked via objectid.

 Author          : Prasath RK
 Version         : 0.0.4
 Release Date    : 10-10-2025
 Dependencies    : streamlit, requests, sqlite3, pandas
 Contact         : https://www.linkedin.com/in/prasath-rk-552076258/
==========================================================================================
"""


import streamlit as st
import requests
import sqlite3
import pandas as pd

# Sidebar version info 
st.sidebar.write("Version: 0.0.4") 
st.sidebar.write("Release Date: 10-10-2025")

#TITLE
st.title("🏛️ Harvard Artifacts 🏛️")
#with st.expander("ETL + Visualization + SQL Insert+Dashboard"):  # smaller subtitle
st.markdown("""
Welcome to the **Harvard Artifacts Explorer**!  
Fetch, visualize, and store artifact metadata like a pro.  
🎨 See colors, 🖼️ view media, and 📊 analyze trends in your browser.
""")
st.markdown("---")

# ===========================
# Database Metrics Section
# ===========================

conn = sqlite3.connect("harvard_db.sqlite3")
cursor = conn.cursor()


tables = ["artifact_metadata", "artifact_media", "artifact_colors"]
counts = []

for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        counts.append(cursor.fetchone()[0])

# Display metrics in styled cards
with st.expander("### **Total Records in Database**"):
    col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("📂 artifact_metadata")
    st.metric(label="Records", value=counts[0])
with col2:
    st.markdown("🖼️ artifact_media")
    st.metric(label="Records", value=counts[1])
with col3:
    st.markdown("🎨 artifact_colors")
    st.metric(label="Records", value=counts[2])

conn.close()
st.divider()


# ===========================
# API Data Collection Section
# ===========================
apikey = 'baeae4fa-903c-4cbe-bc8c-16369ea17a35'
url = 'https://api.harvardartmuseums.org/object'
size = '100'

with st.sidebar:
    col1, col2,col3 = st.columns(3)
with col1: 
    min_page=st.number_input("start page", min_value=1, value=1, step=1)
with col2:
    max_pages=st.number_input("End page", min_value=1, value=1, step=1) 
with col3:
    #classification = st.sidebar.text_input("Choose Classification")
    classification =st.selectbox("Choose Classification", ["Coins","Paintings","Sculptures","Furniture","Drawings",
                                                                "Accessories","Prints","Vessels","Textile Arts",
                                                                "Archival Material","Fragments","Manuscripts","Seals",
                                                                "Straus Materials","All"])

# Initialize lists to store data
metadata = []
media = []
colors = []

# Collect Data Button
if st.sidebar.button("**Collect Data**"):
    start_page= min_page
    end_page = max_pages  # number of pages to fetch
    all_records = []
    progress_bar = st.progress(0)
    
    for pg in range(start_page, end_page + 1):
        params = {
            "apikey": apikey,
            "size": size,
            "page": str(pg)
        }
        if classification.strip() != "" and classification != "All":
            params["classification"] = classification

        with st.spinner(f"Fetching data for page {pg}..."):
            response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            page_records = data.get("records", [])
            all_records.extend(page_records)

            # Process only the current page's records to avoid duplication
            for record in page_records:
                metadata.append({
                    "id": record.get("id"),
                    "title": record.get("title"),
                    "culture": record.get("culture"),
                    "period": record.get("period"),
                    "century": record.get("century"),
                    "medium": record.get("medium"),
                    "dimensions": record.get("dimensions"),
                    "description": record.get("description"),
                    "department": record.get("department"),
                    "classification": record.get("classification"),
                    "accessionyear": record.get("accessionyear"),
                    "accessionmethod": record.get("accessionmethod")
                })

                media.append({
                    "objectid": record.get("objectid"),
                    "imagecount": record.get("imagecount"),
                    "mediacount": record.get("mediacount"),
                    "colorcount": record.get("colorcount"),
                    "rank": record.get("rank"),
                    "datebegin": record.get("datebegin"),
                    "dateend": record.get("dateend")
                })

                for c in record.get("colors", []):
                    colors.append({
                        "objectid": record.get("objectid"),
                        "color": c.get("color"),
                        "spectrum": c.get("spectrum"),
                        "hue": c.get("hue"),
                        "percent": c.get("percent"),
                        "css3": c.get("css3")
                    })
                    # Create indvidual  DataFrames for better display
                    df_metadata = pd.DataFrame(metadata)
                    df_media = pd.DataFrame(media)
                    df_colors = pd.DataFrame(colors)
                    
                    # Store df in session_state for later Load (SQL part) 
                    st.session_state["df_metadata"] = df_metadata
                    st.session_state["df_media"] = df_media
                    st.session_state["df_colors"] = df_colors

                    st.session_state["json_metadata"] = metadata
                    st.session_state["json_media"] = metadata
                    st.session_state["json_colors"] = metadata



        else:
            st.error(f"Error fetching page {pg}: {response.status_code}")
            break
        
        # Update progress bar
        progress_bar.progress(pg / end_page)

    st.success(f"Data collection completed! Total records fetched: {len(all_records)}")

import streamlit as st

st.set_page_config(page_title="Harvard Artifacts ETL", layout="wide")

# --- Sidebar Section: Buttons only ---
with st.sidebar:
    st.header("🧭 Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        json_btn = st.button("JSON")
    with col2:
        df_btn = st.button("DataFrame")
    with col3:
        ins_btn = st.button("Insert into DB")

# --- Main Page Section: Display area ---
st.title("🎨 Harvard Artifacts Explorer")

if json_btn:
    if (
        "json_metadata" in st.session_state and
        "json_media" in st.session_state and
        "json_colors" in st.session_state
    ):
        jsonmetadata = st.session_state["json_metadata"]
        jsonmedia = st.session_state["json_media"]
        jsoncolors = st.session_state["json_colors"]

        st.markdown("## 📦 JSON Data Preview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Metadata JSON")
            st.json(jsonmetadata)
        with col2:
            st.subheader("Media JSON")
            st.json(jsonmedia)
        with col3:
            st.subheader("Colors JSON")
            st.json(jsoncolors)
    else:
        st.warning("⚠️ JSON data not found in session state. Please load data first.")

elif df_btn:
    if (
        "df_metadata" in st.session_state and
        "df_media" in st.session_state and
        "df_colors" in st.session_state
    ):
        df_metadata = st.session_state["df_metadata"]
        df_media = st.session_state["df_media"]
        df_colors = st.session_state["df_colors"]

        st.markdown("## 🧾 DataFrames Overview")

        st.markdown("### 🟩 Metadata Table")
        st.dataframe(df_metadata, use_container_width=True)

        st.markdown("### 🟦 Media Table")
        st.dataframe(df_media, use_container_width=True)

        st.markdown("### 🟨 Colors Table")
        st.dataframe(df_colors, use_container_width=True)
    else:
        st.warning("⚠️ DataFrames not found in session state. Please load data first.")

elif ins_btn:
    st.info("💾 Insert to Database feature coming soon!")


 


# ==============================
# Insert into SQL(SQLite3)
# ==============================

if ins_btn:   #By clicking this button Data will insert to to corresponding tables
    if "df_metadata" in st.session_state and "df_media" in st.session_state and "df_colors" in st.session_state:
        df_metadata = st.session_state["df_metadata"]
        df_media = st.session_state["df_media"]
        df_colors = st.session_state["df_colors"]

        conn = sqlite3.connect("harvard_db.sqlite3")
        cursor = conn.cursor()

        # Record total changes before insert
        before = conn.total_changes


        # Insert into artifact_metadata
        cursor.executemany("""
            INSERT OR IGNORE INTO artifact_metadata
            (id, title, culture, period, century, medium, dimensions, description, department, classification, accessionyear, accessionmethod)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, df_metadata.where(pd.notnull(df_metadata), None).values.tolist())

        # Insert into artifact_media
        cursor.executemany("""
            INSERT OR IGNORE INTO artifact_media
            (objectid, imagecount, mediacount, colorcount, rank, datebegin, dateend)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, df_media.where(pd.notnull(df_media), None).values.tolist())

        # Insert into artifact_colors
        cursor.executemany("""
            INSERT OR IGNORE INTO artifact_colors
            (objectid, color, spectrum, hue, percent, css3)
            VALUES (?, ?, ?, ?, ?, ?)
        """, df_colors.where(pd.notnull(df_colors), None).values.tolist())

        conn.commit()

        # Record total changes after insert
        after = conn.total_changes
        rows_inserted = after - before

        conn.close()
        if rows_inserted == 0:
            st.sidebar.warning("record alreday exist")
        else:
            st.sidebar.success(f"✅ Data inserted successfully into SQLite. Total rows affected: {rows_inserted}")

        # Optionally: preview inserted rows
        #st.subheader("Inserted Metadata Preview")
        #st.dataframe(df_metadata.head(10))  # Show first 10 rows
        #st.dataframe(df_media.head(10))  # Show first 10 rows
        #st.dataframe(df_colors.head(10))  # Show first 10 rows
    else:
        st.warning("⚠️ Please fetch data first (Showcase) before inserting.")


#if st.sidebar.button("delete"):
        conn = sqlite3.connect("harvard_db.sqlite3")
        cursor = conn.cursor()

        cursor.execute("delete from artifact_colors")
        conn.commit()



# ==============================
# Genrating Report from SQL DB
# ==============================

with st.sidebar.markdown("Reports"):
    main_report = st.selectbox(
    "Select Main Report",
    [
        "",
        "Artifact Metadata Report",
        "Artifact Media Report",
        "Artifact Color Report",
        "Join-Based Queries"
    ]
)

# =============================
# Sub Report Selection
# =============================
sub_report = None

if main_report == "Artifact Metadata Report":
    sub_report = st.sidebar.selectbox(
        "Select Sub Report",
        [
            "",
            "Byzantine Artifacts (11th Century)",
            "Unique Cultures Represented",
            "Archaic Period Artifacts",
            "Artifacts by Title (Sorted by Accession Year, Descending)",
            "Department-wise Artifact Counts"
        ]
    )

elif main_report == "Artifact Media Report":
    sub_report = st.sidebar.selectbox(
        "Select Sub Report",
        [
            "",
            "More then 1 Image",
            "Avg Rank of Artifacts",
            "color>Mediacount",
            "Created 1500-1600",
            "No Media reports"
        ]
    )

elif main_report == "Artifact Color Report":
    sub_report = st.sidebar.selectbox(
        "Select Sub Report",
        [
            "",
            "Unique HUE",
            "Top 5 most Colors",
            "Average coverage percentage",
            "all colors Artifact ID",
            "Total Colors"
        ]
    )
elif main_report == "Join-Based Queries":
    sub_report = st.sidebar.selectbox(
        "Select Sub Report",
        [
            "",
            "Byzantine Artifacts and Their Color Hues",
            "Artifact Color Mapping",
            "Artifacts by Period with Media Rank",
            "Top 10 Artifacts with Grey Colors",
            "Artifacts per Classification and Media Overview"

        ]
    )
# =============================
# Final check before running
# =============================
if st.sidebar.button("Generate Report"):
    if not main_report or not sub_report:
        st.warning("⚠️ Please select both a Main Report and a Sub Report before generating.")
    else:
        st.success(f"✅ Generating {sub_report} from {main_report}...")

# =============================
# Generate Report Button
# =============================

    conn = sqlite3.connect("harvard_db.sqlite3")

    if sub_report == "Byzantine Artifacts (11th Century)":
        query = "SELECT * FROM artifact_metadata WHERE century LIKE '11th%' AND culture='Byzantine'"
        df = pd.read_sql_query(query, conn)
        st.markdown("📜 Byzantine Artifacts (11th Century)")
        st.dataframe(df)

    elif sub_report == "Unique Cultures Represented":
        query = "SELECT DISTINCT culture FROM artifact_metadata"
        df = pd.read_sql_query(query, conn)
        st.markdown("🌍 Unique Cultures Represented")
        st.dataframe(df)

    elif sub_report == "Archaic Period Artifacts":
        query = "SELECT * FROM artifact_metadata WHERE period='Archaic period'"
        df = pd.read_sql_query(query, conn)
        st.markdown("🏺 Archaic Period Artifacts")
        st.dataframe(df)

    elif sub_report == "Artifacts by Title (Sorted by Accession Year, Descending)":
        query = "SELECT title, accessionyear FROM artifact_metadata ORDER BY accessionyear DESC"
        df = pd.read_sql_query(query, conn)
        st.markdown("🔖 Artifacts by Title (Sorted by Accession Year, Descending)")
        st.dataframe(df)

    elif sub_report == "Department-wise Artifact Counts":
        query = "SELECT Department, COUNT(*) as artifact_count FROM artifact_metadata GROUP BY Department"
        df = pd.read_sql_query(query, conn)
        st.markdown("🏛️ Department-wise Artifact Counts")
        st.dataframe(df)

    elif sub_report == "More then 1 Image":
        query = "select * from artifact_media where imagecount >1 order by imagecount desc "
        df = pd.read_sql_query(query, conn)
        st.markdown("🌍 More then 1 Image")
        st.dataframe(df)
    elif sub_report =="Avg Rank of Artifacts":
        query="select  ROUND(AVG(rank), 2) AS avg_rank,sum(rank) as Total_ranks,count(rank) as no_of_Ranks from artifact_media"
        df=pd.read_sql_query(query,conn)
        st.markdown("🅰️Avg Rank of Artifacts")
        st.dataframe(df)
    elif sub_report=="color>Mediacount":
        query="select * from artifact_media where colorcount>mediacount"
        #query="select colorcount,mediacount from artifact_media where colorcount > mediacount"
        df=pd.read_sql_query(query,conn)
        st.markdown("higher colorcount than mediacount")
        st.dataframe(df)
    elif sub_report=="Created 1500-1600":
        query="""SELECT *
                    FROM artifact_media a
                    JOIN artifact_metadata m ON a.objectid = m.id
                    WHERE a.datebegin >= 1500
                    AND a.dateend <= 1600
                    ORDER BY a.datebegin"""
        df=pd.read_sql_query(query,conn)
        st.markdown("All artifacts created between 1500 and 1600")
        st.dataframe(df)
    elif sub_report=="No Media reports":
        query="""SELECT COUNT(*) AS artifacts_without_media
                FROM artifact_media
                WHERE imagecount = 0;"""
        df=pd.read_sql_query(query,conn)
        st.markdown("List of artifacts have no media files")
        st.dataframe(df)
    elif sub_report== "Unique HUE":
        query="""SELECT DISTINCT hue FROM artifact_colors WHERE hue IS NOT NULL ORDER BY hue"""
        df=pd.read_sql_query(query,conn)
        st.markdown("Unique HUE")
        st.dataframe(df)
    elif sub_report=="Top 5 most Colors":
        query="""SELECT hue,color, COUNT(*) AS frequency FROM artifact_colors
                GROUP BY color
                ORDER BY frequency DESC
                LIMIT 5"""
        df=pd.read_sql_query(query,conn)
        st.markdown("Top 5 most used colors by frequency")
        st.dataframe(df)
    elif sub_report=="Average coverage percentage":
        query="""SELECT hue, ROUND(AVG(percent), 2) AS avg_coverage
                FROM artifact_colors
                WHERE percent IS NOT NULL
                GROUP BY hue
                ORDER BY avg_coverage DESC"""
        df=pd.read_sql_query(query,conn)
        st.subheader("The average coverage percentage for each hue")
        st.dataframe(df)
    elif sub_report=="all colors Artifact ID":
        query="""SELECT color,objectID, hue, spectrum, percent, css3
                FROM artifact_colors
                --WHERE objectid = 'YOUR_ARTIFACT_ID'"""
        df=pd.read_sql_query(query,conn)
        st.subheader("all colors Artifact ID")
        st.dataframe(df)
    elif sub_report=="Total Colors":
        query="SELECT COUNT(*) AS total_color_entries FROM artifact_colors"
        df=pd.read_sql_query(query,conn)
        st.subheader("Total Colors in DATASETS")
        st.dataframe(df)
    elif sub_report=="Byzantine Artifacts and Their Color Hues":
        query="""SELECT m.title, c.hue  FROM artifact_metadata m
                JOIN artifact_colors c ON m.id = c.objectid
                WHERE m.culture = 'Byzantine'
                ORDER BY m.title, c.hue"""
        df=pd.read_sql_query(query,conn)
        st.subheader("Byzantine Artifacts and Their Color Hues")
        st.dataframe(df)
    elif sub_report=="Artifact Color Mapping":
        query="""SELECT m.title, c.hue
FROM artifact_metadata m
JOIN artifact_colors c ON m.id = c.objectid
ORDER BY m.title, c.hue"""
        df=pd.read_sql_query(query,conn)
        st.subheader("🎨Artifact Titles and Their Color Hues")
        st.dataframe(df)
    elif sub_report=="Artifacts by Period with Media Rank":
        query="""SELECT m.title, m.culture, a.rank
FROM artifact_metadata m
JOIN artifact_media a ON m.id = a.objectid
WHERE m.period IS NOT NULL
ORDER BY m.title"""
        df=pd.read_sql_query(query,conn)
        st.subheader("Artifacts by Period with Media Rank")
        st.dataframe(df)

    elif sub_report=="Top 10 Artifacts with Grey Colors":
        query="""SELECT m.title, a.rank, c.hue
FROM artifact_metadata m
JOIN artifact_media a ON m.id = a.objectid
JOIN artifact_colors c ON m.id = c.objectid
WHERE c.hue = 'Grey'
ORDER BY a.rank ASC
LIMIT 10"""
        df=pd.read_sql_query(query,conn)
        st.subheader("Top 10 Artifacts with Grey Colors")
        st.dataframe(df)
    elif sub_report=="Artifacts per Classification and Media Overview":
        query="""SELECT m.classification, 
       COUNT(*) AS artifact_count, 
       ROUND(AVG(a.mediacount), 2) AS avg_media_count
FROM artifact_metadata m
JOIN artifact_media a ON m.id = a.objectid
GROUP BY m.classification
ORDER BY artifact_count DESC"""
        df=pd.read_sql_query(query,conn)
        st.subheader("Artifacts per Classification and Media Overview")
        st.datafram(df)
    conn.close()


# Sidebar: Select report
chart = st.sidebar.selectbox(
    "Choose a chart_report",
    ["", "Century Wise collection chart","Calssifcation Chart","Calssifcation vs Color Chart"]
)

# Button to display the report
if st.sidebar.button("Display"):

    # Connect to SQLite database
    conn = sqlite3.connect("harvard_db.sqlite3")

    # Run query based on selection
    if chart == "Century Wise collection chart":
        # Query: count of artifacts per century
        query = "SELECT century, COUNT(*) as total FROM artifact_metadata GROUP BY century"
        df = pd.read_sql_query(query, conn)

        # Create bar chart using century as index
        st.bar_chart(df.set_index('century')['total'])

        # Optional: display query and dataframe
        st.markdown("### SQL Query:")
        st.code(query)
        st.markdown("### Data Table:")
        st.dataframe(df)

    if chart == "Calssifcation Chart":
        # Query: count of artifacts per century
        query = "SELECT count(classification) as Total_count ,classification FROM artifact_metadata group by classification "
        df = pd.read_sql_query(query, conn)
        
        # Create bar chart using century as index
        st.bar_chart(df.set_index('classification')['Total_count'])
        
        # Optional: display query and dataframe
        st.markdown("### SQL Query:")
        st.code(query)
        st.markdown("### Data Table:")
        st.dataframe(df)
        

    if chart == "Calssifcation vs Color Chart":
        # Query: count of artifacts per calssification
        query = """SELECT m.classification, ROUND(AVG(c.percent),2) AS avg_color_coverage
        FROM artifact_metadata m
        JOIN artifact_colors c ON m.id = c.objectid
        GROUP BY m.classification
        ORDER BY avg_color_coverage DESC;"""
        df = pd.read_sql_query(query, conn)

        # Create bar chart using classification as index
        st.bar_chart(df.set_index('classification')['avg_color_coverage'])


        # Optional: display query and dataframe
        st.markdown("### SQL Query:")
        st.code(query)
        st.markdown("### Data Table:")
        st.dataframe(df)

        # Close connection
        conn.close()



# ===========================
# Footer / Credits
# ===========================
st.markdown("---")
st.write("© 2025 Built by Prasath Rk")
st.write("Data Source: [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api)")