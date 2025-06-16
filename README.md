# MRS_BL

Code for using the racc for performing batch MRS analyses via slurm. An example is shown in notebooks/test.ipynb.
## Project Structure

```
/mrs_bl/
├── config/
│   └── config.yml         # Configuration file for SLURM and MATLAB batch jobs
├── mrsbl/
│   ├── __init__.py
│   ├── mrs.py
│   ├── utils.py
│   ├── OspreySetup.m
│   ├── quality_check_setup_MC.m
│   ├── quality_check_setup_OCC.m
│   ├── QualityCheck.m
│   ├── skeleton.m
│   └── __pycache__/
├── notebooks/
│   ├── README.md
│   └── test.ipynb
└── README.md              # Project overview and documentation
```

- **config/config.yml**: Contains SLURM and MATLAB configuration for batch processing.
- **mrsbl/**: Main codebase with Python modules and MATLAB scripts for MRS analysis.
- **notebooks/**: Example Jupyter notebooks and related documentation.
- **README.md**: This file.

## Usage

1. Edit `config/config.yml` to set SLURM and MATLAB parameters.
2. Use the provided Python and MATLAB scripts in `mrsbl/` for batch MRS analyses.
3. Refer to `notebooks/` for usage examples and testing.

## Requirements

- MATLAB R2023a (module loaded via SLURM)
- Python 3.10+ environmment

## Installation

pip install -e .

## License

See repository for license information.
