# Godot ML Toolkit

Godot ML Toolkit is an open-source project that allows video game developers to integrate intelligent agents into their games.
The main features are:
- Support for both single and multi agent environments using the Godot game engine
- Ability to control an agent through an algorithm or user I/O
- Speed up the simulation speed for faster training times

This project was built for an internship for my Bachelor's Degree in Artificial Intelligence and Data Science.

The corresponding Godot 4 plugin can be found [here](https://github.com/campiao/Godot-ML-Toolkit-Plugin).

A simple showcase using the example environments can be seen [here](https://youtu.be/DEHcFC5Y1jc).

[!(https://img.youtube.com/vi/DEHcFC5Y1jc/maxresdefault.jpg)](https://youtu.be/DEHcFC5Y1jc)

## Getting Started

### Installation
Before installing the package, it is highly recommended to create a virtual environment. To do that, you can use venv or conda.

After setting up your virtual environment, clone the repository and go to the project folder to install it by running:

```bash
pip install .
```

To use one of example environments, run one of the provided files or use your own solution:

```bash
godot-mlagents path/to/solution/file.py
```

## Creating Custom Environments
To implement your own environments, start by creating your project. Then, download and enable the Godot ML Toolkit Plugin.

Add a AIController Node to any other node in your game to controll it. Then, click on `Extend Script` on the AIController, creating a new script which will define how your agent behaves. Implement all the necessary methods before running your game.

Add an AgentsManager node to your scene tree and you are now ready to start interacting with the Python API. 
