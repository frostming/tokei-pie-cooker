# Tokei Pie Cooker

[![pdm-managed](https://img.shields.io/endpoint?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fpdm-project%2F.github%2Fbadge.json)](https://pdm-project.org)

Visualize your code statistics with Pie Chart

---

🚀 [Demo Website](https://piechart.zeabur.app/) 🚀

## Start locally

This project requires Python 3.10 or later.

It is managed by [PDM](https://pdm-project.org/). Please refer to the [Installation Guide](https://pdm-project.org/en/latest/#installation) to install PDM first.

```bash
# install dependencies
pdm install
# start development server
pdm dev
# Now visit http://localhost:5000
```

## Deployment

### As a container

```bash
docker run -v ./tokei-caches:/app/.caches -p 8000:8000 -d frostming/tokei-pie-cooker

# Visit http://localhost:8000
```

## Credits

- [tokei](https://github.com/XAMPPRocky/tokei)
- [tokei-pie](https://github.com/laixintao/tokei-pie)
