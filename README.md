# Getting Started 

## Pre-Requisite

__Version used for Project__
- __[<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/>](https://www.python.org/downloads/release/python-3105/)__ Python 3.10
- __[<img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/>](https://docs.djangoproject.com/en/5.0/)__ Django 5.0
- __[<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original.svg" alt="nodejs" width="40" height="40"/>](https://nodejs.org/en)__ Node.js >=18
- __[<img src="https://angular.io/assets/images/logos/angular/angular.svg" alt="angular" width="40" height="40"/>](https://github.com/angular/angular-cli)__ Angular 17

# Development Setup

Before you begin, ensure you have the following installed on your system:

1. **Node.js (Version 20 or above)**: This includes the Node Package Manager (npm). You can download and install Node.js from [the official Node.js website](https://nodejs.org/). Make sure to install Node.js version 20 or above.

2. **Python 3.10.5**: Download and install Python 3.10.5 from [the official Python website](https://www.python.org/downloads/release/python-3105/).

## Setting Up a Project

### Install Angular CLI

To install Angular CLI version 17 globally, run the following command in your terminal:

```bash
npm install -g @angular/cli@17
```

### Clone the Repository

To build and run the project using Docker, follow these steps:

First, clone the repository to your local machine:

```bash
$ git clone <repository_url>
```

```bash 
cd <repository_name>
```

Replace <repository_url> with the URL of your repository and <repository_name> with the name of the repository folder.

### Build the Docker Images

Run the following command to build the Docker images:

```bash 
docker-compose build
```

### Start the Docker Containers

After building the images, start the Docker containers using the following command:

```bash
docker-compose up
```

This command will launch your application and it will be ready for use with the configured API key.

### Access the Application

Once the containers are up and running, you can access the application via the URL or port specified in your docker-compose.yml file.

## Contributing 

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are welcome.
