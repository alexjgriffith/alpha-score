// This file is part of peakAnalysis, http://github.com/alexjgriffith/peaks/, 
// and is Copyright (C) University of Ottawa, 2014. It is Licensed under 
// the three-clause BSD License; see doc/LICENSE.txt.
// Contact: griffitaj@gmail.com

// Generate Heights Writen in C
// Alexander Griffith
// June 6
// Removes chrY chrX and chrM

#ifndef _MAIN
#define _MAIN
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

typedef struct peaks{
  int chr;
  int start;
  int end;
  int readcount[200];
}peaks;

int read_file(char * filename,peaks * data);
int file_length(char * filename);
int split_token(char  trim[1024], char del[],  int i);
int merge_length(peaks * data, int length);
int merge(peaks * data,int x,peaks * merge_data,int y);
int countreads(peaks * data, int y, char * filename,int column);
#endif

int main(int argc,char ** argv)
{
  int i,x,y,k;
  x=file_length(argv[1]);
  peaks * data=(peaks *)calloc(x,sizeof(peaks));
  if ( read_file(argv[1],data))
    exit(0);
  y=x-merge_length(data, x);
  peaks * merge_data=(peaks *)calloc(y,sizeof(peaks));
  merge(data,x,merge_data,y);
  //free(data);
  for(i=0;i<argc-2;i++)
    {
      countreads(merge_data,y, argv[i+2],i);
    }
  for(i=0;i<y;i++)
    {
      printf("chr%d\t%d\t%d\t",merge_data[i].chr,merge_data[i].start,merge_data[i].end);
      for(k=0;k<argc-2;k++)
	printf("%d\t",merge_data[i].readcount[k]);
      printf("\n");
    }
  //free(merge_data);
}

int countreads(peaks * data, int y, char * filename,int column)
{
  int i=0,chr,start,end;
  char   buffer[1024];
  FILE * f = fopen(filename,"r");
  char   tck[5];
  strcpy(tck,"\n");
  while(fgets(buffer,1024, f))
    {
      if(i>=y)
	break;
      split_token(buffer,tck,0);
      sscanf(buffer,"chr%d\t%d\t%d" ,&chr,&start,&end);
      if(chr==data[i].chr)
	{
	  if(data[i].start>end)
	    {
	    continue;
	    }
	  else if(data[i].end<start)
	    {
	    i++;
	    continue;
	    }
	  else
	    data[i].readcount[column]++;
	}
      else if(chr>data[i].chr)
	{
	i++;
	continue;
	}
      else if(chr<data[i].chr)
	continue;
    }
  fclose(f);
  return 0;  
}

int read_file(char * filename,peaks * data)
{
  int i=0;
  char   buffer[1024];
  FILE * f = fopen(filename,"r");
  char   tck[5];
  strcpy(tck,"\n");
  while(fgets(buffer,1024, f))
    {
      split_token(buffer,tck,0);
      sscanf(buffer,"chr%d\t%d\t%d" ,&data[i].chr,&data[i].start,&data[i].end);
      i=i+1;
    }
  fclose(f);
  return 0;
}
 
int merge(peaks * data,int x,peaks * merge_data,int y)
{
  int i,n=0;
  int k=0;
  int start=data[0].start;
  for(i=0;i<x-1;i++)
    {
    if(n>y)
      {
        printf("there was an error\t%d\t%d\n",x,y);
	exit(0);
      }
    if(data[i].chr==data[i+1].chr)
      {
        if(data[i].end<data[i+1].start)
	 {
           merge_data[n].start=start;
	   merge_data[n].end=data[i].end;
	   merge_data[n].chr=data[i].chr;
	   start=data[i+1].start;
	   k=0;
	   n++;	
         } 
	else
	  if(k==0)
	    {
              k=1;
	      start=data[i].start;
            }
       }
    else
      {
        merge_data[n].start=start;
        merge_data[n].end=data[i].end;
	merge_data[n].chr=data[i].chr;
	start=data[i+1].start;
	k=0;
	n++;
      }
  }
      merge_data[n].start=start;
      merge_data[n].end=data[x-1].end;
      merge_data[n].chr=data[x-1].chr;
  return 0;
}

int merge_length(peaks * data, int length)
{
  int i;
  int k=0;
  for(i=0;i<length-1;i++)
    if(data[i].chr==data[i+1].chr && data[i].end>=data[i+1].start)
      k++;
  return k;
}

int file_length(char * filename)
{
  int lines=0;
  int ch;
  FILE *f;
  f = fopen(filename,"r");
  while (EOF != (ch=fgetc(f)))
  {
    if (ch=='\n')
        lines++;
    }
  fclose(f);
  return lines;
}

int split_token(char  trim[1024], char del[],  int i)
{
  char *s;
  int j=0;
    s = strtok (trim, del);
    while (s != NULL && j<=i)
  {
    strcpy(trim,s);
    s = strtok (NULL, del);
    j=j+1;
  }
    return 0;
}
