// This file is part of peakAnalysis, http://github.com/alexjgriffith/peaks/, 
// and is Copyright (C) University of Ottawa, 2014. It is Licensed under 
// the three-clause BSD License; see doc/LICENSE.txt.
// Contact: griffitaj@gmail.com

#ifndef GFA_H_
#define GFA_H_
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include "generate_fasta_index.h"

int generateFasta(char sourceFasta[100],char indexFasta[100],char outputFasta[100],char bedFile[100], int width);

#endif

int main(int argc,char ** argv)
{
  char bedFile[100];
  char outputFasta[100];
  char sourceFasta[100];
  char indexFasta[100];
  int width= 300;
  int ch;
  FILE * file;

  static struct option long_options[] ={
      {"input-bed", required_argument, NULL, 'b'},
      {"output-fasta", required_argument, NULL, 'o'},
      {"source-fasta",required_argument,NULL,'s'},
      {"index_file",required_argument,NULL,'i'},
      {"width",optional_argument,NULL,'w'},
      {NULL, 0, NULL, 0}};

  while ((ch = getopt_long(argc, argv, "b:o:s:i:w:", long_options, NULL)) != -1){
    switch (ch){
    case 'b':
      strcpy(bedFile,optarg);
      break;
    case 'o':
      strcpy(outputFasta,optarg);
      break;
    case 's':
      strcpy(sourceFasta,optarg);
      break;
    case 'i':
      strcpy(indexFasta,optarg);
      break;
    case 'w':
      sscanf(optarg,"%d",&width);
      break;}}
  
  file=fopen(indexFasta,"r");
  if(file==NULL ){
    fprintf(stderr,"Could not find the index file: %s\ngenerating %s now.\n",indexFasta,indexFasta);
    generateIndex(sourceFasta,indexFasta);
  }
  else
    fclose(file);
  generateFasta(sourceFasta,indexFasta,outputFasta,bedFile,width);
}

int generateFasta(char sourceFasta[100],char indexFasta[100],char outputFasta[100],char bedFile[100], int width)
{
  FILE * file;
  FILE * fasta;
  FILE * outputFile;
  char buffer[256];
  int k;
  int i;
  int chroLength;
  char caps[100][100];
  unsigned long temp[100];
  unsigned long rats,line;
  char chro[100];
  unsigned long summit,start;
  char output[2000];
  file=fopen(indexFasta,"r"); //
  fasta=fopen(sourceFasta,"r"); //
  k=0;
  while (fgets(buffer,100,file))
    {
      sscanf(buffer, "%s\t%lu",caps[k],&temp[k]);
      k++;
    }
  fclose(file);
  chroLength=k;
  outputFile=fopen(outputFasta,"w"); //
  file=fopen(bedFile,"r"); //
  while(fgets(buffer,256,file))
    {
      sscanf(buffer, "%s\t%lu",chro,&summit);
      start=summit;
      for (i=0;i<chroLength;i++)
	{
	  if (!strcmp(caps[i],chro))
	    {
	      line=start/50;
	      rats=start+temp[i]+line;
	      fseek(fasta,rats,SEEK_SET);
	      fprintf(outputFile,">%s:%lu-%lu\n",chro,start,start+width);
	      for(k=0;k<width;k++)
		{
		  fread(buffer,1,1,fasta);
		  if (buffer[0]=='\n')
		    k--;
		  else     
		    fprintf(outputFile,"%c",buffer[0]);
		}
	      fprintf(outputFile,"\n");
	    }
	}
    }
  fclose(outputFile);
  fclose(file);
  fclose(fasta);
  return 0;
}
