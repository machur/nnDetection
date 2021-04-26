"""
Copyright 2020 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import os
from pathlib import Path

from hydra.experimental import initialize_config_module

from nndet.utils.config import compose


if __name__ == '__main__':
    """
    Automatically deletes files generated by seg2det and restores
    the orignal segmentations
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('tasks', type=str, nargs='+',
                        help="Single or multiple task identifiers to process consecutively",
                        )

    args = parser.parse_args()
    tasks = args.tasks
    initialize_config_module(config_module="nndet.conf")

    for task in tasks:
        cfg = compose(task, "config.yaml", overrides=[])
        print(cfg.pretty())

        splitted_dir = Path(cfg["host"]["splitted_4d_output_dir"])
        for postfix in ["Tr", "Ts"]:
            if (p := splitted_dir / f"labels{postfix}").is_dir():
                # delete everything except original files
                for f in p.iterdir():
                    if f.is_file() and not str(f).endswith("_orig.nii.gz"):
                        os.remove(f)

                # rename files
                for f in p.glob("*.nii.gz"):
                    os.rename(f, f.parent / f"{f.name.rsplit('_', 1)[0]}.nii.gz")
            else:
                print(f"{p} is not a dir. Skipping.")
