# 🎮 Platformer

A 2D platformer game built with **Python** and **pygame-ce**.

The project contains multiple levels stored as JSON maps, a playable game client, and a utility for visualizing level layouts.

## ✨ Features

* 🕹️ 2D platformer gameplay
* 🗺️ Multiple levels
* 📄 Levels stored as JSON files
* 🎨 Level visualization with NumPy and Matplotlib
* ⚙️ Simple and easy-to-understand project structure
* 🖥️ Ready-to-run EXE version available
* 🐍 Built with Python and pygame-ce

## 🎮 Controls

| Key           | Action       |
|---------------| ------------ |
| `←`           | Move left    |
| `→`           | Move right   |
| `Space` / `↑` | Jump         |
| `Esc`         | Exit / pause |

## 📥 Installation

### Requirements

* **Python 3.14.7**
* `pip`

Make sure that the Python version matches the version used for development.

### Install dependencies

Clone the repository and open a terminal in the project directory:

```bash
git clone https://github.com/artem121112111211-coder/Platformer.git
cd Platformer
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Game

From the repository directory, run:

```bash
python main.py
```

## 🗺️ Level Visualization

`level.py` is a development utility used to visualize the game's level maps.

It reads the JSON level files from the `Levels` directory and generates PNG images representing their layouts.

To generate the level images, run:

```bash
python level.py
```

The generated images are saved in the `Levels` directory.

### Dependencies used by `level.py`

* **NumPy** — processes the level matrix.
* **Matplotlib** — renders the level as an image.

## 📦 EXE Version

A ready-to-run **EXE version** is available in:

**<a href="https://github.com/artem121112111211-coder/Platformer/releases"><strong>GitHub Releases</strong></a>**

The EXE version does not require manually running `main.py`.

## 📁 Project Structure

```text
Platformer/
│
├── Icon/
│   └── ...                  # Game icons and graphical resources
│
├── Levels/
│   ├── level1.json         # Level 1 map
│   ├── level2.json         # Level 2 map
│   ├── level3.json         # Level 3 map
│   ├── level4.json         # Level 4 map
│   └── ...                 # Generated level images/resources
│
├── main.py                 # Main game program
├── level.py                # Level visualization utility
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── LICENSE                 # Project license
└── README.md               # Project documentation
```

## 🛠️ For Developers

### Main game

The main game logic is located in `main.py`.

To start the game during development:

```bash
python main.py
```

### Level files

Game levels are stored in the `Levels` directory as JSON files.

The level data is loaded by the game and can also be visualized using:

```bash
python level.py
```

When modifying a level, regenerate its visualization if you want to update the corresponding PNG preview.

### Dependencies

Project dependencies are listed in `requirements.txt`.

To install them:

```bash
pip install -r requirements.txt
```

When adding a new external Python dependency, add it to `requirements.txt` so that other developers can reproduce the development environment.

## 🔧 Development Workflow

A typical workflow for contributing to the project:

```bash
git pull
```

Make your changes, test the game, and then commit them:

```bash
git add .
git commit -m "Describe your changes"
git push
```

For level-related changes, it is recommended to test both:

```bash
python main.py
```

and:

```bash
python level.py
```

## 📄 License

This project is distributed under the license included in the [`LICENSE`](LICENSE) file.

## 👤 Author

**Artem**

GitHub: <a href="https://github.com/artem121112111211-coder"><strong>artem121112111211-coder</strong></a>
