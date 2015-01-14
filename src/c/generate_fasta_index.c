// This file is part of peakAnalysis, http://github.com/alexjgriffith/peaks/, 
// and is Copyright (C) University of Ottawa, 2014. It is Licensed under 
// the three-clause BSD License; see doc/LICENSE.txt.
// Contact: griffitaj@gmail.com
#include "generate_fasta_index.h"

int generateIndex(char sourceFasta[100],char indexFasta[100])
{
  FILE * file;
  FILE * write;
  int i;
  char buffer[10];
  char chro[10];
  int k;
  file=fopen(sourceFasta,"r");
  write=fopen(indexFasta,"w");
  while (fread(buffer,1,1,file))
    {
      if (buffer[0]=='>')
	{
	  for(k=0;k<10;k++)
	    chro[k]='\0';
	  k=0;  
	    while(fread(buffer,1,1,file))
	      {
		if(buffer[0]=='\n' || k==9)
		  break;
		chro[k]=buffer[0];
		k++;
	      }
	    fprintf(write,"%s\t%lu\n",chro,ftell(file));
	}
    }
  fclose(write);
  fclose(file);
  return 0;
}
