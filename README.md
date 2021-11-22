# Tokei Pie Cooker

Visualize your code statistics with Pie Chart

---

🚀 [Demo Website](https://tokei-pie-cooker.herokuapp.com/) 🚀

## Start locally

This project is developed on Python 3.10, while it should run smoothly on Python>=3.7.

```bash
# make a virtualenv
python3 -m venv venv
# install requirements
venv/bin/python -m pip -r requirements.txt
# start development server
venv/bin/flask run
# Now visit http://localhost:8000
```

## Deployment

### Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### As a container

```bash
docker run -v ./tokei-caches:/app/.caches -p 8000:8000 -d frostming/tokei-pie-cooker

# Visit http://localhost:8000
```

## Credits

- [tokei](https://github.com/XAMPPRocky/tokei)
- [tokei-pie](https://github.com/laixintao/tokei-pie)
