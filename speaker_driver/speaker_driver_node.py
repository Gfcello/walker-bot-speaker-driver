#!/usr/bin/env python3

import os
import random
import subprocess

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class AudioPlayerNode(Node):
    def __init__(self):
        super().__init__('audio_player')

        self.subscription = self.create_subscription(
            String,
            '/play_audio',
            self.play_audio_callback,
            10
        )

        # Base directory where audio folders are mounted
        self.audio_base_path = os.environ.get(
            'AUDIO_BASE_PATH',
            '/audio'
        )

        # Command used to play audio
        # aplay: WAV only
        # ffplay: supports many formats
        self.player_cmd = os.environ.get(
            'AUDIO_PLAYER',
            'ffplay'
        )

        self.get_logger().info('Audio Player Node started')

    def play_audio_callback(self, msg: String):
        folder_name = msg.data.strip()

        if not folder_name:
            self.get_logger().warn('Received empty folder name')
            return

        folder_path = os.path.join(self.audio_base_path, folder_name)

        if not os.path.isdir(folder_path):
            self.get_logger().error(f'Folder not found: {folder_path}')
            return

        audio_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.wav', '.mp3', '.ogg'))
        ]

        if not audio_files:
            self.get_logger().error(f'No audio files in {folder_path}')
            return

        selected_file = random.choice(audio_files)
        file_path = os.path.join(folder_path, selected_file)

        self.get_logger().info(f'Playing: {file_path}')

        try:
            subprocess.Popen(
            [
                self.player_cmd,
                "-nodisp",
                "-autoexit",
                "-loglevel", "quiet",
                file_path
            ]
            )
        except Exception as e:
            self.get_logger().error(f'Failed to play audio: {e}')


def main():
    rclpy.init()
    node = AudioPlayerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
