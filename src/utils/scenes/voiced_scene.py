import os
import sys

from functools import partial
from typing import Any, Dict, List

from manim import *


AUDIO_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "audio"
))


class VoicedScene(Scene):
    name = ""

    def __init__(
        self,
        renderer=None,
        camera_class=Camera,
        always_update_mobjects=False,
        random_seed=None,
        skip_animations=False,
        animations: list=[],
        audio_filename: str | None=None,
        audio_offset: float=0
    ):
        super(VoicedScene, self).__init__(
            renderer=renderer,
            camera_class=camera_class,
            always_update_mobjects=always_update_mobjects,
            random_seed=random_seed,
            skip_animations=skip_animations,
        )
        
        self.animation_map = {"wait": self.waiting}
        self.animations: List[Dict[str, Any]] = animations
        self.audio_offset = audio_offset
        if audio_filename is not None:
            if not os.path.isfile(audio_filename):
                audio_filename = os.path.join(AUDIO_DIR, audio_filename)
            if not os.path.isfile(audio_filename):
                raise IOError(f"Voice file {audio_filename} does not exist.")
            self.audio_filename = audio_filename
            self.add_sound(self.audio_filename)
            segment = self.renderer.file_writer.audio_segment
            self.audio_length = segment.duration_seconds
            
    def waiting(self, run_time: float, wait_time: float=0, **kwargs):
        self.wait(run_time)
        
    def setup(self):
        offset = self.audio_offset
        self.animation_funcs = []
        if not hasattr(self, "audio_filename"):
            return
        for i, animation in enumerate(self.animations):
            func = self.animation_map[animation["name"]]
            end = animation.get("audio_mark", self.audio_length)
            duration = end - offset
            offset = end
            partitions = animation.get("partitions", 1)
            wait_time = animation.get("wait_partitions", 1)
            duration = (duration - wait_time) / partitions
            if duration < 0:
                msg = (f"Something went wrong. Got start = {offset}, "
                       f"end = {end}, wait_time = {wait_time}"
                       f" and partitions = {partitions}")
                logger.error(msg)
                sys.exit(1)
            kwargs = animation.get("kwargs", {})
            self.animation_funcs.append(
                partial(func, run_time=duration, wait_time=1, **kwargs)
            )
    
    def construct(self):
        if not hasattr(self, "animation_funcs"):
            self.setup()
        for func in self.animation_funcs:
            func()
