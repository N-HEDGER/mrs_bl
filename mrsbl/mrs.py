import os
from simple_slurm import Slurm
from .utils import load_pkg_yaml
import pkg_resources
import yaml

#os.system('source ~/.bashrc')
#os.system('cd /storage')

base_path = os.path.dirname(os.path.dirname(
    pkg_resources.resource_filename("mrsbl", 'config')))

# Define the path to the config file
pkg_yaml = os.path.join(base_path, 'config', 'config.yml')



class MrsHandler:
    """
    MrsHandler manages the setup and submission of MRS (Magnetic Resonance Spectroscopy) processing jobs via SLURM.
    Attributes:
        sub (str): Subject identifier.
        ses (str): Session identifier.
        VOI (str): Volume of Interest identifier.
        slurmout_path (str): Path to store SLURM output and error files.
        jobname (str): Generated job name for SLURM submission.
        outfile (str): Path to the SLURM output file.
        errfile (str): Path to the SLURM error file.
        yaml (str): Path to the YAML configuration file.
        y (dict): Loaded YAML configuration.
        slurm (Slurm): SLURM job handler instance.
        cmd (str): Command to be executed by SLURM.
        message (str): Submission message for the user.
    Methods:
        __init__(sub, ses, VOI, slurmout_path, yaml=pkg_yaml):
            Initializes the MrsHandler, loads configuration, and prepares output paths.
        make_dirs():
            Creates the directory for SLURM output and error files if it does not exist.
        load_yaml():
            Loads the YAML configuration file into the handler.
        internalize_config(y, subdict):
            Sets attributes on the handler from a sub-dictionary in the YAML config.
        make_slurm():
            Initializes the SLURM handler, sets output/error files, and prepares the command.
        submit_slurm():
            Submits the job to SLURM and prints a submission message.
        make_message():
            Constructs a message about the job submission status.
        print_message():
            Prints the submission message to the console.
    """
    

    def __init__(self,sub,ses,VOI, slurmout_path: str, yaml: str = pkg_yaml):
        self.sub = sub
        self.ses = ses
        self.VOI = VOI
        self.slurmout_path = slurmout_path
        self.jobname = 'MRS_{subject}_{ses}_{VOI}'.format(subject=self.sub, ses=self.ses, VOI=self.VOI)
        self.make_dirs()

        
        self.outfile = os.path.join(self.slurmout_path, '{subject}.out'.format(subject=self.jobname))
        self.errfile = os.path.join(self.slurmout_path, '{subject}.err'.format(subject=self.jobname))

        self.yaml = yaml
        self.load_yaml()
        self.internalize_config(self.y, 'paths')
        self.internalize_config(self.y, 'cmds')


    def make_dirs(self):
  
        os.makedirs(self.slurmout_path, exist_ok=True)


    def load_yaml(self):

        with open(self.yaml, 'r') as f:
            self.y = yaml.safe_load(f)

    def internalize_config(self, y: dict, subdict: str):

        subdict = y[subdict]

        for key in subdict.keys():
            setattr(self, key, subdict[key])

    def make_slurm(self):

        self.slurm = Slurm(**load_pkg_yaml()['slurm'])

        self.slurm._add_one_argument('output', self.outfile)
        self.slurm._add_one_argument('error', self.errfile)
        [self.slurm.add_cmd(cmd) for cmd in self.slurm_pre_commands]


        self.cmd = self.cmd_wcard.format(matlab=self.matlab_path, sub=self.sub,ses=self.ses,voi=self.VOI,script=self.full_script_path)


    def submit_slurm(self):

        self.slurm.sbatch(self.cmd)
        self.make_message()
        self.print_message()

    def make_message(self):
  
        self.message = ("""Job with {jobname} submitted! \n
              Progress updated in {outfile}\n
              Errors will be reported at {errfile}\n""".format(jobname=self.jobname, outfile=self.outfile, errfile=self.errfile))

    def print_message(self):
 
        print(self.message)


from itertools import product

class MultipleMrsHandler:
    """
    Handles the creation and management of multiple MrsHandler instances for different subjects, sessions, and VOIs.

    Attributes:
        subjects (list): List of subject identifiers.
        sessions (list): List of session identifiers.
        VOIs (list): List of VOI (Volume of Interest) identifiers.
        slurmout_path (str): Path to the output directory for SLURM job files.
        handlers (list): List of MrsHandler instances created for each subject/session/VOI combination.

    Methods:
        make_mrs_handlers():
            Creates MrsHandler instances for all combinations of subjects, sessions, and VOIs, and stores them in self.handlers.

        make_slurms():
            Calls the make_slurm() method on each MrsHandler instance to generate SLURM job files.

        submit_slurms():
            Calls the submit_slurm() method on each MrsHandler instance to submit the SLURM jobs.
    """
    def __init__(self, subjects: list, sessions: list, VOIs,slurmout_path: str):
        self.subjects = subjects
        self.sessions = sessions
        self.VOIs = VOIs
        self.slurmout_path = slurmout_path
        self.handlers = []

    def make_mrs_handlers(self):

        for sub, ses, voi in product(self.subjects, self.sessions, self.VOIs):
            handler = MrsHandler(sub=sub, ses=ses, VOI=voi, slurmout_path=self.slurmout_path)
            self.handlers.append(handler)

    def make_slurms(self):

        for handler in self.handlers:
            handler.make_slurm()

    def submit_slurms(self):

        for handler in self.handlers:
            handler.submit_slurm()




        



