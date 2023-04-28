# ml_jenkins_starter
A Starter Repository for ML Team Experimentation

## Getting Started
1. Branch off of this repo
2. Copy the [Template Job](https://tentacruel.bb.schrodinger.com/jenkins/job/ml_experiment_template/]) naming it what you want.
3. On Jenkins Change the "Branch Specifier" to your branch.

When run the jenkins job it will run `my_experiment.py` with the python environment described in `devtools/requirements.json`

## Dealing with large assets
Try to keep large file assets that need to be read from these jobs in `boltio:/nfs/working/deep_learn/key_store`.
If you need to bring them over to local during a job add a line in `devtools/install.sh` in which you scp them to the correct location.

### Interesting Settings
#### Build Triggers
By default this will run every day unless you remove "Build Periodically".

"Poll SCM" is a good choice if you want automatic builds on every push.

#### Post-build Actions
You can select "Archive Artifacts".
Here you can select outputs of your experiment to save for posterity.
File paths are relative to the git root.

## Picking Hardware
We sadly currently have a heterogeneous computing system. At the time of writing this these are our machines.

| name | memory | cpu | gpu | schrodinger? | other |
|------|--------|-----|-----|--------------|-------|
| jango | 32GB | 16 | 2 | No | |
| boba | 32GB | 8 | 1 | No | |
| kyo | 32GB | 4 | 1 | No | |
| jarjar | 16GB | 4 | 1 | No | |
| obi | 16GB | 4 | 1 | No | | 
| ayush | 16GB | 4 | 0 | No | P1000 not GTX 1080|
| monica | 32GB | 12 | 1 | Yes | | 
| monty | 32GB | 12 | 1 | Yes | |
| tensorflow-build | 32GB | 8 | 0 |  Yes | Quadro M2000 |
| schrodinger2 | 32GB | 8 | 0 | Yes | Quadro P400 | 
| jabba | 16GB | 8 | 0 | No | OSX Machine



