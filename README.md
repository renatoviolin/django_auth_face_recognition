# Django User Authentication using Face Recognition

*THIS IS NOT READY TO PRODUCTION*, as it needs to improve the face anti-spoofing attacks.

This application aims to integrate a deep learning face recognition model to authenticate the user. It is a toy application with purpouse to integrate Django Framework with a deep learning model.

To achieve the results, those models were are: 

1) Multi Task Cascade CNN (MTCNN) to extract faces.
2) [Facenet Pytorch](https://github.com/timesler/facenet-pytorch) to extract features of the faces.

The web-app is using [SB Admin 2](https://github.com/StartBootstrap/startbootstrap-sb-admin-2) free template, and sqlite database to store user profile and embeddings.


# Application
### Try to access before upload a picture.
![Validation](validation1.gif)


### Uploading the picture in profile page, and trying to authenticate again.
![Validation](validation2.gif)


### Trying to cheat the app using a picture from a mobile screen.
![Hacking](validation3.gif)


### Install

```
pip install -r requirements.txt
```


### Running 

After install the requirements, start the Django app, migrate the database, creating a superuser and running the server.
```
cd auth_app
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

Open your browser http://localhost:8000

1. Create a new user using the registration form.
2. Login with your new user.
3. In top right menu, access Profile.
4. Upload your picture's face.
5. Save
6. Logout
7. In login page you should be able to access using only your face.


### Implement details

All face images will be stored in /media/users folders.

At upload time, the embeddings of the picture is calculated and store in the sqlite table.

At auth time, a JavaScript script take the picture (in a interval of 2 seconds), and call the endpoint to validate the picture. If success, the callback call the default login method of Django.

The threshold is defined as 0.9 in the file face_app.py. This value (almost) avoid hack the system with a valid picture displayed at the mobile screen.

Two or more faces in the screen is ignored return "invalid user".
