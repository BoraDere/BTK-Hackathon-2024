import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_list_items(links, filenames):
    scraped_data = []
    if len(links) != len(filenames):
        print("Error: Number of links and filenames must be the same.")
        return
    
    for link, filename in zip(links, filenames):
        try:
            response = requests.get(link)
            response.raise_for_status()  # Check for successful request
            soup = BeautifulSoup(response.text, 'html.parser')
            
            items_text = []
            # Find the specific <div> and then target <ul> within it, excluding <div> with id="ez-toc-container"
            entry_div = soup.find('div', class_="entry-content entry clearfix")
            if entry_div:
                for ul in entry_div.find_all('ul'):
                    if ul.find_parent(id="ez-toc-container"):
                        continue
                    
                    list_items = ul.find_all('li')
                    items_text.extend([item.get_text(strip=True) for item in list_items])

                if not items_text:
                    for p in entry_div.find_all('p'):
                        # Skip <p> tags with style="text-align: justify;"
                        if p.get("style") == "text-align: justify;":
                            continue
                        
                        # Check for <strong> tags within <p> and collect their text
                        strong_items = p.find_all('strong')
                        items_text.extend([strong.get_text(strip=True) for strong in strong_items])

                if not items_text:
                    tbody = entry_div.find('tbody')  # Look for <tbody> directly within entry_div
                    if tbody:
                        # Extract text from <span> within <td>
                        table_cells = tbody.find_all('td')
                        for cell in table_cells:
                            spans = cell.find_all('span')  # Find all <span> in <td>
                            for span in spans:
                                items_text.append(span.get_text(strip=True))  # Append the text from <span>
            
            # Write scraped topics to file and append to scraped_data
            scraped_data.append(items_text)
            with open(f'courses/{filename}', 'w', encoding='utf-8') as f:
                for item in items_text:
                    f.write(item + "\n")
            
            print(f"Data from {link} has been written to {filename}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {link}: {e}")
        except AttributeError:
            print(f"No relevant content found in {link}.")
    
    return scraped_data

def update_json_with_topics(scraped_data, json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    course_index = 0
    for grade in data.get("Grades", []):
        for course in grade.get("Courses", []):
            if course_index < len(scraped_data):
                # Update the "Topics" field with the corresponding scraped data
                course["Topics"] = scraped_data[course_index]
                course_index += 1
    
    # Write updated data back to the JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Updated {json_file} with scraped topics.")

links = [
    # 9th grade topics
    "https://www.unirehberi.com/9-sinif-matematik-konulari/",
    "https://www.unirehberi.com/9-sinif-fizik-konulari/",
    "https://www.unirehberi.com/9-sinif-kimya-konulari/",
    "https://www.unirehberi.com/9-sinif-biyoloji-konulari/",
    "https://www.unirehberi.com/9-sinif-cografya-konulari/",
    "https://www.unirehberi.com/9-sinif-tarih-konulari-ve-mufredati/",
    "https://www.unirehberi.com/9-sinif-turk-dili-ve-edebiyati-konulari/",
    "https://www.unirehberi.com/9-sinif-ingilizce-konulari/",
    "https://www.unirehberi.com/9-sinif-almanca-konulari-ve-mufredati/",
    "https://www.unirehberi.com/9-sinif-din-kulturu-konulari-ve-mufredati/",
    # 10th grade topics
    "https://www.unirehberi.com/10-sinif-matematik-konulari/",
    "https://www.unirehberi.com/10-sinif-fizik-konulari/",
    "https://www.unirehberi.com/10-sinif-kimya-konulari/",
    "https://www.unirehberi.com/10-sinif-biyoloji-konulari/",
    # "https://www.unirehberi.com/10-sinif-cografya-konulari/",
    # "https://www.unirehberi.com/10-sinif-tarih-konulari-ve-mufredati/",
    # "https://www.unirehberi.com/10-sinif-turk-dili-ve-edebiyati-konulari/",
    # "https://www.unirehberi.com/10-sinif-felsefe-konulari/",
    # "https://www.unirehberi.com/10-sinif-dil-ve-anlatim-konulari/",
    # "https://www.unirehberi.com/10-sinif-ingilizce-konulari/",
    # "https://www.unirehberi.com/10-sinif-din-kulturu-konulari-ve-mufredati/",
    # # 11th grade topics
    # "https://www.unirehberi.com/11-sinif-matematik-konulari/",
    # "https://www.unirehberi.com/11-sinif-geometri-konulari/",
    # "https://www.unirehberi.com/11-sinif-fizik-konulari/",
    # "https://www.unirehberi.com/11-sinif-kimya-konulari/",
    # "https://www.unirehberi.com/11-sinif-biyoloji-konulari/",
    # "https://www.unirehberi.com/11-sinif-cografya-konulari/",
    # "https://www.unirehberi.com/11-sinif-tarih-konulari-ve-mufredati/",
    # "https://www.unirehberi.com/11-sinif-turk-dili-ve-edebiyati-konulari/",
    # "https://www.unirehberi.com/11-sinif-dil-ve-anlatim-konulari/",
    # "https://www.unirehberi.com/11-sinif-felsefe-konulari/",
    # "https://www.unirehberi.com/11-sinif-psikoloji-konulari-ve-mufredati/",
    # "https://www.unirehberi.com/11-sinif-sosyoloji-konulari-ve-mufredati/",
    # "https://www.unirehberi.com/11-sinif-ingilizce-konulari/",
    # "https://www.unirehberi.com/11-sinif-almanca-konulari-ve-mufredati/",
    # "https://www.unirehberi.com/11-sinif-din-kulturu-konulari-ve-mufredati/",
    # # 12th grade topics
    # "https://www.unirehberi.com/12-sinif-matematik-konulari/",
    # "https://www.unirehberi.com/12-sinif-geometri-konulari/",
    # "https://www.unirehberi.com/12-sinif-fizik-konulari/",
    # "https://www.unirehberi.com/12-sinif-kimya-konulari/",
    # "https://www.unirehberi.com/12-sinif-biyoloji-konulari/",
    # "https://www.unirehberi.com/12-sinif-cografya-konulari/",
    # "https://www.unirehberi.com/12-sinif-t-c-inkilap-tarihi-ve-ataturkculuk-konulari-ve-mufredati/",
    # "https://www.unirehberi.com/12-sinif-edebiyat-konulari/",
    # "https://www.unirehberi.com/12-sinif-cagdas-turk-ve-dunya-tarihi-konulari-ve-mufredati/",
    # "https://www.unirehberi.com/12-sinif-demokrasi-ve-insan-haklari-konulari-ve-mufredati/",
    # "https://www.unirehberi.com/12-sinif-ingilizce-konulari/",
    # "https://www.unirehberi.com/12-sinif-mantik-konulari/",
    # "https://www.unirehberi.com/12-sinif-sosyoloji-konulari-ve-mufredati/",
    # "https://www.unirehberi.com/12-sinif-din-kulturu-konulari-ve-mufredati/"
]
filenames = [
    "09_math.txt",
    "09_physics.txt",
    "09_chem.txt",
    "09_bio.txt",
    "09_geo.txt",
    "09_hist.txt",
    "09_turkish.txt",
    "09_eng.txt",
    "09_german.txt",
    "09_religion.txt",
    "10_math.txt",
    "10_physics.txt",
    "10_chem.txt",
    "10_bio.txt",
    # "10_geo.txt",
    # "10_hist.txt",
    # "10_turkish.txt",
    # "10_philosophy.txt",
    # "10_communication.txt",
    # "10_eng.txt",
    # "10_religion.txt",
    # "11_math.txt",
    # "11_geometry.txt",
    # "11_physics.txt",
    # "11_chem.txt",
    # "11_bio.txt",
    # "11_geo.txt",
    # "11_hist.txt",
    # "11_turkish.txt",
    # "11_communication.txt",
    # "11_philosophy.txt",
    # "11_psychology.txt",
    # "11_sociology.txt",
    # "11_eng.txt",
    # "11_german.txt",
    # "11_religion.txt",
    # "12_math.txt",
    # "12_geometry.txt",
    # "12_physics.txt",
    # "12_chem.txt",
    # "12_bio.txt",
    # "12_geo.txt",
    # "12_ataturk.txt",
    # "12_literature.txt",
    # "12_modern_hist.txt",
    # "12_democracy.txt",
    # "12_eng.txt",
    # "12_logic.txt",
    # "12_sociology.txt",
    # "12_religion.txt"
]

scraped_topics = scrape_list_items(links, filenames)
update_json_with_topics(scraped_topics, 'metadata.json')
