#!/usr/bin/env python
import os
import sys, getopt


##
threads = "1"
name = "RUN"
nodes = "1"

isqsub = 1 ##0

def usage():
    print "./runprogram [mode] [paramaters]"
    print "mode:  qsub, trim, sra2fq, fqc, downloadsrp, asperasrp, bwameth, bismark_1, bismark_2"
    print "\nqsub mode:"
    print "    run.qsub.py qsub \"CMD\" -N programName -p threads [-n]"
    print "    -n number of nodes, default:1"
    print "trim mode:"
    print "    Here is a trim sample."
    print "downloadsrp:"
    print "    Usage: script downliadsra {srp/drp}_head_3 srp/drp sra/drr"
    print "asperasrp:"
    print "    Usage: script asperasrp {srp/drp}_head_3 srp/drp sra/drr"
    print "bwameth:"
    print "    Here is a bwameth sample. bismark is same."
    print "sra2fq:"
    print "    script sra2fq [--split-3] [-X ..] [...] SRA"

if len(sys.argv) < 2:
    usage()
    sys.exit()

#command = " ".join(sys.argv[2:])
mode = sys.argv[1]
if name == "RUN":
    name = mode
command = sys.argv[2]

def detect_paramaters():
    try:
        opts, args = getopt.getopt(sys.argv[3:], "N:n:p:h", ["version", "file="])
    except:
        print "Please make sure the paramaters is correct."
    global threads, name, nodes
    for op, value in opts:
    #    print op, value
        if op == "-p":
            threads = value
        elif op == "-N":
            name = value
        elif op == "-n":
            nodes = value
        elif op == "-h":
            usage()
            sys.exit()

if mode == "qsub":
    detect_paramaters()

def runprogram(cmd):
    print cmd
    error = os.system(cmd)
    if error != 0:
        print "program %s error!"%cmd
        sys.exit()
    else:
        print "job runing."

def qsub(command, nodes, threads, name):
    cmd = "echo '{command}' | qsub -l nodes={nodes}:ppn={threads} -N {name} -d ./ -e ./"
    cmd = cmd.format(**locals())
    runprogram(cmd)
##for i in range(1, len(sys.argv)):
##  print sys.argv[i]
def trim():
    print "java -jar ~/software/trimmomatic-0.35/trimmomatic-0.35.jar PE -phred33 SRR3503136_1.fastq SRR3503136_2.fastq SRR3503136_1.paired.fq unpaired_1.fq SRR3503136_2.paired.fq unpaired_2.fq ILLUMINACLIP:/home/qwzhou/software/trimmomatic-0.35/adapters/Illumina_Universal_Adapter.fa:1:15:7 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:125"
    print "java -jar trimmomatic-0.35.jar PE -phred33 input_forward.fq.gz input_reverse.fq.gz output_forward_paired.fq.gz output_forward_unpaired.fq.gz output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"
    print "java -jar trimmomatic-0.35.jar SE -phred33 input.fq.gz output.fq.gz ILLUMINACLIP:TruSeq3-SE:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"

def downloadsrp(SRP3, SRP, SRA):
    cmd = "wget ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByStudy/sra/SRP/{SRP3}/{SRP}/{SRA}/{SRA}.sra"
    cmd = cmd.format(**locals())
    if isqsub == 1:
        qsub(cmd, nodes, threads, name)
    else:
        runprogram(cmd)

def bwameth():
    print "python ~/software/bwa-meth/bwameth.py --reference /public/home/qwzhou/practice/Genome/hg19/bwa-meth-index/hg19.fa Read1.fq -t 6 > bwameth_1.sam"
    #print "~/scripts/run.qsub.py qsub \"python ~/software/bwa-meth/bwameth.py --reference /public/home/qwzhou/practice/Genome/hg19/bwa-meth-index/hg19.fa Read1.fq -t 6 > bwameth_1.sam\" -N align_1 -p 6"

def batmeth2():
    print ""

def bismark_bowtie1():
    print "bismark ~/practice/Genome/oryza/bismark_bowtie1/ Read2.fq --bowtie1 --multicore 6 -non_directional"
    print "bismark ~/practice/Genome/oryza/bismark_bowtie1/ Read1.fq --bowtie1 --multicore 6"

def bismark_bowtie2():
    print "bismark ~/practice/Genome/oryza/bismark_bowtie2/ Read1.fq --bowtie2 -p 6 --prefix bowtie2 --sam"
    print "bismark ~/practice/Genome/oryza/bismark_bowtie2/ Read2.fq --bowtie2 -p 6 --prefix bowtie2 --sam -non_directional"

def asperasrp(SRP3, SRP, SRA):
    cmd = "ascp -QT -l 100m -i ~/.aspera/connect/etc/asperaweb_id_dsa.openssh anonftp@ftp-private.ncbi.nlm.nih.gov:sra/sra-instant/reads/ByStudy/sra/SRP/{SRP3}/{SRP}/{SRA}/{SRA}.sra ."
    cmd = cmd.format(**locals())
    runprogram(cmd)

def sra2fq():
    cmd = "fastq-dump "
    cmd += " ".join(sys.argv[2:])
    if isqsub == 1:
        qsub(cmd, nodes, threads, name)
    else:
        runprogram(cmd)

def fqc():
    cmd = "fastqc "
    cmd += " ".join(sys.argv[2:])
    if isqsub == 1:
        qsub(cmd, nodes, threads, name)
    else:
        runprogram(cmd)

if mode == "qsub":
    qsub(command, nodes, threads, name)
elif mode == "trim":
    trim()
elif mode == "bwameth":
    bwameth()
elif mode == "bismark-1":
    bismark_bowtie1()
elif mode == "bismark-2":
    bismark_bowtie2()
elif mode == "downloadsrp":
    if(len(sys.argv)>=5):
        srp3=sys.argv[2]
        srp=sys.argv[3]
        sra=sys.argv[4]
        downloadsrp(srp3,srp,sra)
    else:
        print "Usage: script downliadsra {srp/drp}_head_3 srp/drp sra/drr"
elif mode == "asperasrp":
    if(len(sys.argv)>=5):
        srp3=sys.argv[2]
        srp=sys.argv[3]
        sra=sys.argv[4]
        asperasrp(srp3,srp,sra)
    else:
        print "Usage: script asperasra {srp/drp}_head_3 srp/drp sra/drr"
elif mode == "sra2fq":
    sra2fq()
elif mode == "fqc":
    fqc()