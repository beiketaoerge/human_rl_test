# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for DT114 humanoid robot."""

import os
import shutil

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.utils import configclass

# Path to the DT114 URDF package
DT114_URDF_DIR = "/home/tao/Downloads/unitree_rl_lab/urdf_dt_114"


@configclass
class DT114ArticulationCfg(ArticulationCfg):
    """Configuration for DT114 articulations."""

    joint_sdk_names: list[str] = None
    soft_joint_pos_limit_factor = 0.9


@configclass
class DT114UrdfFileCfg(sim_utils.UrdfFileCfg):
    """URDF configuration for DT114 with mesh path handling."""

    fix_base: bool = False
    activate_contact_sensors: bool = True
    replace_cylinders_with_capsules = True
    joint_drive = sim_utils.UrdfConverterCfg.JointDriveCfg(
        gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0, damping=0)
    )
    articulation_props = sim_utils.ArticulationRootPropertiesCfg(
        enabled_self_collisions=True,
        solver_position_iteration_count=8,
        solver_velocity_iteration_count=4,
    )
    rigid_props = sim_utils.RigidBodyPropertiesCfg(
        disable_gravity=False,
        retain_accelerations=False,
        linear_damping=0.0,
        angular_damping=0.0,
        max_linear_velocity=1000.0,
        max_angular_velocity=1000.0,
        max_depenetration_velocity=1.0,
    )

    def replace_asset(self):
        """Set up symlinks and modify URDF for mesh resolution.

        The original URDF uses 'package://simstl装配另存/meshes/' paths.
        This function creates a temporary directory structure with symlinks
        and a modified URDF that uses relative paths.
        """
        # Create temporary directory structure
        tmp_dir = "/tmp/IsaacLab/unitree_rl_lab/dt114"
        meshes_symlink = f"{tmp_dir}/meshes"

        os.makedirs(tmp_dir, exist_ok=True)

        # Remove existing symlink if present
        if os.path.islink(meshes_symlink):
            os.remove(meshes_symlink)
        elif os.path.exists(meshes_symlink):
            shutil.rmtree(meshes_symlink)

        # Create symlink to meshes directory
        meshes_dir = f"{DT114_URDF_DIR}/meshes"
        os.symlink(meshes_dir, meshes_symlink)

        # Copy URDF and update paths
        urdf_src = f"{DT114_URDF_DIR}/urdf/simstl装配另存.urdf"
        self.asset_path = f"{tmp_dir}/dt114.urdf"

        if os.path.exists(self.asset_path):
            os.remove(self.asset_path)

        # Read URDF and update package paths to relative paths
        with open(urdf_src, "r", encoding="utf-8") as f:
            urdf_content = f.read()

        # Replace package:// paths with relative paths
        urdf_content = urdf_content.replace("package://simstl装配另存/meshes/", "meshes/")

        with open(self.asset_path, "w", encoding="utf-8") as f:
            f.write(urdf_content)


# Create spawn config instance and set up paths
_dt114_spawn_cfg = DT114UrdfFileCfg(
    asset_path=f"{DT114_URDF_DIR}/urdf/simstl装配另存.urdf",  # Will be replaced
)
_dt114_spawn_cfg.replace_asset()


UNITREE_DT114_CFG = DT114ArticulationCfg(
    spawn=_dt114_spawn_cfg,
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.78),  # Initial height based on leg kinematics
        joint_pos={
            # Legs - slight crouch for stability
            # NOTE: Isaac Sim converts "0_" prefix to "a__"
            "a__.*_hip_pitch_joint": -0.15,
            "a__.*_hip_roll_joint": 0.0,
            "a__.*_hip_yaw_joint": 0.0,
            "a__.*_knee_joint": 0.35,
            "a__.*_ankle_pitch_joint": -0.2,
            "a__.*_ankle_roll_joint": 0.0,
            # Waist
            "waist_yaw_joint": 0.0,
            "waist_roll_joint": 0.0,
            "torso_joint": 0.0,
            # Head
            "head_joint": 0.0,
            # Arms - relaxed pose
            # NOTE: Isaac Sim converts "1_" prefix to "a__"
            "a__.*_shoulder_pitch_joint": 0.3,
            "a__left_shoulder_roll_joint": 0.2,
            "a__right_shoulder_roll_joint": -0.2,
            "a__.*_elbow_joint": 0.6,
            ".*_wrist_roll_joint": 0.0,
            ".*_wrist_pitch_joint": 0.0,
        },
        joint_vel={".*": 0.0},
    ),
    actuators={
        # Leg main actuators - hip pitch and hip yaw (high torque)
        # NOTE: Isaac Sim converts "0_" prefix to "a__"
        "legs_main": ImplicitActuatorCfg(
            joint_names_expr=[
                "a__.*_hip_pitch_joint",
                "a__.*_hip_yaw_joint",
            ],
            effort_limit_sim=88,
            velocity_limit_sim=32.0,
            stiffness=100.0,
            damping=2.0,
            armature=0.01,
        ),
        # Leg roll and knee actuators (highest torque)
        "legs_roll_knee": ImplicitActuatorCfg(
            joint_names_expr=[
                "a__.*_hip_roll_joint",
                "a__.*_knee_joint",
            ],
            effort_limit_sim=139,
            velocity_limit_sim=20.0,
            stiffness={
                "a__.*_hip_roll_joint": 100.0,
                "a__.*_knee_joint": 150.0,
            },
            damping={
                "a__.*_hip_roll_joint": 2.0,
                "a__.*_knee_joint": 4.0,
            },
            armature=0.01,
        ),
        # Ankle actuators
        "ankles": ImplicitActuatorCfg(
            joint_names_expr=[
                "a__.*_ankle_pitch_joint",
                "a__.*_ankle_roll_joint",
            ],
            effort_limit_sim=35,
            velocity_limit_sim=30,
            stiffness=40.0,
            damping=2.0,
            armature=0.01,
        ),
        # Waist actuators
        "waist": ImplicitActuatorCfg(
            joint_names_expr=[
                "waist_yaw_joint",
                "waist_roll_joint",
                "torso_joint",
            ],
            effort_limit_sim={
                "waist_yaw_joint": 88,
                "waist_roll_joint": 50,
                "torso_joint": 50,
            },
            velocity_limit_sim=32.0,
            stiffness={
                "waist_yaw_joint": 200.0,
                "waist_roll_joint": 40.0,
                "torso_joint": 40.0,
            },
            damping=5.0,
            armature=0.01,
        ),
        # Head actuator
        "head": ImplicitActuatorCfg(
            joint_names_expr=["head_joint"],
            effort_limit_sim=10,
            velocity_limit_sim=20,
            stiffness=20.0,
            damping=1.0,
            armature=0.01,
        ),
        # Arm actuators (shoulder and elbow)
        # NOTE: Isaac Sim converts "1_" prefix to "a__"
        "arms": ImplicitActuatorCfg(
            joint_names_expr=[
                "a__.*_shoulder_pitch_joint",
                "a__.*_shoulder_roll_joint",
                "a__.*_elbow_joint",
            ],
            effort_limit_sim=25,
            velocity_limit_sim=37,
            stiffness=40.0,
            damping=1.0,
            armature=0.01,
        ),
        # Wrist actuators
        "wrists": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*_wrist_roll_joint",
                ".*_wrist_pitch_joint",
            ],
            effort_limit_sim=5,
            velocity_limit_sim=22,
            stiffness=20.0,
            damping=1.0,
            armature=0.01,
        ),
    },
    # fmt: off
    joint_sdk_names=[
        # Left leg (6 DOF) - NOTE: Isaac Sim converts "0_" to "a__"
        "a__left_hip_pitch_joint",
        "a__left_hip_roll_joint",
        "a__left_hip_yaw_joint",
        "a__left_knee_joint",
        "a__left_ankle_pitch_joint",
        "a__left_ankle_roll_joint",
        # Right leg (6 DOF)
        "a__right_hip_pitch_joint",
        "a__right_hip_roll_joint",
        "a__right_hip_yaw_joint",
        "a__right_knee_joint",
        "a__right_ankle_pitch_joint",
        "a__right_ankle_roll_joint",
        # Waist (3 DOF)
        "waist_yaw_joint",
        "waist_roll_joint",
        "torso_joint",
        # Head (1 DOF)
        "head_joint",
        # Right arm (5 DOF) - NOTE: Isaac Sim converts "1_" to "a__"
        "a__right_shoulder_pitch_joint",
        "a__right_shoulder_roll_joint",
        "a__right_elbow_joint",
        "right_wrist_roll_joint",
        "right_wrist_pitch_joint",
        # Left arm (5 DOF)
        "a__left_shoulder_pitch_joint",
        "a__left_shoulder_roll_joint",
        "a__left_elbow_joint",
        "left_wrist_roll_joint",
        "left_wrist_pitch_joint",
    ],
    # fmt: on
)
