

 ALLEGRO HANDLING TIME AUTOMATION
------------------------------------------------------------
------------------------------------------------------------
Automated system for managing Allegro offer handling times
based on a configurable target date.


------------------------------------------------------------
OVERVIEW
------------------------------------------------------------

This application integrates with the Allegro API and
automatically adjusts the handling time of offers depending
on how many days remain until a specified target date.

It works as a lightweight backend service with scheduled
automation.


------------------------------------------------------------
KEY FEATURES
------------------------------------------------------------

- OAuth2 integration with Allegro API
- Per-offer target date configuration
- Bulk updates for multiple offers
- Dynamic handling time calculation
- Automated daily updates (cron)
- Test coverage using pytest


------------------------------------------------------------
TECH STACK
------------------------------------------------------------

* Backend:    Python, Django, Django REST Framework
* Database:   PostgreSQL
* Testing:    pytest


------------------------------------------------------------
SETUP
------------------------------------------------------------

1. Clone repository

   * git clone https://github.com/kamilszy123/django-order-handling-time-service.git
   * cd django-order-handling-time-service


2. Create virtual environment

   * python3 -m venv venv

   * Linux:
     source venv/bin/activate

   * Windows:
     venv\Scripts\activate


3. Install dependencies

   pip install -r requirements.txt


4. Register application on Allegro (sandbox): https://apps.developer.allegro.pl.allegrosandbox.pl/
    * set app name: TimeControlApp
    * To function correctly, the application must be granted the following Allegro API permissions:
        * allegro:api:sale:offers:read – enables access to retrieve offer data
        * allegro:api:sale:offers:write – enables creating, updating, linking, and closing offers
    * Chose option - The application will have access to a web browser, which will be used by the user to log in to Allegro (e.g., a server-hosted application or an executable file).

    * you will receive your CLIENT ID and CLIENT SECRET

------------------------------------------------------------
CONFIGURATION
------------------------------------------------------------

Create a `.env` file:

    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    
    DJANGO_SECRET_KEY='your_django_secret_key'
    
    ALLEGRO_CLIENT_ID=your_client_id
    ALLEGRO_CLIENT_SECRET=your_client_secret
    BASE_URL=your_redirect_base_url


------------------------------------------------------------
DATABASE
------------------------------------------------------------

   python manage.py migrate


------------------------------------------------------------
RUN APPLICATION
------------------------------------------------------------

   python manage.py runserver

------------------------------------------------------------
ALLEGRO USER AUTHORIZATION
------------------------------------------------------------

To authorize the application (only needed once), open the following URL
in a web browser:

https://allegro.pl.allegrosandbox.pl/auth/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI


Replace:

- YOUR_CLIENT_ID      -> your actual Client ID
- YOUR_REDIRECT_URI   -> your application's redirect URL


The redirect_uri should be constructed as:

   BASE_URL (from .env) + /api/allegro/callback/

Example:

   https://example-domain.com/api/allegro/callback/


IMPORTANT:

The redirect_uri cannot be a localhost address.
It must be publicly accessible.

For local development, you can use tools like ngrok
to expose your application to the internet.


After opening the authorization URL:

1. User logs in to Allegro
2. Grants required permissions
3. Allegro redirects to redirect_uri with authorization code


------------------------------------------------------------
API
------------------------------------------------------------

Create / Update configuration for one offer:

   POST /config/

       {
         "offer_id": "123",
         "target_date": "2026-04-20"
       }


Get all configurations:

   GET /config/


Bulk update:

   POST /config/all/

       {
         "target_date": "2026-04-20"
       }


------------------------------------------------------------
AUTOMATION
------------------------------------------------------------

Run manually:

   python manage.py update_handling_time


Cron job (daily at 02:00):

   add script run_cron.sh to project
      #!/bin/bash
      
      cd /path/to/project
      source venv/bin/activate
      python manage.py update_handling_time

0 2 * * * /path/to/project/run_cron.sh >> /tmp/cron.log 2>&1


------------------------------------------------------------
TESTS
------------------------------------------------------------

   pytest


------------------------------------------------------------
HOW IT WORKS
------------------------------------------------------------

1. User sets a target date
2. System calculates remaining days
3. Handling time is updated
4. Scheduled job keeps everything in sync


