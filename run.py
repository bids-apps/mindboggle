#!/usr/bin/env python3
import argparse
import os
from os.path import join, exists, abspath
from subprocess import check_call
from glob import glob

def bidser(basedir, subject_label):
    out = glob(join(basedir, "sub-%s_T1w" % (subject_label))) + \
    glob(join(basedir, "sub-%s_ses-*_T1w" % (subject_label)))
    return out


def get_ants_node():
    from nipype.interfaces.ants.segmentation import CorticalThickness
    import nipype.pipeline.engine as pe

    antsCT = pe.MapNode(CorticalThickness(quick_registration=True,
                                          segmentation_iterations=1),
                        name="antsCT", iterfield=["anatomical_image"])
    antsCT.inputs.dimension = 3
    #antsCT.inputs.anatomical_image = self.inputs.t1_files
    antsCT.inputs.brain_probability_mask = "OASIS-30_Atropos_template/T_template0_BrainCerebellumProbabilityMask.nii.gz"
    antsCT.inputs.t1_registration_template = "OASIS-30_Atropos_template/T_template0_BrainCerebellum.nii.gz"
    antsCT.inputs.segmentation_priors = ["OASIS-30_Atropos_template/Priors2/priors%d.nii.gz"%i for i in range(1,7)]
    antsCT.inputs.brain_template = "OASIS-30_Atropos_template/T_template0.nii.gz"
    antsCT.inputs.extraction_registration_mask = "OASIS-30_Atropos_template/T_template0_BrainCerebellumExtractionMask.nii.gz"
    return antsCT


def run_ants_cortical_thickness(subid, nii_files, output_dir, merge = False):
    import nipype.interfaces.io as nio
    import nipype.pipeline.engine as pe

    wf = pe.Workflow(name="antsCT_%s" % subid)
    wf.base_dir = join(output_dir,"scratch")

    antsCT = get_ants_node()

    if merge:
        #do some registering and averaging here.
        raise Exception("Not Implemented Yet")
    else:
        antsCT.inputs.anatomical_image = nii_files

    sinker = pe.Node(nio.DataSink(), name="sinker")
    sinker.inputs.base_directory = join(output_dir, "derivatives")
    for output in antsCT._outputs().get().keys():
        wf.connect(antsCT, output, sinker, "antsCT.@%s" % output)

    def subs(t1_files):
        #fix the mapnode crap here
        pass

    sinker.inputs.container = subid

    wf.run()


def run_mindboggle(fs_path, output_dir, n_cpus=1):

    cmd = ["mindboggle", fs_path,
           #"--ants", antsfile,
           "--out", join(output_dir, "derivatives", "mindboggle"),
           "--working", join(output_dir,"scratch"),
           "--cache", join(output_dir,"scratch", "cache"),
           "--cpus", str(n_cpus),"--no_surfaces",
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
parser.add_argument("--n_cpus", help="number of cpus", default="1")

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
            fs_folder = join(args.bids_dir, "derivatives", "freesurfer", "sub-"+subject_label)
            print("fs folder is", fs_folder)
            run_mindboggle(fs_folder, args.output_dir, args.n_cpus)

