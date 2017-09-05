#!/usr/bin/env python3
import argparse
import os
from os.path import join, exists, abspath
from subprocess import check_call
from glob import glob

def get_t1_images(basedir, subject_label):
    out = glob(join(basedir,"anat", "sub-%s_T1w.nii.gz" % (subject_label))) + \
    glob(join(basedir, "anat", "sub-%s_ses-*_T1w.nii.gz" % (subject_label)))
    return out

def run_mindboggle(image, output_dir):
    #mindboggle123 $IMAGE --id $ID --out $OUT --working $WORKING
    cmd = ["mindboggle123", image,
           "--out", join(output_dir, "derivatives", "mindboggle"),
           "--working", join(output_dir,"scratch"),
           "--cache", join(output_dir,"scratch", "cache")
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
    subjects_to_analyze = [s.split("/")[-1] for s in glob(os.path.join(args.bids_dir, "sub*"))]

# running participant level
print(args)
print(subjects_to_analyze)
if args.analysis_level == "participant":
    print("running")
    # find all T1s and skullstrip them
    for subject_label in subjects_to_analyze:
        print("subject_label is", subject_label)
        t1_images = get_t1_images(args.bids_dir, subject_label)
        print("images are", t1_images)
        [run_mindboggle(t1, args.output_dir) for t1 in t1_images]

