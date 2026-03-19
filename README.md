# ✨ Fountain Particle System

> A beautiful, real-time 3D particle fountain with physics simulation and realistic lighting

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)

---

## ✨ Features

### 🎨 Visual Effects
- **Realistic Particle Fountain** - Water-like particles spraying upward from a stone basin
- **Advanced Lighting System** - Real light source with inverse square law physics
- **Volumetric Rays** - Crepuscular (god) rays for atmospheric effects
- **Dynamic Shadows** - Real-time shadow casting based on light position and particle distance
- **Color Gradients** - Smooth color transitions and fading effects
- **Particle Trails** - Motion trails showing particle trajectories

### 🔬 Physics Simulation
- **Gravity** - Realistic downward acceleration
- **Air Resistance** - Drag force affecting particle motion
- **Terminal Velocity** - Speed cap to prevent unrealistic acceleration
- **Collision Physics** - Realistic bouncing with energy loss
- **Fountain Mechanics** - Particles shoot upward at realistic angles
- **Particle-to-Particle Interaction** - Subtle gravity wells between particles

### 💡 Lighting & Rendering
- **Inverse Square Law** - Proper light attenuation over distance
- **Color-Aware Lighting** - Particles brighten based on proximity to light source
- **Soft Shadows** - Multi-layer shadow rendering for realism
- **Gradient Background** - Smooth atmospheric gradient
- **Bloom Effects** - Light source with realistic glow

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [License](#license)

---

## 💻 Installation

### Prerequisites
- Python 3.12+
- pip package manager
- Linux/WSL environment (with audio drivers for full functionality)

### Setup Steps

1. **Clone the repository**
```bash
git clone git@github.com:MiladBarani/ClaudeRepo.git
cd ClaudeRepo
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install pygame numpy
```

4. **Optional: Install audio support** (for future enhancements)
```bash
sudo apt install portaudio19-dev python3.12-venv
pip install sounddevice
```

---

## 🎮 Usage

### Running the Application

```bash
cd ClaudeRepo
source venv/bin/activate
python test.py
```

The fountain will start automatically, continuously spawning colored particles that arc upward, fall under gravity, and rest on the floor.

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| **Click** | Create particle burst at mouse position |
| **SPACE** | Pause/Resume simulation |
| **I** | Toggle information display |
| **C** | Clear all particles |
| **ESC** | Exit application |

---

## 🎯 Project Structure

```
ClaudeRepo/
├── test.py              # Main application - Fountain Particle System
├── venv/                # Python virtual environment
├── README.md            # This file
├── LICENSE              # MIT License
└── requirements.txt     # Python dependencies (optional)
```

---

## 📦 Requirements

- **pygame** 2.6.1 - Graphics and window management
- **numpy** 2.4.3 - Numerical computations
- **Python** 3.12+ - Runtime environment

---

## 🔧 Technical Details

### Particle System
The fountain system implements a sophisticated particle engine with:
- Vector-based physics calculations
- Accurate collision detection and response
- Life cycle management with fade-out effects
- Trail rendering for motion visualization

### Lighting Model
- **Light Position**: Center-top of screen
- **Light Color**: Warm white (255, 240, 180)
- **Light Falloff**: Inverse square law - intensity ∝ 1/distance²
- **Shadow Calculation**: Ray-casting from light through particles to floor

### Animation Loop
- **Frame Rate**: 60 FPS target
- **Physics Update**: Per-frame integration
- **Collision Detection**: AABB + circle collision
- **Rendering**: Back-to-front with lighting calculations

---

## 🎨 Customization

You can easily customize various aspects by editing `test.py`:

```python
# Change fountain spawn rate
if random.random() < 0.6:  # Increase to spawn more particles

# Adjust gravity
GRAVITY = 0.15  # Higher = stronger gravity

# Change floor height
FLOOR_HEIGHT = 650  # Lower = particles fall further

# Modify light position
LIGHT_POS = (WIDTH // 2, 100)  # Change fountain lighting

# Add more colors
'cyan': [(50, 255, 255), (100, 255, 255), (150, 255, 255)],
```

---

## 🚀 Performance Tips

- Reduce `NUM_PARTICLES` for better performance on slower systems
- Set particle generation rate lower if FPS drops
- Use I key to hide info display for smoother rendering
- Close other applications to free system resources

---

## 🐛 Troubleshooting

**Particles not appearing?**
- Ensure pygame is properly installed
- Check that the virtual environment is activated

**Low FPS?**
- Reduce `NUM_PARTICLES` constant in test.py
- Decrease fountain spawn rate

**Window issues?**
- Try running in fullscreen or adjusting WIDTH/HEIGHT

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Created with Claude AI assistance

---

## ⭐ Support

If you found this project interesting, please star it on GitHub!

**Repository**: [MiladBarani/ClaudeRepo](https://github.com/MiladBarani/ClaudeRepo)

---

## 🔮 Future Enhancements

- [ ] Add audio visualization integration
- [ ] Multiple fountain sources
- [ ] Interactive light control
- [ ] Particle collision effects
- [ ] Export to video/GIF
- [ ] Configuration file support
- [ ] Preset scenarios
- [ ] 3D perspective mode

---

*Last Updated: March 19, 2026*

# Start building!
```

---

## 📦 Installation

### Prerequisites

- Git 2.0+
- SSH key configured for GitHub
- Node.js 14+ (optional, for future projects)

### Setup

```bash
# Clone the repository
git clone git@github.com:MiladBarani/ClaudeRepo.git
cd ClaudeRepo

# Verify installation
git status
```

---

## 💻 Usage

This repository serves as a template for modern development workflows:

- **Version Control**: All changes are tracked with Git
- **Collaboration**: SSH authentication ensures secure access
- **Documentation**: Well-documented codebase for easy onboarding

---

## 📁 Project Structure

```
ClaudeRepo/
├── README.md           # This file
├── .gitignore          # Git ignore rules
└── docs/               # Documentation (coming soon)
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📖 Development Guidelines

### Code Style
- Follow standard conventions for your language
- Write clear, descriptive commit messages
- Keep functions small and focused

### Testing
- Write tests for new features
- Ensure all tests pass before submitting PR

### Documentation
- Update README for major changes
- Add inline comments for complex logic

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## 💬 Support

Need help? Here are resources:

- 📧 **Email**: milad.jafare@gmail.com
- 🐙 **GitHub Issues**: [Open an issue](https://github.com/MiladBarani/ClaudeRepo/issues)
- 📚 **Documentation**: Check the [docs](./docs) folder

---

## 🎉 Acknowledgments

- Built with ❤️ using Claude AI
- Powered by Git & GitHub
- Created on March 19, 2026

---

## 📊 Repository Stats

- **Repository**: ClaudeRepo
- **Owner**: MiladBarani
- **Created**: March 2026
- **Latest Update**: March 19, 2026

---

<div align="center">

**[⬆ back to top](#clauderepo)**

Made with 💙 by [MiladBarani](https://github.com/MiladBarani)

</div>
