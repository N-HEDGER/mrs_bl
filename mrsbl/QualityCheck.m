
% Carolyn McNabb
% Septeer 2021

% GBGABA BRAIN DATA ANALYSIS
% QualityCheck.m will run the Osprey preprocessing pipeline in MATLAB.
% It will use the data specified in the quality_check_setup_MC.m or
% quality_check_setup_OCC.m functions for individual preprocessing,
% or from group_analybsis_setup_MC.m or group_analysis_setup_OCC.m for group preprocessing.

% Define voxel of interest for quality check:
% (options are MC and OCC).
% NOTE: this is only required for individual quality checks.
%VOI = ['OCC']; 


 %cd('/')

sub = evalin('base', 'sub');
ses = evalin('base', 'ses');
VOI = evalin('base', 'VOI');

disp(sub)
disp(ses)

disp(sprintf('quality_check_setup_%s_%s_%s.m', VOI,sub,ses))

% add path to SPM12
addpath('/home/users/yg916972/Software/spm12')

% add folders and subfolders for Osprey to path
addpath(genpath('/home/users/yg916972/Software/osprey-Osprey2.10'))

% add path to data
addpath(genpath('/storage/research/cinn/2020/gbgaba/GBGABA_BIDS'))

% change directory to the folder containing Osprey jobfiles
cd('/home/users/yg916972/Software/mrs_bl/mrsbl')

% Set RNG seed
rng('default');
rng(42, 'twister');


% Run the pre-processing:
%%% (comment out depending on individual or group pre-processing)
%%% for individual pre-processing, run:d
filename=sprintf('quality_check_setup_%s_%s_%s.m', VOI,sub,ses)
filename=strrep(filename, '-', '_');
disp(filename)

[MRSCont] = RunOspreyJob(filename);
%%% for group MC pre-processing, run:
%%% [MRSCont] = OspreyJob(sprintf('group_analysis_setup_MC.m'));
%%% or for OCC, run:
 %[MRSCont] = OspreyJob(sprintf('group_analysis_setup_OCC.m'));

 % [MRSCont] = OspreyJob(sprintf('MC_group_test.m'));

% Run the Osprey Workflow as follows:

% Load the raw metabolite and water reference data:
 %[MRSCont] = OspreyLoad(MRSCont);

% Translate the raw, un-aligned, un-average data into spectra for modeling:
% [MRSCont] = OspreyProcess(MRSCont);

% Create a binary voxel mask and coregister this to structural image, in
% order to reproduce original voxel placement:
 %[MRSCont] = OspreyCoreg(MRSCont);

% Segment structural image into gray matter (GM), white matter (WM), and
% cerebrospinal fluid (CSF). Overlay coregistered voxel mask with GM, WM 
% and CSF probability maps and calculate fractional tissue volumes for 
% GM, WM, and CSF:
 %[MRSCont] = OspreySeg(MRSCont);

% Model the processed spectra:
%[MRSCont] = OspreyFit(MRSCont);

% Calculate quantitative outputs:
 %[MRSCont] = OspreyQuantify(MRSCont);

% Provide summary visualisations:
 %[MRSCont] = OspreyOverview(MRSCont); 

