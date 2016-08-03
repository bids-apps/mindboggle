#!/usr/bin/env python3
import argparse
import os
from os.path import join, exists, abspath
from subprocess import check_call
import subprocess
from glob import glob

def bidser(basedir, subject_label):
    out = glob(join(basedir, "sub-%s_T1w" % (subject_label))) + \
    glob(join(basedir, "sub-%s_ses-*_T1w" % (subject_label)))
    return out




def run_mindboggle(fs_path, antsfile, output_dir):

    cmd = ["mindboggle", fs_path,
           "--ants", antsfile, "--out", output_dir
           ]
    check_call(cmd)
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
print(args)
print(subjects_to_analyze)
if args.analysis_level == "participant":
    print("running")
    # find all T1s and skullstrip them
    for subject_label in subjects_to_analyze:
            print("subject_label is", subject_label)
            fs_folders = bidser(join(args.output_dir, "derivatives", "freesurfer"), subject_label)
            ants_folders = [join(q, "antsBrainSegmentation.nii.gz")
                            for q in bidser(join(args.output_dir, "derivatives", "ants"), subject_label)]
            if not len(fs_folders) == len(ants_folders):
                raise Exception("run ANTS and Freesurfer for all T1w files of %s" % subject_label)
            for idx, fsid in enumerate(fs_folders):
                run_mindboggle(fsid, ants_folders[idx], args.output_dir)

