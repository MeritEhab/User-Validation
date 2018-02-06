# Two Steps Validation
A simple 2 steps validation application that enables user to  register without password, when logging in provide password that creates or gets token for him   

### Installation

Create a virtualenv for the project, and run:

```pip install -r requirements.txt```

Run python ```manage.py migrate```

### Usage

To make an account run 
```python manage.py createsuperuser```

Then run ```python manage.py runserver```

And test functionality theough this links  

http://localhost:8000/account

http://localhost:8000/account/login

http://localhost:8000/account/status

