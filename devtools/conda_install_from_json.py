import sys
import json
import delegator
import datetime
import os

buffer = []


def read_requirements(fnames):
    keys = ["channels", "packages", "cpu_packages", "gpu_packages"]
    with open(fnames[0]) as fin:
        d = json.load(fin)
    for fname in fnames[1:]:
        with open(fname) as fin:
            d2 = json.load(fin)
            for key in keys:
                d[key].extend(d2[key])
    return d


def add_platform_specific_packages(cmd, requirements):
    if 'CPU_ONLY' in os.environ and os.environ['CPU_ONLY'] == '1':
        for package in requirements['cpu_packages']:
            cmd = '%s "%s"' % (cmd, package)
        return cmd
    for package in requirements['gpu_packages']:
        cmd = '%s "%s"' % (cmd, package)
    return cmd


def add_wheels(requirements):
    wheels = requirements.get('wheels', [])
    if 'CPU_ONLY' in os.environ and os.environ['CPU_ONLY'] == '1':
        wheels.extend(requirements.get('cpu_wheels', []))
    else:
        wheels.extend(requirements.get('gpu_wheels', []))
    for whl in wheels:
        cmd = "pip install %s" % whl
        print(cmd)
        buffer.append(cmd)


def run_install():
    with open("devtools/install_env.sh", 'w') as fout:
        fout.write("#!/bin/bash\n")
        fout.write(f"# {datetime.datetime.now()}\n")
        for line in buffer:
            fout.write(f"{line}\n")

    c = delegator.run("/bin/bash devtools/install_env.sh")
    print(c.out)
    print(c.err)
    print(c.return_code)
    return c


def main(conda_binary, fnames):
    requirements = read_requirements(fnames)
    cmd = f"{conda_binary} install -y -q "
    for channel in requirements['channels']:
        cmd = "%s -c %s" % (cmd, channel)
    for package in requirements['packages']:
        cmd = '%s "%s"' % (cmd, package)
    cmd = add_platform_specific_packages(cmd, requirements)
    print("Conda Command")
    print("%s" % cmd)
    buffer.append(cmd)
    add_wheels(requirements)
    return run_install()


if __name__ == "__main__":
    """
    python conda_install_from_json.py {optional_conda_binary} {requirements1.json}...

    This script creates devtools/install_env.sh a single script which will call all the
    bash commands to create a conda environment from multiple requirements.json files
    """
    if sys.argv[1].endswith('.json'):
        c = main('conda', sys.argv[1:])
        sys.exit(c.return_code)
    c = main(sys.argv[1], sys.argv[2:])
    sys.exit(c.return_code)
