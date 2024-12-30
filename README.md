# COMP2001 Trail API Microservice

This repository contains the **Trail API Microservice** developed for the COMP2001 coursework. The microservice provides CRUD functionality to manage trail data and integrates with Flask, SQLAlchemy, JWT authentication, and Docker for deployment. 

The microservice provides the following features: 
- Full CRUD operations for managing trails (Create, Read, Update, Delete). 
- Secure authentication using JWT (JSON Web Tokens). 
- External authentication API integration: `https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users`. 
- Swagger UI for API documentation: [http://127.0.0.1:5000/swagger](http://127.0.0.1:5000/swagger). 
- Dockerized for consistent and easy deployment.

### How to Run Locally
**Prerequisites**: Python 3.10+ and Docker (optional for containerized deployment). 
Steps: 
1. Clone the repository: 
   ```bash 
   git clone https://github.com/Dylan-PlymouthUni/COMP2001.git 
   cd COMP2001
2. install dependencies: pip install -r requirements.txt

3. Run the Flask application: python app.py

4.  Access the API via Swagger at http://127.0.0.1:5000/swagger or endpoints like /trails, /trails/<trail_id>.

### How to Run Using Docker
1. Pull the Docker image: docker pull dyldough87/trail-api:latest
2. Run the container: docker run -d -p 5000:5000 dyldough87/trail-api
3. Access the API via Swagger at http://127.0.0.1:5000/swagger.

   #### Repository Structure
1. Dockerfile: Present and ready for containerization.

2. README.md: Contains documentation.

3. app.py: The main application file, crucial for the microservice.

4. requirements.txt: All dependencies listed here—great for easy setup.
   

Testing
All CRUD operations and authentication routes have been tested via Swagger UI. Refer to the report for screenshots and further details.

Contact
For any questions or concerns, please contact Dylan Swallow at dylanswallow@students.plymouth.ac.uk

