import requests
from bs4 import BeautifulSoup

faculty_directory_url = "https://www.calstatela.edu/ecst/cs/faculty"
response=requests.get(faculty_directory_url)
print(response)
html_content= response.text

Parse = BeautifulSoup(html_content, 'html.parser')

paragraphs = Parse.find_all('//*[@id="block-csula-content"]/article')

table = Parse.find('table')

print(paragraphs)
print(table)


def get_faculty_homepage_urls(directory_url):
  homepage_urls = []
  response = requests.get(directory_url)
  
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    faculty_links = soup.select(".faculty-list a")
    for link in faculty_links:
        homepage_url = link.get("href")
        
        if not homepage_url.startswith("http"):
          homepage_url = f"{directory_url}/{homepage_url}"
          
        homepage_urls.append(homepage_url)
        
  return homepage_urls

def scrape_faculty_info(homepage_url):
  faculty_info = {}
  
  response = requests.get(homepage_url)
  
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    faculty_info["name"] = soup.select_one(".faculty-name").text.strip()
    faculty_info["bio"] = soup.select_one(".faculty-bio").text.strip()
    faculty_info["courses"] = [course.text.strip() for course in soup.select(".faculty-courses li")]
    
  return faculty_info

if __name__ == "_main_":
  faculty_directory_url = "https://www.calstatela.edu/ecst/cs/faculty"
  faculty_homepage_urls = get_faculty_homepage_urls(faculty_directory_url)
  
  faculty_data = []
  
  for homepage_url in faculty_homepage_urls:
    faculty_info = scrape_faculty_info(homepage_url)
    faculty_data.append(faculty_info)
    
  for faculty in faculty_data:
    print("Name:", faculty.get("name"))
    print("Bio:", faculty.get("bio"))
    print("Courses:", ", ".join(faculty.get("courses")))
    print("\n")
