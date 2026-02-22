import pandas as pd
import random
import os

# Constants
TOTAL_RECORDS = 1200
INDIAN_RATIO = 0.7
FAKE_RATIO = 0.6

# Indian Constraints
INDIAN_COUNT = int(TOTAL_RECORDS * INDIAN_RATIO)
FOREIGN_COUNT = TOTAL_RECORDS - INDIAN_COUNT

# Templates & Data for Synthesis

# 1. INDIAN GENUINE
indian_companies = ["TCS", "Infosys", "Wipro", "HCL Tech", "Tech Mahindra", "Reliance Jio", "Airtel", "HDFC Bank", "ICICI Bank", "Tata Motors"]
indian_locations = ["Bangalore", "Hyderabad", "Pune", "Chennai", "Mumbai", "Gurgaon", "Noida"]
indian_roles_gen = ["Software Engineer", "System Analyst", "Data Scientist", "Java Developer", "Business Analyst", "Sales Manager", "HR Executive"]
indian_emails_gen = ["careers@{company}.com", "hr@{company}.co.in", "recruitment@{company}.net"]

indian_desc_gen = [
    "We are looking for a skilled {role} to join our team in {location}. Minimum 2 years experience required. Apply on our official portal.",
    "{company} is hiring for {role}. Excellent communication skills and technical knowledge required. Competitive salary and benefits.",
    "Join {company} as a {role}. Work on cutting-edge technologies. Location: {location}. Send resume to our official email.",
    "Urgent opening for {role} at {company} {location} branch. Bachelor's degree mandatory. Formal interview process includes Technical and HR rounds."
]

# 2. INDIAN FAKE
indian_scam_roles = ["Data Entry Operator", "Back Office Executive", "Form Filling Job", "SMS Sending Job", "Captcha Entry Work", "Assistant Helper", "Airport Ground Staff"]
indian_scam_patterns = [
    "Pay registration fee of Rs. {amount} to get started. Refundable after first salary.",
    "Work from home opportunity. Earn {salary} daily. No interview needed. Contact via WhatsApp {phone}.",
    "Urgent hiring for {role}. 100% genuine. Pay processing charge {amount} for ID card and laptop gate pass.",
    "Direct joining without interview. Salary {salary}. Security deposit required for verification.",
    "Part time job. Just typing work. Earn weekly payment. 100% guaranteed. Call HR {name} on {phone}.",
    "Government job backdoor entry. Pay {amount} for cleaning charges and get appointment letter today."
]
indian_emails_fake = ["hr.{company}@gmail.com", "recruiter.{company}@yahoo.co.in", "carrer.offer@rediffmail.com", "job.offer123@hotmail.com"]
fake_companies_in = ["DataTech Solutions", "Global Services", "Smart Work Pvt Ltd", "Digital India Hub", "Airport Services"]

# 3. FOREIGN GENUINE
foreign_companies = ["Google", "Amazon", "Microsoft", "Tesla", "Facebook", "Netflix", "Adobe", "Salesforce"]
foreign_locations = ["New York", "London", "Berlin", "San Francisco", "Remote", "Singapore", "Sydney"]
foreign_roles_gen = ["Frontend Developer", "Product Manager", "DevOps Engineer", "Cloud Architect", "Marketing Director"]
foreign_emails_gen = ["jobs@{company}.com", "careers@{company}.org"]

foreign_desc_gen = [
    "{company} is seeking a talented {role}. Experience with modern tech stack is a plus. Apply via our careers page.",
    "Exciting opportunity for {role} at {company}. Remote options available. Competitive compensation package.",
    "Join our global team as a {role}. We prioritize innovation and diversity. Full health benefits included."
]

# 4. FOREIGN FAKE
foreign_scam_roles = ["Mystery Shopper", "Package Handler", "Payment Processor", "Cruise Ship Crew", "Oil Rig Worker"]
foreign_scam_patterns = [
    "Earn $2000 weekly working from home. We need a {role} immediately. Shipping supplies included.",
    "Exciting offer for {role}. We will send you a check for equipment. Deposit the rest to our vendor.",
    "Immediate visa sponsorship for {role}. Pay small administrative fee for visa processing.",
    "No experience needed. {role} position. High pay. Contact us on Telegram for details."
]
foreign_emails_fake = ["employment@{company}-jobs.com", "hiring@gmail.com", "career@yahoo.com"]


def generate_record(is_indian, is_fake):
    record = {}
    
    # Setup context
    if is_indian:
        record['country'] = 'India'
        company = random.choice(fake_companies_in if is_fake else indian_companies)
        role = random.choice(indian_scam_roles if is_fake else indian_roles_gen)
        email_fmt = random.choice(indian_emails_fake if is_fake else indian_emails_gen)
        desc_tmplt = random.choice(indian_scam_patterns if is_fake else indian_desc_gen)
        
        # Specific Indian Scam Fillers
        amount = random.choice(["500", "999", "1500", "2000", "5000"])
        salary = random.choice(["25000", "40000", "5000/day", "30000/month"])
        phone = f"+91-{random.randint(6000000000, 9999999999)}"
        
        description = desc_tmplt.format(company=company, role=role, amount=amount, salary=salary, phone=phone, location=random.choice(indian_locations), name="Amit")
        
        # Payment Request Logic
        record['payment_request'] = True if is_fake and ("fee" in description or "charge" in description or "deposit" in description) else False
        
        # Interview Process
        record['interview_process'] = "No Interview" if is_fake else "Aptitude + Technical + HR"
        
        # URL
        if is_fake:
            record['job_url'] = random.choice([f"http://bit.ly/job{random.randint(100,999)}", f"http://tinyurl.com/{company.lower()}", "http://forms.gle/xyz"])
        else:
            record['job_url'] = f"https://careers.{company.lower().replace(' ', '')}.com/jobs/{random.randint(1000,9999)}"

    else:
        record['country'] = 'Foreign'
        company = random.choice(foreign_companies) # Fake foreigns often impersonate real ones too
        role = random.choice(foreign_scam_roles if is_fake else foreign_roles_gen)
        email_fmt = random.choice(foreign_emails_fake if is_fake else foreign_emails_gen)
        desc_tmplt = random.choice(foreign_scam_patterns if is_fake else foreign_desc_gen)
        
        description = desc_tmplt.format(company=company, role=role)
        
        record['payment_request'] = True if is_fake and ("fee" in description or "check" in description) else False
        record['interview_process'] = "Online Chat" if is_fake else "Video Conference x3"
        
        if is_fake:
             record['job_url'] = f"http://{company.lower()}-hiring-now.net"
        else:
             record['job_url'] = f"https://jobs.{company.lower()}.com"

    # Common Fields
    record['job_title'] = role
    record['company_name'] = company
    record['job_description'] = description
    record['recruiter_email'] = email_fmt.format(company=company.lower().replace(' ', ''))
    record['salary'] = "Undisclosed" if not is_fake else "High/Unrealistic"
    record['location'] = random.choice(indian_locations) if is_indian else random.choice(foreign_locations)
    record['label'] = 'Fake' if is_fake else 'Genuine'
    
    return record


# Generation Loop
data = []

# 1. Indian Records
indian_fake_count = int(INDIAN_COUNT * FAKE_RATIO)
indian_real_count = INDIAN_COUNT - indian_fake_count

for _ in range(indian_fake_count): data.append(generate_record(True, True))
for _ in range(indian_real_count): data.append(generate_record(True, False))

# 2. Foreign Records
foreign_fake_count = int(FOREIGN_COUNT * FAKE_RATIO)
foreign_real_count = FOREIGN_COUNT - foreign_fake_count

for _ in range(foreign_fake_count): data.append(generate_record(False, True))
for _ in range(foreign_real_count): data.append(generate_record(False, False))

# Shuffle and Save
random.shuffle(data)
df = pd.DataFrame(data)

os.makedirs('ml_service/data', exist_ok=True)
csv_path = 'ml_service/data/jobcheq_dataset.csv'
df.to_csv(csv_path, index=False)

print(f"Dataset generated successfully at {csv_path}")
print(f"Total Records: {len(df)}")
print(df['country'].value_counts())
print(df['label'].value_counts())
