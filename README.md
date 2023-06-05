
# project-equilibrium

a minimal workspace.
## Features

- neco-arc (why not)
- a simple todolist (finished)
- a pomodoro timer (inaccurate, will be customizable)
- an AI-powered chatbot that generates random messages (in development)
- a beautiful and comfortable [dark color scheme](https://github.com/monkeytypegame/monkeytype/blob/16c956c62c241deb9c3ffd0f3b3647625df4156e/frontend/static/themes/serika_dark.css) to reduce eye strain and help you focus.
## Dependencies

- [Python](https://www.python.org/downloads/) 3.11.3 or above.
- [Node.js](https://nodejs.org/en/download) 18.16.0 or above.
- [git](https://git-scm.com/downloads)
## Installation

Make sure the depencencies are installed on your local machine.
```
$ python --version
Python 3.11.3
$ npm --version
9.6.4
$ git --version
git version 2.40.0.windows.1
```
Clone the repository:
```
$ git clone https://github.com/NTDuck/project-equilibrium.git
$ cd project-equilibrium
```
Install the required packages:
```
# windows
$ python -m venv venv
$ venv\Scripts\activate

# macos/linux
$ python3 -m venv venv
$ source venv/bin/activate
```
```
(venv) $ pip install -r requirements.txt
(venv) $ npm install
```
Alternatively, for ensured version conflict/incompatibility:
```
(venv) $ pip install flask flask-moment flask-sqlalchemy flask-migrate Flask-HTMLmin python-dotenv
(venv) $ pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
(venv) % pip install transformers
```

## Deployment

To start the server, simply run:
```
(venv) $ flask run
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

## Screenshots

![](/app/static/images/.github/screenshot.jpeg)
## License

[MIT](LICENSE)


## Acknowledgements

- Gifs from [Seseren](https://www.pixiv.net/en/users/16274829), [u/BeardyDuck](https://www.reddit.com/user/BeardyDuck/) from [r/meltyblood](https://www.reddit.com/r/meltyblood/comments/wtpt66/neco_arc_pngs_are_available_so_i_made_some_select/).
- Audio by Herta from Honkai: Star Rail.


## Support

If you wish to support further development and feel extra awesome, you can [buy me a coffee](https://www.buymeacoffee.com/ntduck).

