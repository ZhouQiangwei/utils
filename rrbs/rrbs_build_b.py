#!/usr/bin/env python

import os
import datetime
from optparse import OptionParser, OptionGroup
import sys
import re

def IUPAC ( nuc ) :
    if nuc == 'R' :
        return ('A','G')
    elif nuc == 'Y' :
        return ('C', 'T')
    elif nuc == 'S' :
        return ('G', 'C')
    elif nuc == 'W' :
        return ('A', 'T')
    elif nuc == 'K' :
        return ('G','T')
    elif nuc == 'M' :
        return ('A','C')
    elif nuc == 'B' :
        return ('C', 'G', 'T')
    elif nuc == 'D' :
        return ('A', 'G', 'T')
    elif nuc == 'H' :
        return ('A', 'C', 'T')
    elif nuc == 'V' :
        return ('A', 'C', 'G')
    elif nuc == 'N' :
        return ('A', 'C', 'G', 'T')
    else :
        return (nuc)

def uniq(inlist):
    # order preserving
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques

from itertools import product

def EnumerateIUPAC ( context_lst ) :
    tag_list = []
#    context_lst = [context]
    for one_context in context_lst :
        for m in product(*[ IUPAC(i) for i in list(one_context)]) :
            tag_list.append(''.join(m))
    return uniq(tag_list)

def error(msg):
    print >> sys.stderr, 'ERROR: %s' % msg
    exit(1)

global_stime = datetime.datetime.now()
def elapsed(msg = None):
    print "[%s]" % msg if msg is not None else "+", "Last:" , datetime.datetime.now() - elapsed.stime, '\tTotal:', datetime.datetime.now() - global_stime

    elapsed.stime = datetime.datetime.now()

elapsed.stime = datetime.datetime.now()

def logm(message):
    log_message = "[%s] %s\n" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message)
    print log_message,
    open_log.logfile.write(log_message)

# example: T-CGA

def read_fasta(fasta_file):
    """ Iterates over all sequences in a fasta file. One at a time, without reading the whole file into the main memory.
    """

    try :
        input = (gzip.open if fasta_file.endswith('.gz') else open)(fasta_file)
    except IOError:
        print "[Error] Cannot find fasta file : %s !" % fasta_file
        exit(-1)
    sanitize = re.compile(r'[^ACTGN]')
    sanitize_seq_id = re.compile(r'[^A-Za-z0-9]')

    chrom_seq = []
    chrom_id = None
    seen_ids = set()

    for line in input:
        if line[0] == '>':
            if chrom_id is not None:
                yield chrom_id, ''.join(chrom_seq)

            chrom_id = sanitize_seq_id.sub('_', line.split()[0][1:])

            if chrom_id in seen_ids:
                error('BS Seeker found identical sequence ids (id: %s) in the fasta file: %s. Please, make sure that all sequence ids are unique and contain only alphanumeric characters: A-Za-z0-9_' % (chrom_id, fasta_file))
            seen_ids.add(chrom_id)

            chrom_seq = []

        else:
            chrom_seq.append(sanitize.sub('N', line.strip().upper()))

    yield chrom_id, ''.join(chrom_seq)

    input.close()

def rrbs_build(fasta_file, ref_path, low_bound, up_bound, cut_format="C-CGG"):
    # ref_path is a string that contains the directory where the reference genomes are stored with
    # the input fasta filename appended

    cut_format = cut_format.upper() # Ex. "C-CGG,C-TAG"; MspI&ApekI:"G^CWGC"

    ref_p = lambda filename: os.path.join(ref_path, filename)

    refd = {}
    rrbs_ref = open(ref_p('rrbs.fa'),'w')

    mappable_regions_output_file = open(ref_p("RRBS_mappable_regions.txt"),"w")

    all_L = 0
    all_mappable_length = 0
    all_unmappable_length = 0

    no_mappable_region = 0
    total_chromosomes = 0

#    cut_context = re.sub("-", "", cut_format).split(",")
    cut_context = EnumerateIUPAC(cut_format.replace("-","").split(","))
    print cut_context
    cut_len = [len(i) for i in cut_context]
    cut_len_max = max(cut_len)


    for chrom_id, chrom_seq in read_fasta(fasta_file):
        total_chromosomes += 1
        refd[chrom_id] = len(chrom_seq)

        L = len(chrom_seq)
        XXXX_sites = []
        XXXX_XXXX = []

        #-- collect all "XXXX sites ---------------------------------
        i = 1
        while i <= L - cut_len_max:
            j = 0
            while j < len(cut_len) :
                if chrom_seq[i : i + cut_len[j]] == cut_context[j]:
                    XXXX_sites.append( (i, i + cut_len[j] - 1) ) # add (1st position, last position)
                j += 1
            i += 1

        #-- find "XXXX" pairs that are within the length of fragment ----
        for j in xrange(len(XXXX_sites) - 1):
            DD = (XXXX_sites[j+1][0] - XXXX_sites[j][1]) - 1 # NOT including both XXXX; DD: fragment length
            if low_bound <= DD <= up_bound:
                XXXX_XXXX.append([XXXX_sites[j][0], XXXX_sites[j+1][1]]) # leftmost <--> rightmost
                mappable_seq = chrom_seq[XXXX_sites[j][0] : XXXX_sites[j+1][1] + 1]
                no_mappable_region += 1

                # start_position, end_position, serial, sequence
                mappable_regions_output_file.write("%s\t%d\t%d\t%d\t%s\n"%(chrom_id, no_mappable_region,
                                            XXXX_sites[j][0], XXXX_sites[j+1][1], mappable_seq))
        # storing region information to file

        #-----------------------------------
        # mask the genome
        _map_seq = []
        mappable_length = 0
        unmappable_length = 0
        m = 0
        mark = False
        while m < L: # for every nucleotide in chr
            if len(XXXX_XXXX) > 0:
                pair = XXXX_XXXX[0]
                p1 = pair[0]  # left end of fragment
                p2 = pair[1]  # right end of fragment
                if p1 <= m < p2 + 1 :
                    _map_seq.append(chrom_seq[m])
                    mappable_length+=1
                    mark = True
                else :
                    if not mark:
                        _map_seq.append("-")
                        unmappable_length += 1
                    else: # the last eligible base
                        _ = XXXX_XXXX.pop(0)
                        if len(XXXX_XXXX)>0:
                            pair = XXXX_XXXX[0]
                            p1 = pair[0]
                            p2 = pair[1]
                            if  p1 <= m < p2 + 1:
                                _map_seq.append(chrom_seq[m])
                                mappable_length += 1
                                mark = True
                            else:
                                _map_seq.append("-")
                                unmappable_length += 1
                                mark = False
                        else:
                            _map_seq.append("-")
                            unmappable_length+=1
                            mark = False
            else:
                if not mark:
                    _map_seq.append("-")
                    unmappable_length+=1
                else:
                    _map_seq.append("-")
                    unmappable_length+=1
                    mark = False

            m+=1

        #-----------------------------------

        chrom_seq = ''.join(_map_seq)

        rrbs_ref.write('>%s\n%s\n' % (chrom_id, chrom_seq)) #.replace("C","T")))

        #chrom_seq = reverse_compl_seq(chrom_seq)
        #-----------------------------------
        all_L += L
        all_mappable_length += mappable_length
        all_unmappable_length += unmappable_length

        elapsed('Finished initial pre-processing of ' + chrom_id)


    for outf in [rrbs_ref]:
        outf.close()


    logm("# Total %d chromosome(s) : all (%d) : unmappable (%d) : mappable (%d) : ratio (%1.5f)" %(total_chromosomes,
                                                                                       all_L,
                                                                                       all_unmappable_length,
                                                                                       all_mappable_length,
                                                                                       float(all_mappable_length)/all_L) )
    logm("# eligible fragments : %d" % no_mappable_region )

    mappable_regions_output_file.close()
    elapsed('Storing mappable regions and genome')

    # delete all fasta files
    # delete_files( f +'.fa' for f in to_bowtie)

    elapsed('END')


if __name__ == '__main__':
    reference_genome_path = os.path.join(os.path.split(globals()['__file__'])[0],'reference_genomes')
    parser = OptionParser()
    #
    parser.add_option("-f", "--file", dest="filename", help="Input your reference genome file (fasta)", metavar="FILE")
    parser.add_option("-d", "--db", type="string", dest="dbpath", help="Path to the reference genome library (generated in preprocessing genome) [Default: %default]", metavar="DBPATH", default = reference_genome_path)
    # RRBS options
    rrbs_opts = OptionGroup(parser, "Reduced Representation Bisulfite Sequencing Options",
                                "Use this options with conjuction of -r [--rrbs]")
    rrbs_opts.add_option("-r", "--rrbs", action="store_true", dest="rrbs", help = 'Build index specially for Reduced Representation Bisulfite Sequencing experiments. Genome other than certain fragments will be masked. [Default: %default]', default = False)
    rrbs_opts.add_option("-l", "--low",type= "int", dest="low_bound", help="lower bound of fragment length (excluding recognition sequence such as C-CGG) [Default: %default]", default = 20)
    rrbs_opts.add_option("-u", "--up", type= "int", dest="up_bound", help="upper bound of fragment length (excluding recognition sequence such as C-CGG ends) [Default: %default]", default = 500)
    rrbs_opts.add_option("-c", "--cut-site", type= "string", dest="cut_format", help="Cut sites of restriction enzyme. Ex: MspI(C-CGG), Mael:(C-TAG), double-enzyme MspI&Mael:(C-CGG,C-TAG). [Default: %default]", default = "C-CGG")
    parser.add_option_group(rrbs_opts)
    (options, args) = parser.parse_args()
    #
    # if no options were given by the user, print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)
    #
    rrbs = options.rrbs
    #
    if options.filename is not None :
        fasta_file=os.path.expanduser(options.filename)
    else :
        error("Please specify the genome file (Fasta) using \"-f\"")
    #
    if fasta_file is None:
        error('Fasta file for the reference genome must be supported')

    if not os.path.isfile(fasta_file):
        if os.path.isfile(os.path.join(options.dbpath, fasta_file)):
            # Search for options.dbpath to check if the genome file is stored there.
            fasta_file = os.path.join(options.dbpath, fasta_file)
        else:
            error('%s cannot be found' % fasta_file)

    ref_path = options.dbpath
    #
    if os.path.exists(ref_path):
        if not os.path.isdir(ref_path):
            error("%s must be a directory. Please, delete it or change the -d option." % ref_path)
        #
    else:
        os.mkdir(ref_path)

    rrbs_build(fasta_file, ref_path, options.low_bound, options.up_bound, options.cut_format)
    #
