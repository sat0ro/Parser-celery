## Installation

### Install Python 3.12

To execute the code you will need Python 3.12. If not, download and install it from [python.org](https://www.python.org).

### Install Docker

To deploy this project you will need Docker. You can install it from [docker.com](https://www.docker.com).

### Clone the Repository

```bash
git clone https://github.com/sat0ro/Parser-celery.git
```


### Install Python Dependencies

Install the required Python dependencies using pip:

```bash
pip install -r requirements.txt
```

## Startup instructions

Step 1: start Docker, open PowerShell and enter the command:

```bash
docker run -p 6379:6379 redis
```

Step 2: open IDE and enter the command in the terminal:

```bash
celery -A tasks worker --loglevel=INFO --pool=solo
```

Step 3: run main.py
