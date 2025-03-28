import openpyxl, json, requests
from openpyxl import Workbook

url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

job_title = input("Enter the job title you're looking for: ")
location = input("Enter the location (e.g., city or state): ")


params = {
    "app_id": "08e49799",
    "app_key": "7a9887c1e3f68f97dd4e7bc4587a5a08",
    "results_per_page": 20,
    "what": job_title,
    "where": location,
    "max_days_old": 5
}

response = requests.get(url, params=params)
if response.status_code != 200:
    print("❌ Error:", response.status_code)
    print(response.text)
    exit()

json_data = response.json()
jobs = json_data.get("results", [])
print(f"✅ Total jobs retrieved: {len(jobs)}")



yelp_url = "https://api.yelp.com/v3/businesses/search"

yelp_header = {
    "accept": "application/json",
    "authorization": "Bearer lGhHfJ5rJl8nMrr0QLei61oKEm9yS--MZa9WUtadR1-X0qWjXtvBmGRUXKqbWGwEKq6SaBgS4D69fDbKswUSFuU7ZhkLEqnXICzv8zRvfYNi5ofrJ_FZc-hQwKHhZ3Yx"
}
def search_yelp (organization, city):
    yelp_param = {
    "location": city,
    "term": organization
    }
    response = requests.get(yelp_url, headers=yelp_header, params = yelp_param)
    data = response.json()
    for business in data.get('businesses', []):
        if business.get("name", "").lower() == organization.lower():
            return {
                "rating": business.get('rating'),
                "address": ",".join(business.get('location', {}).get('display_address', []))
            }
    return None

wb = Workbook()
ws = wb.active
ws.title = "Job Listings + Yelp"
headers = ["Created", "Title", "Organization", "City", "Region", "Salary Range", "URL", "Description", "Yelp Rating", "Yelp Address"]
ws.append(headers)


for job in jobs:
    created = job.get("created", "N/A")
    title = job.get("title", "N/A")
    organization = job.get("company", {}).get("display_name", "N/A")
    location = job.get("location", {}).get("area", [])
    city = location[-1] if len(location) > 0 else "N/A"
    region = location[-2] if len(location) > 1 else "N/A"
    description = job.get("description", "N/A")[:32767]

    
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
    
    # Call Yelp
    yelp_info = search_yelp(organization, city)
    yelp_rating = yelp_info["rating"] if yelp_info else "N/A"
    yelp_address = yelp_info["address"] if yelp_info else "N/A"

    ws.append([created, title, organization, city, region, salary_range, url, description, yelp_rating, yelp_address])


wb.save("joblist.xlsx")