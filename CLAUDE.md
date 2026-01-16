# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Unitree RL Lab is a reinforcement learning framework for training locomotion policies on Unitree robots (Go2 quadruped, H1/G1 humanoids). Built on IsaacLab (NVIDIA robotics simulation) with RSL-RL for PPO training.

## Essential Commands

```bash
# Install package (requires Isaac Lab conda env activated)
conda activate env_isaaclab
./unitree_rl_lab.sh -i

# List available tasks
./unitree_rl_lab.sh -l

# Train a task
./unitree_rl_lab.sh -t --task Unitree-Go2-Velocity

# Run inference/play with trained model
./unitree_rl_lab.sh -p --task Unitree-Go2-Velocity

# Run pre-commit checks (black, flake8, isort)
pre-commit run --all-files
```

## Architecture

### Task Registration System
Tasks are registered with IsaacLab's gymnasium registry. Each task defines:
- `env_cfg_entry_point`: Environment configuration class
- `rsl_rl_cfg_entry_point`: RL agent configuration class
- `play_env_cfg_entry_point`: Inference environment configuration

### Key Directories
- `source/unitree_rl_lab/unitree_rl_lab/tasks/locomotion/robots/{robot}/` - Robot-specific task configs
- `source/unitree_rl_lab/unitree_rl_lab/tasks/locomotion/mdp/` - MDP components (rewards, observations, commands)
- `source/unitree_rl_lab/unitree_rl_lab/assets/robots/` - Robot asset definitions
- `scripts/rsl_rl/` - Training (`train.py`) and inference (`play.py`) scripts
- `deploy/robots/` - C++ controllers for Sim2Real deployment

### Environment Configuration Pattern
Each task's `velocity_env_cfg.py` defines:
- **Scene**: Robot, terrain, sensors (height scanner, contact forces)
- **Observations**: Joint states, base velocity, height map, gait phase
- **Rewards**: Velocity tracking, energy efficiency, orientation penalties
- **Terminations**: Fall detection, episode timeout
- **Events**: Physics randomization, terrain curriculum
- **Commands**: Base velocity commands (vx, vy, wz)

### Training Pipeline
`train.py` uses RSL-RL's OnPolicyRunner with PPO. Checkpoints saved to `logs/rsl_rl/{task_name}/`. `play.py` loads checkpoints and exports policies to JIT (.pt) and ONNX (.onnx) for deployment.

## Code Style

- Line length: 120 characters
- Formatter: Black with preview mode
- Import sorter: isort (black profile)
- Type checking: Pyright (basic mode)
- Docstrings: Google convention
