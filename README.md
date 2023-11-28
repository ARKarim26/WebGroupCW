# Template for ECS639U Group Coursework

This template should be used as the starting point for your group coursework in the module ECS639U Web Programming (at Queen Mary University of London). Use Git (github.qmul.ac.uk) to collaborate on the coursework with your group members. Module leader: Paulo Oliva <[p.oliva@qmul.ac.uk](mailto:p.oliva@qmul.ac.uk)>

## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Fork this repo and clone your fork (or clone the forked repo of one of your team members), e.g.

    ```console
    $ git clone https://github.qmul.ac.uk/<username>/cwgroup
    ```

3. Install Pyhton dependencies (main folder):

    ```console
    $ pip install -r requirements.txt
    ```

4. Create a development database:

    ```console
    $ python manage.py migrate
    ```

5. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    $ npm install
    ```

6. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    ```

7. and the Vue server from the 'frontend' sub-folder:

    ```console
    $ npm run dev
    ```

8. Open your browser and go to http://localhost:5173, you will be greeted with a template page.

## OpenShift deployment

Once your project is ready to be deployed you will need to 'build' the Vue app and place it in Django's static folder.

1. The build command in package.json and the vite.config.ts files have already been modified so that when running 'npm run build' the generated JavaScript and CSS files will be placed in the mainapp static folder, and the index.html file will be placed in the templates folder:

    ```console
    $ npm run build
    ```

2. You should then follow the instruction on QM+ on how to deploy your app on EECS's OpenShift live server.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).


Athish's version of read me:

## Requirements
- Python 3.10
- Django 4.2
- Node.js and npm (for Vue.js frontend)

## Installation

Clone the repository:
git clone https://github.com/athi22/WebGroupCW
cd cwgroup

Set up a Python virtual environment and activate it (replace ecs639u-group with your environment name):
Copy code:
conda create --name ecs639u-group python=3.10
conda activate ecs639u-group

Install the required Python dependencies:
Copy code:
pip install -r requirements.txt

Navigate to the frontend directory and install JavaScript dependencies:
Copy code:
cd frontend
npm install

Return to the project root directory, create, and apply database migrations:
Copy code:
cd ..
python manage.py migrate

Start the development server:
Copy code
python manage.py runserver
Access the application at http://127.0.0.1:8000/

Admin panel is available at http://127.0.0.1:8000/admin/ with the credentials:

Username: admin
Password: admin
