#include <iostream>
#include <string>
#include <stdio.h>
#include <deque>
#include <malloc.h>
#include <string.h>
#include <stdlib.h>
#include <algorithm>

int chromname_len=400;
const int BUFSIZE=600;
FILE* File_Open(const char* File_Name,const char* Mode);
int count_number(char* chr_id, std::string seq, char* redss, char* revcomp);
inline char ConvToUpperA(char chConv)
{

    return (chConv >= 'a' && chConv <= 'z')? (chConv & 0xdf) : chConv;

}
int main(int argc, char* argv[]){
        fprintf(stderr, "\nmg");
        const char* Help_String="\nCommand Format : Key [options] genome.fa\n"
                "\nUsage:\n"
                "\t-S         default: [-S CG] for Count.\n"
		"\t-R         detect complement, default yes, for example: CG->GC\n"
                "\t-h|--help";


	//restriction enzyme digestion sites
	char* redss = new char[100];
	strcpy(redss, "CG");
	char* genome_file = new char[100];
	char Char_To_R[255];
        Char_To_R['A']='T';Char_To_R['a']='t';
        Char_To_R['C']='G';Char_To_R['c']='g';
        Char_To_R['G']='C';Char_To_R['g']='c';
        Char_To_R['T']='A';Char_To_R['t']='a';
        Char_To_R['N']='N';Char_To_R['n']='n';

        if(argc<2)
        {
                printf("%s \n",Help_String);
                exit(0);
        }
        for(int i=1;i<argc;i++)
        {
		if(!strcmp(argv[i], "-S")){
			strcpy(redss, argv[++i]);
		}
	}
	strcpy(genome_file, argv[argc-1]);
	
	//PROCESS redss
	int i=0;bool movp=false;
	for(i=0;i<strlen(redss);i++){
		if(redss[i]=='-'){
			if(i+1<strlen(redss))
				redss[i]=redss[i+1];
			else redss[i]=0;
			movp=true;
		}else if(movp){
			if(i+1<strlen(redss))
                        	redss[i]=redss[i+1];
			else redss[i]=0;
		}
	}
	
	char* revcomp = new char[100];
	for(i=0; i<strlen(redss); i++){
		revcomp[i] = Char_To_R[redss[i]];
		//revcomp[i] = Char_To_R[redss[strlen(redss)-i-1]];
	}
	revcomp[strlen(redss)]='\0';
	fprintf(stderr, "\nDetect case sites: %s, %s\n", redss, revcomp);

	std::string seq="";
	//read genome file and process with reds
	FILE* INFILE=File_Open(genome_file,"r");

	char* Buffer=new char[BUFSIZE];
	Buffer[BUFSIZE]=0;
	char* chr_id=new char[chromname_len];
	chr_id[chromname_len]=0;
	unsigned int total_count=0;

	while (fgets(Buffer,BUFSIZE,INFILE))
	{
		if(Buffer[strlen(Buffer)-1]=='\n')
			Buffer[strlen(Buffer)-1]='\0';
		if (Buffer[0] != '>') 
		{
			seq+=Buffer;
		}
		else if (Buffer[0] == '>') 
		{
			if(seq!=""){
				fprintf(stderr, "\nProcess chromosome: %s", chr_id);
				total_count += count_number(chr_id, seq, redss, revcomp);
			}
			strcpy(chr_id, Buffer);
			seq="";
		}
		
	}
	//the last chrom
	fprintf(stderr, "\nProcess chromosome: %s", chr_id);
	total_count += count_number(chr_id, seq, redss, revcomp);
	fprintf(stderr, "\nTotal Detected: %d %s site in genome", total_count, redss);
	fprintf(stderr, "\nDone!\n");
	fclose(INFILE);


	delete []Buffer;
	delete []chr_id;
	delete []genome_file;
	delete []redss;
	delete []revcomp;
}

FILE* File_Open(const char* File_Name,const char* Mode)
{
	FILE* Handle;
	Handle=fopen64(File_Name,Mode);
	if (Handle==NULL)
	{
		fprintf(stderr, "File %s Cannot be opened ....",File_Name);
		exit(1);
	}
	else return Handle;
}

int count_number(char* chr_id, std::string seq, char* redss, char* revcomp){
	//transform(seq.begin(), seq.end(), seq.begin(), ::toupper);
	unsigned int cLen = seq.length();
        for (size_t i = 0; i<cLen; ++i)
        {
	        seq[i] = ConvToUpperA(seq[i]);
        }

	int redlen=strlen(redss);
    //-- get all red sites ---------------------------------
	fprintf(stderr, "\nDectet case sites in the chromosome.");

	std::deque<std::size_t> reds_loci;
	reds_loci.push_back(0);
	int num=0;
	std::size_t found = seq.find(redss, 0);
	while (found!=std::string::npos){
		num++;
		reds_loci.push_back(found);
		found = seq.find(redss, found+1);
	}
	//reds_loci.push_back(cLen-redlen);
	int casenumber=reds_loci.size();
	fprintf(stderr, "\nProcess the genome with case sites number: %d, genomeLen: %d", reds_loci.size(), cLen);

	reds_loci.clear();
	num=0;
        if(strlen(revcomp)>0){
		std::size_t found = seq.find(revcomp, 0);
		while (found!=std::string::npos){
        	        num++;
	                reds_loci.push_back(found);
                	found = seq.find(revcomp, found+1);
        	}
        }
	fprintf(stderr, "\nProcess the genome with revsere completment case sites number: %d, genomeLen: %d", reds_loci.size(), cLen);
	return reds_loci.size() + casenumber;
}

