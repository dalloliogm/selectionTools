#!/usr/bin/env python
#
# Python Script to perform for running the single process for our pipeline
#
# Murray Cadzow 
# July 2013
# University Of Otago
#
# James Boocock
# July 2013
# University Of Otago
# 

import os
import sys

from optparse import OptionParser
import ConfigParser

import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

def parse_arguments():
    parser = OptionParser()
    parser.add_option('-v','--verbose',action="store_true",dest='verbose',help="Print debug messages")
    parser.add_option('-q','--silent',action="store_false",dest='verbose', help="Run Silently")
    parser.add_option('-i','--vcf',dest='vcf_input',help="VCF input file")
    parser.add_option('-o','--out',dest='output_prefix', help="Output file prefix")
    parser.add_option('-c','--chromosome',dest='chromosome',help="Chromosome")
    parser.add_option('--maf',dest='maf',help='Minor allele-frequency filter') 
    parser.add_option('--hwe',dest='hwe',help="Hardy-Weinberg Equillibrium filter thread")
    parser.add_option('--remove-missing',dest="remove_missing",help="Remove missing genotypes") 
    parser.add_option('--config-file',dest="config_file", help="Config file")
    (options, args) = parser.parse_args()
    if(options.verbose != None):
        if(options.verbose):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.ERROR)
    # Obligatory arguments
    assert options.vcf_input is not None, "No VCF file has been specified as input"
    assert options.chromosome is not None, "No chromosome has been specified to the script"
    assert options.output_prefix is not None, "Output file prefix has not been specified."
    #Optional arguments using sane defaults  
    if(options.hwe is None):
        options.hwe = 0.001
    if(options.maf is None):
        options.maf = 0.05
    if(options.remove_missing is None):
        options.remove_missing = 0.99
    if (options.config_file == None):
        options.config_file = "defaults.cfg"
    logger.debug(options.config_file)
    return options 
     
             

def parse_config(options):
    config = ConfigParser.ConfigParser()
    config.read(options.config_file)
    config_parsed = {}
    logger.debug(config.sections())
    logger.debug(config.get('system','ram_avaliable'))
    for section in config.sections():
        logger.debug(section)
        opts = config.options(section)
        for op in opts:
            try:
                config_parsed[op] = config.get(section,op)
            except:
                logger.info("exception on {0}".format(op))
                config_parsed[op] = None
    return config_parsed

options = parse_arguments()
config = parse_config(options)
logger.debug(config)
