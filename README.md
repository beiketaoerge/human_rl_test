# Unitree RL Lab

[![IsaacSim](https://img.shields.io/badge/IsaacSim-5.1.0-silver.svg)](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html)
[![Isaac Lab](https://img.shields.io/badge/IsaacLab-2.3.0-silver)](https://isaac-sim.github.io/IsaacLab)
[![License](https://img.shields.io/badge/license-Apache2.0-yellow.svg)](https://opensource.org/license/apache-2-0)
[![Discord](https://img.shields.io/badge/-Discord-5865F2?style=flat&logo=Discord&logoColor=white)](https://discord.gg/ZwcVwxv5rq)


## 概述 (Overview)

本项目提供了一套基于 [IsaacLab](https://github.com/isaac-sim/IsaacLab) 构建的 Unitree 机器人强化学习环境。

目前支持 Unitree **Go2**, **H1** 和 **G1-29dof** 机器人。

<div align="center">

| <div align="center"> Isaac Lab </div> | <div align="center">  Mujoco </div> |  <div align="center"> 实体机器人 (Physical) </div> |
|--- | --- | --- |
| [<img src="https://oss-global-cdn.unitree.com/static/d879adac250648c587d3681e90658b49_480x397.gif" width="240px">](g1_sim.gif) | [<img src="https://oss-global-cdn.unitree.com/static/3c88e045ab124c3ab9c761a99cb5e71f_480x397.gif" width="240px">](g1_mujoco.gif) | [<img src="https://oss-global-cdn.unitree.com/static/6c17c6cf52ec4e26bbfab1fbf591adb2_480x270.gif" width="240px">](g1_real.gif) |

</div>

## 安装指南 (Installation)

- 按照[安装指南](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html)安装 Isaac Lab。
- 安装 Unitree RL IsaacLab 独立环境。

  - 将本仓库克隆或复制到 Isaac Lab 安装目录之外（即不要放在 `IsaacLab` 目录中）：

    ```bash
    git clone https://github.com/unitreerobotics/unitree_rl_lab.git
    ```
  - 使用已安装 Isaac Lab 的 python 解释器，以可编辑模式安装本库：

    ```bash
    conda activate env_isaaclab
    ./unitree_rl_lab.sh -i
    # 重启 shell 以激活环境更改。
    ```
- 下载 Unitree 机器人描述文件

  *方法 1: 使用 USD 文件*
  - 从 [unitree_model](https://huggingface.co/datasets/unitreerobotics/unitree_model/tree/main) 下载 unitree usd 文件，保持文件夹结构
    ```bash
    git clone https://huggingface.co/datasets/unitreerobotics/unitree_model
    ```
  - 在 `source/unitree_rl_lab/unitree_rl_lab/assets/robots/unitree.py` 中配置 `UNITREE_MODEL_DIR`。

    ```bash
    UNITREE_MODEL_DIR = "</home/user/projects/unitree_usd>"
    ```

  *方法 2: 使用 URDF 文件 [推荐]* 仅适用于 Isaacsim >= 5.0
  -  从 [unitree_ros](https://github.com/unitreerobotics/unitree_ros) 下载 unitree 机器人 urdf 文件
      ```
      git clone https://github.com/unitreerobotics/unitree_ros.git
      ```
  - 在 `source/unitree_rl_lab/unitree_rl_lab/assets/robots/unitree.py` 中配置 `UNITREE_ROS_DIR`。
    ```bash
    UNITREE_ROS_DIR = "</home/user/projects/unitree_ros/unitree_ros>"
    ```
  - [可选]: 如果你想使用 urdf 文件，请修改 *robot_cfg.spawn*



- 通过以下方式验证环境是否正确安装：

  - 列出可用任务：

    ```bash
    ./unitree_rl_lab.sh -l # 这是比 isaaclab 更快的版本
    ```
  - 运行任务：

    ```bash
    ./unitree_rl_lab.sh -t --task Unitree-G1-29dof-Velocity # 支持任务名称自动补全
    # 等同于
    python scripts/rsl_rl/train.py --headless --task Unitree-G1-29dof-Velocity
    ```
  - 使用训练好的智能体进行推理（Play）：

    ```bash
    ./unitree_rl_lab.sh -p --task Unitree-G1-29dof-Velocity # 支持任务名称自动补全
    # 等同于
    python scripts/rsl_rl/play.py --task Unitree-G1-29dof-Velocity
    ```

## 训练配置 (Training Configuration)

### 命令行参数
你可以直接通过命令行参数配置基本的训练参数：
- `--num_envs`: 并行环境的数量（例如：`--num_envs 4096`）。
- `--max_iterations`: 最大训练迭代次数。
- `--seed`: 用于复现的随机种子。
- `--video`: 在训练期间启用视频录制。
- `--video_interval`: 视频录制之间的间隔（步数）。
- `--video_length`: 录制视频的长度。

示例：
```bash
./unitree_rl_lab.sh -t --task Unitree-DT114-Velocity --num_envs 2048 --max_iterations 1000
```

### 超参数
如需进行高级配置（PPO 超参数、网络架构等），请修改配置文件：
`source/unitree_rl_lab/unitree_rl_lab/tasks/locomotion/agents/rsl_rl_ppo_cfg.py`

`BasePPORunnerCfg` 中的关键参数：
- `num_steps_per_env`: 每次迭代中每个环境的步数。
- `policy`: 网络架构（例如：`actor_hidden_dims`, `activation`）。
- `algorithm`: PPO 特定参数（例如：`learning_rate`, `entropy_coef`, `gamma`）。

## 回放与可视化指南 (Playback & Visualization Guide)

本节介绍如何在不同场景下调试、可视化和录制训练好的策略。

### 1. 交互式调试 (仅可视化)
**目标**：在本地显示器上实时观看机器人的行为。不保存视频。

```bash
./unitree_rl_lab.sh -p \
    --task Unitree-DT114-Velocity \
    --load_run 2026-01-18_19-01-59 \
    --checkpoint model_10700.pt \
    --real-time
```

*   **关键标志**：
    *   `--real-time`: 强制仿真以 1.0x 速度运行。如果不加此参数，它将尽可能快地运行（适合收集数据，不适合观看）。
    *   **(不加 --headless)**: 确保 Isaac Sim GUI 窗口打开。
    *   **(不加 --video)**: 禁用录制以节省资源。

### 2. 后台录制 (仅录制)
**目标**：在远程服务器（或本地）上生成视频文件，而不打开窗口。

```bash
./unitree_rl_lab.sh -p \
    --task Unitree-DT114-Velocity \
    --load_run 2026-01-18_19-01-59 \
    --checkpoint model_10700.pt \
    --headless \
    --video \
    --video_length 200
```

*   **关键标志**：
    *   `--headless`: 不运行 GUI 窗口（服务器必备）。
    *   `--video`: 启用相机传感器和视频写入器。
    *   `--video_length 200`: 录制 200 步后自动退出。
*   **输出**：视频保存在 `logs/rsl_rl/<experiment>/<run>/videos/play/`。

### 3. 交互式录制 (可视化 + 录制)
**目标**：在观看仿真的同时将其录制到文件中。用于检查摄像机角度。

```bash
./unitree_rl_lab.sh -p \
    --task Unitree-DT114-Velocity \
    --load_run 2026-01-18_19-01-59 \
    --checkpoint model_10700.pt \
    --real-time \
    --video
```

### 模式总结

| 模式 | 命令标志 | GUI 窗口 | 视频文件 | 速度 |
| :--- | :--- | :---: | :---: | :--- |
| **调试 / 观看** | `--real-time` | ✅ | ❌ | 实时 |
| **服务器录制** | `--headless --video` | ❌ | ✅ | 快速 |
| **观看并录制**| `--real-time --video` | ✅ | ✅ | 实时 |

## 部署 (Deploy)

模型训练完成后，我们需要在 Mujoco 中对训练好的策略进行 sim2sim 测试，以验证模型性能。
然后进行 sim2real 部署。

### 设置 (Setup)

```bash
# 安装依赖
sudo apt install -y libyaml-cpp-dev libboost-all-dev libeigen3-dev libspdlog-dev libfmt-dev
# 安装 unitree_sdk2
git clone git@github.com:unitreerobotics/unitree_sdk2.git
cd unitree_sdk2
mkdir build && cd build
cmake .. -DBUILD_EXAMPLES=OFF # 安装到 /usr/local 目录
sudo make install
# 编译 robot_controller
cd unitree_rl_lab/deploy/robots/g1_29dof # 或其他机器人
mkdir build && cd build
cmake .. && make
```

### Sim2Sim

安装 [unitree_mujoco](https://github.com/unitreerobotics/unitree_mujoco?tab=readme-ov-file#installation)。

- 在 `/simulate/config.yaml` 中设置 `robot` 为 g1
- 设置 `domain_id` 为 0
- 设置 `enable_elastic_hand` 为 1
- 设置 `use_joystck` 为 1。

```bash
# 启动仿真
cd unitree_mujoco/simulate/build
./unitree_mujoco
# ./unitree_mujoco -i 0 -n eth0 -r g1 -s scene_29dof.xml # 备选方案
```

```bash
cd unitree_rl_lab/deploy/robots/g1_29dof/build
./g1_ctrl
# 1. 按 [L2 + Up] 让机器人站起来
# 2. 点击 mujoco 窗口，然后按 8 让机器人脚接触地面。
# 3. 按 [R1 + X] 运行策略。
# 4. 点击 mujoco 窗口，然后按 9 禁用松紧带。
```

### Sim2Real

你可以使用此程序直接控制机器人，但请确保已关闭板载控制程序。

```bash
./g1_ctrl --network eth0 # eth0 是网络接口名称。
```

## 致谢 (Acknowledgements)

本仓库建立在以下开源项目的支持和贡献之上。特别感谢：

- [IsaacLab](https://github.com/isaac-sim/IsaacLab): 训练和运行代码的基础。
- [mujoco](https://github.com/google-deepmind/mujoco.git): 提供强大的仿真功能。
- [robot_lab](https://github.com/fan-ziqi/robot_lab): 项目结构和部分实现的参考。
- [whole_body_tracking](https://github.com/HybridRobotics/whole_body_tracking): 用于运动跟踪的通用人形控制框架。
