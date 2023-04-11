# 499 Simulations
## Setup

### EP Simulations:

```bash
sudo add-apt-repository ppa:fenics-packages/fenics
sudo apt update
sudo apt install fenicsx
```

### Circuit Simulations

```bash
sudo apt install libngspice0 libngspice0-dev
pip install PySpice
pyspice-post-installation --check-install
```
Drawing
```bash
pip install schemdraw
pip install schemdraw[matplotlib]
pip install schemdraw[svgmath]
pip install --upgrade jupyterthemes
```

