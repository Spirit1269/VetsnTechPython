import requests
from openpyxl import Workbook

# ✅ Correct Adzuna API Request
url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

params = {
    "app_id": "08e49799",  # Replace with your Adzuna app_id
    "app_key": "7a9887c1e3f68f97dd4e7bc4587a5a08",  # Replace with your Adzuna app_key
    "results_per_page": 20,
    "what": "Software Engineer",  # Combine search terms
    "where": "Dallas",
    "max_days_old": 5,
    "content-type": "application/json"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("❌ Error:", response.status_code)
    print(response.text)
    exit()

json_data = response.json()
jobs = json_data.get("results", [])
print(f"✅ Total jobs retrieved: {len(jobs)}")

# ✅ Set up Excel file
wb = Workbook()
ws = wb.active
ws.title = "Adzuna Jobs"
headers = ["Date Posted", "Title", "Company", "City", "Region", "Salary Range", "Job Link", "Description"]
ws.append(headers)

# ✅ Process and write jobs to Excel
for job in jobs:
    date_posted = job.get("created", "N/A")
    title = job.get("title", "N/A")
    company = job.get("company", {}).get("display_name", "N/A")
    location = job.get("location", {}).get("area", [])
    city = location[-1] if len(location) > 0 else "N/A"
    region = location[-2] if len(location) > 1 else "N/A"

    min_salary = job.get("salary_min")
    max_salary = job.get("salary_max")
    if min_salary and max_salary:
        salary_range = f"${min_salary:,.2f} - ${max_salary:,.2f}"
    elif min_salary:
        salary_range = f"From ${min_salary:,.2f}"
    elif max_salary:
        salary_range = f"Up to ${max_salary:,.2f}"
    else:
        salary_range = "N/A"

    url = job.get("redirect_url", "N/A")
    description = job.get("description", "N/A")[:32767]

    ws.append([date_posted, title, company, city, region, salary_range, url, description])

# ✅ Save to Excel
wb.save("adzuna_jobs_clean.xlsx")
print("✅ Saved to adzuna_jobs_clean.xlsx")
