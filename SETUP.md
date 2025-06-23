# Setup and Deployment

## Libraries and Services Required

- [Flask](https://flask.palletsprojects.com)
- [Jinja2](https://jinja.palletsprojects.com/templates/)
- [PicoCSS](https://picocss.com/)
- [Turso](https://turso.tech/)


---

## Setting up a Development Environment

To develop locally, you need to setup a **Python virtual environment (venv)** to keep your Python configuration isolated from the rest of your system.

### VS Code Extensions

To support setting up and developing with the Flask server, add the following extensions to VS Code:

- **Python** (from Microsoft)
- **Better Jinja** (from Samuel Colvin)

You should also have the following (just to n=make life better):

- **Code Spell Checker** (because speeling is hard!)
- **Error Lens** (places error messages inline, next to code)


### Create the Virtual Environment

1. In your terminal, navigate to the project root folder

2. **Create** the virtual environment with:

    ```
    python -m venv venv
    ```

2. **Activate** the virtual environment

    *Note: If using __VS Code__'s terminal, VS Code will offer to use / activate the virtual environment for you - select __Yes__, and then relaunch the terminal. If you do this, there is no need for the following command.*

    Windows PowerShell:

    ```
    .\venv\Scripts\activate
    ```

    Linux:

    ```
    source venv/bin/activate
    ```

3. **Install** all required Python libraries:

    ```
    pip install -r requirements.txt
    ```

### Using a Previously Created Virtual Environment

If you are returning to your project, you do not need to recreate your virtual environment, just activate and update it.

*Note: If using __VS Code__ as mentioned above, VS Code will __automatically__ activate the environment as time you open its Terminal, and you don't need to do anything.*


### Launching the Server Locally

The Flask project is configured as a module called **app** (with main code in **\_\_init__.py**), which allows the the server to be run very easily with:

```
flask run --debug
```

The server should start and will present a URL link, usually 127.0.0.1:5000


---

## Setting Up a Turso Database

Turso provides an online SQLite-like database service. Your app need to be able to securely connect to and access the database that you create. This is done using a secret key / access token.

### Turso Account

Go to [Turso](https://turso.tech/) and login with your **GitHub** credentials. You will be on the free plan by default.


### Create a Database

1. Create a new database in the Turso dashboard.

2. Use the **Edit Data** function within Turso to setup columns, add records, etc. (the Drizzle Studio editor is the most straightforward to use). Or you can skip this and instead setup and initialise the database via the Flask app **init_db()** function.


### API Access Token and URL

1. From the Turso dashboard, click the three-dot menu next to the database and select **Create Token**:

    - Expires: **never**
    - Auth Level: **Read & Write**

2. Copy the database access token and URL to the **.env** file.

    *Note: You will need to alter the URL from `libsql://...` to `https://...`*


---

## Deploying Your App to Render

Deploying to **Render**, an external web app host, is pretty simple. Once setup, every time you push changes to your repo, the app will be updated and redeployed.


### Render Account

1. Go to [Render](https://render.com/) and **Sign in with GitHub**

2. Sign up for the Hobby ($0) plan


### Create a Web App

1. Create a new **Web Service**

2. To see your list of **GitHub repos**, you will need to add credentials so that Render has access to your repos.

3. Select this repo from the list


### Configure the Web App

1. In the deployment settings, set the following:

    - Name: Can customise if you wish
    - Language: **Python 3**
    - Branch: **main**
    - Region: **Singapore**
    - Root Directory: *Leave blank*
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `flask run`
    - Instance Type: **Free**
    - Environment Variables:
        - TURSO_URL      *copy from your .env file*
        - TURSO_KEY      *copy from your .env file*
        - SESSION_KEY    *copy from your .env file*
        - FLASK_RUN_HOST **0.0.0.0**
        - FLASK_RUN_PORT **10000**


2. **Deploy** the web service, and it should be good to go!


### Access the Deployed App

In the Render dashboard:

- Go to your web app

- Note the the **public URL** generated for the deployed app.


### Updating the Deployed App

Every time you **push changes** to your GitHub repo, Render will **automatically re-deploy** the app - there is nothing you need to do.

