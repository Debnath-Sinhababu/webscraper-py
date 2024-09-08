import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, DashboardData, CompanyData, TransportData
from dotenv import load_dotenv
import os
from sqlalchemy import exc

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Set up SQLite database connection
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def load_json_file(file_path):
    """
    Load data from a JSON file.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

def extract_json(text_list):
    """
    Extracts valid JSON from a list of text lines.
    """
    json_data_str = ''

    final_json = {
        "dashboard_data": [],
        "company_data": {},
        "main_page_data": []
    }

    current_item = ''

    for line in text_list:
        if any(skip_text in line for skip_text in ['Login successful.', 'Main Page Data Size:', 'Companies Data Size:', 'Dashboard Data Size:', '[]', 'brokers']):
            continue

        if 'Dashboard Data:' in line:
            current_item = 'dashboard_data'
            json_data_str = ''
            continue
        
        if 'Main Page Data:' in line:
            current_item = 'main_page_data'
            json_data_str = ''
            continue

        if 'Companies Data:' in line:
            current_item = 'company_data'
            json_data_str = ''
            continue

        # Append the line to json_data_str if it's part of the current section
        json_data_str += line.strip().replace('\n', '')

        try:
            # Attempt to load JSON once the string seems to be complete
            if ']' in line and current_item in ['dashboard_data', 'main_page_data']:
                print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                final_json[current_item] = json.loads(json_data_str)
                print('cccccccccccccccccccccccccccccccccccccc')
                current_item = ''
                json_data_str = ''

            if '}' in line and current_item == 'company_data':
                final_json[current_item] = json.loads(json_data_str)
                current_item = ''
                json_data_str = ''
                
        except Exception as e:
            print(f"Error inserting data: {e}")
            print(f"Line: {line}")
            print(f"json_data_str: {json_data_str}")
            return None

    return final_json

def process_and_insert(data_json):
    session = SessionLocal()

    try:
        # Process JSON structure
        json_data = extract_json(data_json)
        if json_data is None:
            print("Failed to extract JSON data.")
            return

        # Insert company_data into the database, handling conflicts
        for key, value in json_data["company_data"].items():
            new_company = CompanyData(company_name=key, value=value)
            try:
                session.add(new_company)
                session.flush()  # This triggers the insert immediately for handling conflicts
            except exc.IntegrityError:
                session.rollback()  # Ignore duplicate entries
                print(f"Duplicate entry found for company: {key}")

        # Insert main_page_data into the database, handling conflicts
        for item in json_data['main_page_data']:
            try:
                new_transport = TransportData(
                    pickup=item['pickup'],
                    destination=item['destination'],
                    date=item['date'],
                    weight=item['weight'],
                    distance=item['distance'],
                    type=item['type']
                )
                session.add(new_transport)
                session.flush()  # Trigger the insert immediately
            except exc.IntegrityError:
                session.rollback()  # Ignore duplicate entries
                print(f"Duplicate transport data: {item}")
        
        # Insert dashboard_data into the database, handling conflicts
        for item in json_data['dashboard_data']:
            new_entry = DashboardData(
                id=int(item["id"]),
                uid=item["uid"],
                pickup=item["pickup"],
                age=item["age"],
                origin=item["origin"],
                destination=item["destination"],
                weight=item["weight"],
                distance=item["distance"],
                price=item["price"],
                company=item["company"],
                phone=item["phone"]
            )
            try:
                session.add(new_entry)
                session.flush()  # Trigger the insert immediately
            except exc.IntegrityError:
                session.rollback()  # Ignore duplicate entries
                print(f"Duplicate dashboard data: {item}")
        
        # Commit the session after all inserts
        session.commit()
        print("Data inserted successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")
        print(f"-----: {json_data}")
    finally:
        session.close()

if __name__ == "__main__":

    json_data = load_json_file('scrape_data.json')
    pp = json_data["cells"]
    
    if len(pp) > 1 and len(pp[1]["outputs"]) > 0:
        for item in pp[1]["outputs"]:
            process_and_insert(item["text"])
