# Marine Traffic Presentation - Talking Points

**Total Time: 5-8 minutes**
**Style: Casual, curiosity-driven, "f*ck around and find out"**

---

## **SLIDE 1: Title Slide**
**"Marine Traffic Data Analysis: An Exploratory Study of Global Vessel Patterns"**

### What to Say:
*"So this whole project started because I saw an Instagram reel about ship tracking websites. I was supposed to do a data science project for this class, and I thought—why not? Let me see if I can scrape some ship data."*

**Time: 15-20 seconds**

---

## **SLIDE 2: What does global maritime traffic look like?**
**Graph: Geographic Distribution (05_geographic_distribution.png)**

### What to Say:
*"First thing I did was reverse-engineer the MarineTraffic website. Opened the browser network tab, found their JSON API endpoint—no authentication, just sitting there. Within like 30 minutes I had scraped 10,379 vessels from around the globe."*

*"And look at this plot—this is just latitude and longitude coordinates of all those ships. You can literally see the continents forming. That's Europe, that's Southeast Asia, those are the major shipping lanes. Pretty cool how vessel density just recreates the world map."*

**Time: 45-60 seconds**

---

## **SLIDE 3: Do different vessel types have characteristic shapes?**
**Graph: Length-to-Width Ratio by Ship Type (03_lw_ratio_by_shiptype.png)**

### What to Say:
*"So then I got curious—do different types of ships have different shapes? I calculated the length-to-width ratio for each vessel type."*

*"Check this out—fishing vessels are super narrow and long, probably because they need to be fuel-efficient and maneuverable. Cargo vessels on the other hand? Absolute units. We literally called them 'chonky ships' in the analysis. They're wide because they need to stack containers and carry massive loads."*

**Time: 30-40 seconds**

---

## **SLIDE 4: How does cargo capacity relate to vessel size?**
**Graph: Deadweight Tonnage vs Length (04_dwt_vs_length.png)**

### What to Say:
*"Next question—does cargo capacity scale with vessel size? This is deadweight tonnage versus length on a log scale."*

*"Cargo vessels and tankers dominate the upper right—huge ships carrying tons of cargo. But look at the bottom left—pleasure crafts, tiny fishing vessels. There's like a 1000x difference in cargo capacity even though they're all boats."*

**Time: 30 seconds**

---

## **SLIDE 5: How does speed vary geographically?**
**Graph: Speed by Location (06_speed_by_location.png)**

### What to Say:
*"Then I overlaid speed data onto the geographic distribution. The blue/dark regions are ships that are stationary or slow-moving—mostly near ports and harbors where there are speed restrictions."*

*"The bright yellow/white dots are ships hauling ass in open ocean. You can see how coastal waters are congested and slow, but once you're out in the middle of nowhere, ships go full speed."*

**Time: 30-40 seconds**

---

## **SLIDE 6: Can heading-course differences identify vessels in distress?**
**Graph: Heading-Course Anomalies (02_hc_diff_anomalies.png)**

### What to Say:
*"Okay, so here's where I tried to get clever. Ships have a 'heading'—where the front points—and a 'course'—where they're actually moving. I thought, if these are really misaligned, maybe the ship is in trouble? Like being blown off course by waves or wind?"*

*"The red triangles are ships with huge heading-course differences at high speeds. But turns out... this doesn't really correlate with danger. Ships turn, they drift in currents, they maneuver in harbors. So this metric didn't work as a distress indicator."*

*"But hey, that's science—sometimes your hypothesis is wrong."*

**Time: 45-60 seconds**

---

## **SLIDE 7: Which features show strong correlations?**
**Graph: Correlation Matrix (07_correlation_matrix.png)**

### What to Say:
*"This is a correlation matrix showing which features relate to each other. Width and deadweight tonnage? Super correlated—makes sense, wider ships carry more cargo."*

*"Heading and course? Almost perfectly aligned—most ships go where they're pointing, which validates that the misalignment thing from before is rare."*

*"This helped me figure out which variables to use for modeling."*

**Time: 30 seconds**

---

## **SLIDE 8: What's missing in our data?**
**Graph: Missing Data Analysis (08_missing_data_analysis.png)**

### What to Say:
*"Real-world data is messy. This shows how much data is missing for each feature. Rate of turn? 73% missing. Destination? 60% missing."*

*"But I used some domain knowledge to fill gaps. Like, if a ship is moving fast and on course, it's probably not turning—so I imputed rate of turn with zero. Smart imputation beats just dropping data."*

**Time: 30 seconds**

---

## **SLIDE 9: Can we model dimensional relationships?**
**Graph: Multivariate Visualization (12_dimensions_with_speed.png)**

### What to Say:
*"Finally, the academic part—simple linear regression. This plot shows length versus width, colored by vessel type, with point size representing speed."*

*"I built a model predicting width from length. R-squared of 0.518—so like 52% of the variance explained. Not amazing, but it satisfies the course requirements for statistical modeling."*

*"The real insight here is that vessel dimensions follow patterns, but there's a lot of complexity. Different ship types cluster differently, and speed doesn't really depend on size."*

**Time: 40-50 seconds**

---

## **SLIDE 10: Conclusion**

### What to Say:
*"So to wrap up—I scraped 10,000 ships globally by reverse-engineering an API, explored the data, found patterns in vessel shapes and speeds, and built some predictive models."*

*"But here's the kicker—this is just ONE snapshot in time. If I scraped this every hour for a month, I could do time-series analysis, anomaly detection, trajectory prediction... this could become a full-stack machine learning pipeline for maritime surveillance."*

*"Started with curiosity about a random Instagram reel. Ended with architecture diagrams for real-time ship tracking systems. That's data science, I guess."*

**Time: 45-60 seconds**

---

## **TIMING BREAKDOWN:**
- Slide 1: 15-20s
- Slide 2: 45-60s
- Slide 3: 30-40s
- Slide 4: 30s
- Slide 5: 30-40s
- Slide 6: 45-60s
- Slide 7: 30s
- Slide 8: 30s
- Slide 9: 40-50s
- Slide 10: 45-60s

**TOTAL: ~5:30 - 7:30 minutes** ✅

---

## **TIPS FOR DELIVERY:**

1. **Energy matters** - You're telling a story of curiosity spiraling into a massive project. Show that excitement!

2. **Point at the graphs** - Don't just talk, gesture at specific clusters, outliers, patterns on the plots

3. **Be casual with the jargon** - Say "chonky ships," "absolute units," "hauling ass," etc. Makes it relatable

4. **Acknowledge failures** - The heading-course distress detection didn't work. That's honest science!

5. **End with the vision** - Leave them thinking "wait, this could actually be a real product"

6. **If someone asks technical questions:**
   - "How'd you bypass rate limits?" → Used headless browser with user-agent rotation
   - "Why linear regression?" → Course requirement, but acknowledged it's too simple
   - "What ML would you use?" → Clustering (DBSCAN), anomaly detection (Isolation Forest), trajectory prediction (LSTM)

---

## **BACKUP SLIDES (if you have extra time):**

If someone asks "what's the data look like?" or you need to fill time:
- Show the Network tab screenshot (how you found the API)
- Show the JSON response (what the raw data looks like)
- Show speed distribution plot (01_speed_distribution.png) - bimodal distribution showing stationary vs moving vessels

**Good luck! You've got this. 🚢**
