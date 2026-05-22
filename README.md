# 🌊 USGS Guadalupe River — Live Stage Monitor

## 📋 Table of Contents
- [Overview](#overview)
- [Why This Matters](#why-this-matters)
- [Live Output](#live-output)
- [How It Works](#how-it-works)
- [Architecture Decision Log](#architecture-decision-log)
- [Repository Structure](#repository-structure)
- [Flood Stage Thresholds](#flood-stage-thresholds)
- [Connection to ArcGIS Experience Builder](#connection-to-arcgis-experience-builder)
- [Automated Schedule](#automated-schedule)
- [Technologies Used](#technologies-used)

## 🌐 Overview
Automated Python script using GitHub Actions (IoT data pipeline) that pulls live stream gauge readings from a federal USGS sensor on the Guadalupe River at Hunt, TX and delivers them to a public ArcGIS Experience Builder flood monitoring application, updated automatically 
every 60 minutes via GitHub Actions.

## ⚠️ Why This Matters
Flood monitoring is a time-critical discipline. Emergency 
managers, floodplain administrators, and civil engineers 
need current river stage data to make informed decisions 
about evacuation timing, infrastructure risk, and resource 
deployment.

The Guadalupe River corridor near Hunt, Texas experienced 
a catastrophic flood event on July 4, 2025, in which the 
river rose 26 feet in 45 minutes. This repository is part 
of a broader GIS flood vulnerability analysis of that 
corridor, connecting live federal sensor data to a 
professional spatial analysis application.

By integrating Internet of Things sensor data directly 
into a public GIS platform, this pipeline demonstrates 
how automated real-time monitoring can support situational 
awareness before, during, and after flood events.

## 📡 Live Output
The pipeline produces a live river stage widget embedded 
directly inside a public ArcGIS Experience Builder 
application. The widget displays the following information, 
updated every 60 minutes automatically:

- Current river stage in feet
- Color-coded flood status: Normal (green), Elevated 
  (yellow), or Flood Stage (red)
- Official sensor name: Guadalupe River at Hunt, TX
- USGS Site No. 08165500
- Data source: USGS Water Data for the Nation
- Timestamp of the most recent reading

Flood stage thresholds are based on official USGS and 
National Weather Service designations for gauge 08165500.

Live Application:
[Guadalupe River Flood Vulnerability — ArcGIS Experience Builder] https://experience.arcgis.com/experience/09c67703781c49ddbc0830655aba9473/
 
Live Gauge Widget:
https://austin-aeceomnis.github.io/USGS-Guadalupe-LiveStage/

## ⚙️ How It Works
The pipeline operates in four stages:

**1. Data Request**
A Python script (fetch_gauge.py) sends a request to the 
USGS Water Services API, querying the instantaneous value 
for stream gauge parameter 00065 (gage height in feet) at 
site 08165500. The API returns a JSON response containing 
the most recent reading and its timestamp.

**2. Data Storage**
The script parses the API response and writes the current 
stage reading, timestamp, and site name to a file called 
current_stage.json in this repository. This file is 
updated automatically with every pipeline run.

**3. Automation**
A GitHub Actions workflow (fetch_stage.yml) triggers the 
Python script on a scheduled cron interval of every 60 
minutes, 24 hours a day, without any manual intervention. 
The workflow runs on a GitHub-hosted Ubuntu virtual machine, 
installs the required Python dependencies, executes the 
script, and commits the updated JSON file back to the 
repository.

**4. Display**
GitHub Pages serves this repository as a live website. 
A custom HTML file (index.html) reads current_stage.json 
at page load, parses the stage value, applies the flood 
status logic, and renders the formatted widget. That widget 
is embedded inside the ArcGIS Experience Builder 
application via the platform's native Embed widget.

## 🏗️ Architecture Decision Log
Multiple approaches were evaluated before selecting the 
final pipeline architecture. This log documents each option 
considered, the reasoning behind its rejection or selection, 
and the tradeoffs involved.

**Option 1: ArcGIS Online Hosted Feature Layer Push**
The Python script would push each new reading directly into 
a hosted feature layer in ArcGIS Online, which Experience 
Builder would read natively as a map layer. This approach 
was rejected because it required storing ArcGIS credentials 
as GitHub repository secrets, added significant 
authentication complexity to the Python script, and created 
a dependency on Esri API stability. Any future change to 
Esri's authentication model could break the pipeline 
silently.

**Option 2: ArcGIS Instant App with Embedded GitHub Pages**
A standalone Instant App would host the gauge widget and 
link from Experience Builder. This approach was rejected 
as unnecessary added complexity. Experience Builder is 
capable of hosting the embed widget directly, making a 
separate Instant App a redundant layer with no functional 
benefit.

**Option 3: Embed USGS Public Widget Directly**
USGS provides public-facing monitoring pages for each 
gauge station. The intent was to embed the official USGS 
page directly into Experience Builder via an iframe. This 
option was tested live and rejected. USGS monitoring pages 
block iframe embedding via Content Security Policy headers, 
which produced a blank widget inside Experience Builder 
with no error message. Testing before committing to a build 
path confirmed this incompatibility.

**Option Selected: GitHub Pages HTML Widget**
GitHub Actions writes the live reading to 
current_stage.json on each run. GitHub Pages serves that 
file at a public HTTPS URL. A custom index.html reads the 
JSON and renders the formatted stage widget. Experience 
Builder embeds the GitHub Pages URL via its native Embed 
widget. This approach was selected for the following 
reasons: zero credential exposure, no dependency on Esri 
API changes, HTTPS enforced automatically by GitHub Pages 
eliminating iframe blocking risk, and the complete 
technical pipeline visible to any reviewer in a single 
public repository.

## 📁 Repository Structure
USGS-Guadalupe-LiveStage/
├── fetch_gauge.py          # Python script that queries 
│                           # the USGS Water Services API 
│                           # and writes the live reading 
│                           # to current_stage.json
├── current_stage.json      # Auto-updated file containing 
│                           # the most recent stage reading, 
│                           # timestamp, and site name
├── index.html              # Custom HTML widget served via 
│                           # GitHub Pages that reads 
│                           # current_stage.json and renders 
│                           # the formatted live display
└── .github/
    └── workflows/
        └── fetch_stage.yml # GitHub Actions workflow that 
                            # runs fetch_gauge.py on a 
                            # 60-minute cron schedule and 
                            # commits the updated JSON file 
                            # back to the repository

## 🌡️ Flood Stage Thresholds
The flood status indicator displayed in the live widget 
is based on official USGS and National Weather Service 
designations for gauge 08165500 on the Guadalupe River 
at Hunt, TX. The following thresholds are applied:

| Status      | Stage Range       | Indicator Color |
|-------------|-------------------|-----------------|
| Normal      | Below 10.0 ft     | Green           |
| Elevated    | 10.0 to 14.9 ft   | Yellow          |
| Flood Stage | 15.0 ft and above | Red             |

At flood stage, the Guadalupe River at Hunt begins to 
affect low-lying structures and roadways in the corridor. 
The July 4, 2025 flood event reached an estimated crest 
of 26 feet above normal stage, inundating 107 structures 
matching the Camp Mystic terrain signature identified 
in the companion spatial analysis.

## 🗺️ Connection to ArcGIS Experience Builder
The live gauge widget is embedded inside a public ArcGIS 
Experience Builder application built as part of a broader 
Guadalupe River flood vulnerability analysis. The 
application displays terrain-based flood risk data for 
the Hunt, Texas corridor, including 255 structures in 
elevated risk zones, 107 structures matching the Camp 
Mystic terrain signature, and live river stage data from 
this pipeline.

The connection between this repository and Experience 
Builder works as follows. GitHub Actions updates 
current_stage.json every 60 minutes. GitHub Pages serves 
the updated index.html at a public HTTPS URL. Experience 
Builder's native Embed widget displays that URL inline 
inside the application. No Esri credentials, no hosted 
feature layers, and no manual updates are required at 
any point in the chain.

This architecture was chosen specifically to avoid 
dependencies on Esri API changes while keeping the 
complete technical pipeline visible and auditable in 
a single public GitHub repository.

Live Application:
[Guadalupe River Flood Vulnerability — ArcGIS Experience Builder] https://experience.arcgis.com/experience/09c67703781c49ddbc0830655aba9473/

## ⏱️ Automated Schedule
The GitHub Actions workflow runs automatically on the 
following schedule:

- Frequency: Every 60 minutes, 24 hours a day
- Trigger: Scheduled cron expression (0 * * * *)
- Runtime environment: GitHub-hosted Ubuntu virtual machine
- Manual trigger: Available via the Actions tab in this 
  repository for on-demand runs

GitHub Actions free tier allows 2,000 minutes of runtime 
per month. At the current schedule, this pipeline consumes 
approximately 720 to 1,440 minutes per month, staying 
comfortably within free tier limits.

## 🛠️ Technologies Used
- Python 3.11
- USGS Water Services API (api.waterdata.usgs.gov)
- GitHub Actions
- GitHub Pages
- HTML and JavaScript
- ArcGIS Experience Builder
- USGS gauge parameter 00065: Gage Height, feet
- Monitoring location: USGS-08165500, Guadalupe River 
  at Hunt, TX
