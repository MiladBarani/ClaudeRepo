# ✨ Advanced Particle Physics Engine with Realistic Lighting

> A sophisticated 2D particle system simulation built with Python and Pygame, featuring realistic physics, dynamic lighting, and beautiful visual design.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)

---

## ✨ Features

### 🎨 Visual Effects
- **Beautiful Sky Background** - Gradient sky with procedurally generated clouds
- **Realistic Particle Fountain** - Particles fountain from a fixed basin at the bottom
- **Advanced Lighting System** - Fixed light source at top with inverse square law physics
- **Dynamic Shadows** - Real-time shadow casting based on light position
- **Color Gradients** - Smooth particle color transitions and fading (Red, Blue, Green, Purple, Orange)
- **Particle Trails** - Motion trails showing particle trajectories
- **Glow Effects** - Particles emit subtle light halos

### 🔬 Physics Simulation
- **Gravity** - Realistic downward acceleration (0.15 m/frame²)
- **Air Resistance** - Drag force affecting particle motion (0.995 factor)
- **Terminal Velocity** - Speed cap at 20 pixels/frame to prevent unrealistic acceleration
- **Collision Physics** - Realistic bouncing with energy loss (0.85 damping)
- **Fountain Mechanics** - Particles spray upward at realistic angles from fountain
- **Particle-to-Particle Interaction** - Subtle gravity wells between nearby particles
- **Floor Friction** - Velocity loss when particles slide on floor (0.95)

### 💡 Lighting & Rendering
- **Inverse Square Law** - Proper light attenuation: intensity = 1 / (1 + (distance/100)²)
- **Color-Aware Lighting** - Particles brighten based on proximity to light source
- **Soft Shadows** - Multi-layer shadow rendering for realistic depth
- **Bright Fountain Area** - Enhanced floor lighting around fountain
- **Light Source Bloom** - Realistic light core with glow layers

### 🎮 Interactive Controls
- **Click to Create Bursts** - Left-click to spawn particle bursts at cursor
- **Speed Adjustment** - Real-time animation speed control (0.1x to 5.0x)
- **Pause/Resume** - Freeze simulation with SPACE key
- **Info Toggle** - Show/hide on-screen statistics
- **Clear Particles** - Remove all particles instantly

### 🏗️ Software Architecture
- **Layered Design** - Configuration, Utility, Domain, Presentation, Application layers
- **Separation of Concerns** - Physics, Lighting, and Rendering engines are independent
- **Static Utility Methods** - Pure functions for physics calculations
- **Easy to Extend** - Add features without breaking existing code
- **Configurable** - All magic numbers centralized in Config class

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Architecture](#architecture)
- [Customization](#customization)
- [Requirements](#requirements)
- [License](#license)

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
