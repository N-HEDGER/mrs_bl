import os
from simple_slurm import Slurm
from .utils import load_pkg_yaml
import pkg_resources
import yaml
import pandas as pd

#os.system('source ~/.bashrc')
#os.system('cd /storage')

base_path = os.path.dirname(os.path.dirname(
    pkg_resources.resource_filename("mrsbl", 'config')))

# Define the path to the config file
pkg_yaml = os.path.join(base_path, 'config', 'config.yml')



class MrsHandler:
    """
    MrsHandler is a class for managing MRS (Magnetic Resonance Spectroscopy) processing jobs, including configuration, script generation, and SLURM job submission.
    Attributes:
        sub (str): Subject identifier.
        ses (str): Session identifier.
        VOI (str): Volume of Interest.
        slurmout_path (str): Path to store SLURM output and error files.
        jobname (str): Name of the SLURM job.
        outfile (str): Path to the SLURM output file.
        errfile (str): Path to the SLURM error file.
        yaml (str): Path to the YAML configuration file.
        y (dict): Loaded YAML configuration.
        slurm (Slurm): SLURM job handler instance.
        populate_cmd (str): Command to populate the script.
        new_filepath (str): Path to the generated MATLAB script.
        message (str): Submission message.
    Methods:
        __init__(sub, ses, VOI, slurmout_path, yaml=pkg_yaml):
            Initializes the MrsHandler instance, loads configuration, and prepares output paths.
        make_script():
            Generates the command and file path for the MATLAB script used in processing.
        make_dirs():
            Creates necessary directories for SLURM output and error files.
        load_yaml():
            Loads the YAML configuration file into the instance.
        internalize_config(y, subdict):
            Sets instance attributes from a sub-dictionary in the YAML configuration.
        make_slurm():
            Prepares the SLURM job configuration and command for submission.
        submit_slurm():
            Submits the SLURM job and prints a submission message.
        make_message():
            Creates a message summarizing the job submission details.
        print_message():
            Prints the job submission message.
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
        self.make_script()

    def make_script(self,):
        self.populate_cmd=self.script_cmd.format(populator=self.populator,sub=self.sub, ses=self.ses, template=self.template_wcard.format(VOI=self.VOI))

        base_dir = os.path.dirname(self.template_wcard.format(VOI=self.VOI))
        new_filename = f"quality_check_setup_MC_{self.sub}_{self.ses}.m"
        self.new_filepath = os.path.join(base_dir, new_filename)
        #os.system(self.populate_cmd)


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
        self.slurm.add_cmd(self.populate_cmd)


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



class MultipleMrsHandlerFromFrame:
    """
    Handles the creation and management of multiple MrsHandler instances from a given DataFrame.

    This class is designed to automate the process of generating and submitting SLURM job scripts
    for multiple configurations specified in a pandas DataFrame.

    Attributes:
        frame (pandas.DataFrame): The DataFrame containing configuration data for each MrsHandler.
        slurmout_path (str): The path where SLURM output files will be stored.
        handlers (list): A list to store the created MrsHandler instances.

    Methods:
        make_mrs_handlers():
            Instantiates a MrsHandler for each row in the DataFrame using the row's data and
            appends it to the handlers list.

        make_slurms():
            Calls the make_slurm() method on each MrsHandler instance to generate SLURM job scripts.

        submit_slurms():
            Calls the submit_slurm() method on each MrsHandler instance to submit the generated
            SLURM job scripts.
    """

    def __init__(self, frame,slurmout_path: str):
        self.frame= frame
        self.slurmout_path = slurmout_path
        self.handlers = []

    def make_mrs_handlers(self):

        for row in range(len(self.frame)):
            handler = MrsHandler(**self.frame.loc[row].to_dict(),slurmout_path=self.slurmout_path)
            self.handlers.append(handler)

    def make_slurms(self):

        for handler in self.handlers:
            handler.make_slurm()

    def submit_slurms(self):

        for handler in self.handlers:
            handler.submit_slurm()

        



