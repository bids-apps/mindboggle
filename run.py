#!/usr/bin/env python3
import argparse
import os
from os.path import join, exists, abspath
from subprocess import Popen, PIPE
import subprocess
from glob import glob

def run(command, env={}):
    process = Popen(command, stdout=PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
    while True:
        line = process.stdout.readline()
        line = str(line, 'utf-8')[:-1]
        print(line)
        if line == '' and process.poll() != None:
            break

def check_for_freesurfer(subject, bids_dir, output_dir):
    cmd = ["docker", "run", "-ti", "bids/freesurfer",
           "--participant_label", subject, bids_dir, output_dir, "participant"]
    if exists(join(output_dir, subject_label, "scripts", "recon-all.done")):
        return join(output_dir, subject_label)
    else:
        run(cmd)
        return join(output_dir, subject_label)

def check_for_ants(t1_file, output_dir):
    from nipype.interfaces.ants.segmentation import CorticalThickness

    antsCT = CorticalThickness()
    antsCT.inputs.dimension = 3
    antsCT.inputs.anatomical_image = t1_file
    antsCT.inputs.brain_probability_mask = abspath("OASIS-30_Atropos_ProbabilityMask.nii.gz ")
    antsCT.inputs.t1_registration_template = abspath("OASIS-30_Atropos_template.nii.gz")
    antsCT.inputs.segmentation_priors = [abspath("OASIS-30_Atropos_priors%d.nii.gz" % i) for i in range(1,5)]
    antsCT.inputs.extraction_registration_mask = abspath("OASIS-30_Atropos_ExtractionMask.nii.gz")
    antsCT.inputs.



def run_mindboggle(fsid, antsfile, output_dir):

    cmd = ["mindboggle", fsid,
           "--ants", antsfile, "--out", output_dir
           ]
    run(cmd)
    return


parser = argparse.ArgumentParser(description='Example BIDS App entrypoint script.')
parser.add_argument('bids_dir', help='The directory with the input dataset '
                                     'formatted according to the BIDS standard.')
parser.add_argument('output_dir', help='The directory where the output files '
                                       'should be stored. If you are running group level analysis '
                                       'this folder should be prepopulated with the results of the'
                                       'participant level analysis.')
parser.add_argument('analysis_level', help='Level of the analysis that will be performed. '
                                           'Multiple participant level analyses can be run independently '
                                           '(in parallel) using the same output_dir.',
                    choices=['participant'])
parser.add_argument('--participant_label', help='The label(s) of the participant(s) that should be analyzed. The label '
                                                'corresponds to sub-<participant_label> from the BIDS spec '
                                                '(so it does not include "sub-"). If this parameter is not '
                                                'provided all subjects should be analyzed. Multiple '
                                                'participants can be specified with a space separated list.',
                    nargs="+")

args = parser.parse_args()

subjects_to_analyze = []
# only for a subset of subjects
if args.participant_label:
    subjects_to_analyze = args.participant_label
# for all subjects
else:
    subject_dirs = glob(os.path.join(args.bids_dir, "sub-*"))
    subjects_to_analyze = [subject_dir.split("-")[-1] for subject_dir in subject_dirs]

# running participant level
if args.analysis_level == "participant":

    # find all T1s and skullstrip them
    for subject_label in subjects_to_analyze:
        for T1_file in glob(os.path.join(args.bids_dir, "sub-%s" % subject_label,
                                         "anat", "*_T1w.nii*")) + glob(os.path.join(args.bids_dir, "sub-%s" %
                subject_label, "ses-*", "anat", "*_T1w.nii*")):
            fsid_path = check_for_freesurfer(subject_label, args.bids_dir, args.output_dir)
            antsid = check_for_ants(T1_file, args.output_dir)
            run_mindboggle(fsid_path, antsid, args.output_dir)

