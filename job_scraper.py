"""
Job Scraper Module
Collects job listings from multiple sources (LinkedIn, Indeed, Naukri).
In production, use Selenium/Playwright or official APIs.
"""
import random

JOB_LISTINGS = [
    {
        "id": 1, "title": "Machine Learning Engineer", "company": "Google",
        "location": "Bangalore / Remote", "salary": "₹25-40 LPA",
        "source": "LinkedIn",
        "skills": ["Python","TensorFlow","PyTorch","MLflow","Docker","Kubernetes"],
        "description": "Build and deploy scalable ML models for Google's core products.",
        "embedding_vector": None,
        "url": "https://careers.google.com",
    },
    {
        "id": 2, "title": "Data Scientist", "company": "Microsoft",
        "location": "Hyderabad / Remote", "salary": "₹20-35 LPA",
        "source": "Indeed",
        "skills": ["Python","SQL","Pandas","Scikit-learn","Power BI","Azure"],
        "description": "Analyze large datasets to drive product insights at Microsoft Azure.",
        "embedding_vector": None,
        "url": "https://careers.microsoft.com",
    },
    {
        "id": 3, "title": "NLP Engineer", "company": "Amazon",
        "location": "Remote", "salary": "₹22-38 LPA",
        "source": "Naukri",
        "skills": ["NLP","Hugging Face","Python","LLM","RAG","Transformers"],
        "description": "Build conversational AI systems for Alexa and AWS services.",
        "embedding_vector": None,
        "url": "https://www.amazon.jobs",
    },
    {
        "id": 4, "title": "AI Engineer", "company": "Meta",
        "location": "Remote", "salary": "₹30-50 LPA",
        "source": "LinkedIn",
        "skills": ["PyTorch","Deep Learning","Python","Computer Vision","React","GraphQL"],
        "description": "Research and implement next-generation AI for Meta's platforms.",
        "embedding_vector": None,
        "url": "https://www.metacareers.com",
    },
    {
        "id": 5, "title": "Backend Engineer", "company": "Flipkart",
        "location": "Bangalore", "salary": "₹18-30 LPA",
        "source": "Naukri",
        "skills": ["Java","Kafka","Docker","Kubernetes","SQL","REST API","Git"],
        "description": "Build high-scale backend services for Flipkart's e-commerce platform.",
        "embedding_vector": None,
        "url": "https://www.flipkartcareers.com",
    },
    {
        "id": 6, "title": "Full Stack Developer", "company": "Razorpay",
        "location": "Bangalore / Remote", "salary": "₹15-25 LPA",
        "source": "Indeed",
        "skills": ["React","TypeScript","Node.js","SQL","MongoDB","AWS","Docker"],
        "description": "Design and build Razorpay's payment infrastructure and dashboards.",
        "embedding_vector": None,
        "url": "https://razorpay.com/jobs",
    },
    {
        "id": 7, "title": "Data Engineer", "company": "Swiggy",
        "location": "Bangalore", "salary": "₹16-28 LPA",
        "source": "LinkedIn",
        "skills": ["Python","Spark","Airflow","Kafka","SQL","GCP","Hadoop"],
        "description": "Build real-time data pipelines to power Swiggy's analytics platform.",
        "embedding_vector": None,
        "url": "https://careers.swiggy.com",
    },
    {
        "id": 8, "title": "Computer Vision Engineer", "company": "Ola",
        "location": "Bangalore", "salary": "₹18-32 LPA",
        "source": "Naukri",
        "skills": ["Computer Vision","PyTorch","Python","C++","Deep Learning","Linux"],
        "description": "Develop perception systems for Ola's autonomous vehicle division.",
        "embedding_vector": None,
        "url": "https://www.olacabs.com/careers",
    },
]

def get_sample_jobs() -> list:
    """
    Return a list of job listings (simulated scrape from multiple platforms).
    In production: use Selenium, BeautifulSoup, or platform APIs.
    """
    jobs = JOB_LISTINGS.copy()
    # Simulate embeddings for each job
    for job in jobs:
        job["embedding_vector"] = [random.uniform(-1, 1) for _ in range(384)]
    return jobs
