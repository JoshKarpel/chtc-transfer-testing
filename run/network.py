#!/usr/bin/env python3

import itertools
import sys

import htcondor_jobs as jobs

# todo: parse args using argparse

prefix = sys.argv[1]
num_tests_per_facility = int(sys.argv[2])

base_sub = jobs.SubmitDescription(
    # make sure that request_disk is large enough!
    transfer_input_files = 'file.txt',
    request_disk = '11GB',  # todo: automatically figure out request disk from size of input file
    # probably don't need to edit these
    requirements = 'Facility == "$(TargetFacility)"',
    executable = 'network.sh',
    request_memory = '50MB',
    log = '{}/$(Cluster).log'.format(prefix),
    output = '{}/$(Cluster).out'.format(prefix),
    error = '{}/$(Cluster).err'.format(prefix),
    submit_event_notes = '$(TargetFacility)',
)
base_sub['+TargetFacility'] = '"$(TargetFacility)"'

facilities = ['CS_2360', 'CS_3370A', 'CS_B240', 'WID']
facility_cycle = itertools.cycle(facilities)

for test_number, facility in zip(range(num_tests_per_facility * len(facilities)), facility_cycle):
    print(f'Sending test {test_number} to facility {facility}')
    sub = base_sub.copy(
        jobbatchname = str(test_number),
        TargetFacility = facility,
    )

    hnd = jobs.submit(sub, 1)

    print(f'Submitted network test job {hnd}')

    hnd.wait()
