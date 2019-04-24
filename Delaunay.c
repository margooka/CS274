# include <stdio.h>

//------------------------------------------------

//https://stackoverflow.com/questions/24290273/check-if-input-file-is-a-valid-file-in-c
int file_isreg(const char *path) {
    struct stat st;
    if (stat(path, &st) < 0)
        return -1;
    return S_ISREG(st.st_mode);
} 
//https://stackoverflow.com/questions/12275667/check-if-a-file-is-a-specific-type-in-c
int endsWith (char *str, char *end) {
    size_t slen = strlen (str);
    size_t elen = strlen (end);
    if (slen < elen)
        return 0;
    return (strcmp (&(str[slen-elen]), end) == 0);
}

//--------------------------------------------------

int main(int argc, char * argv[])
{
	if (argc != 1)
	{
		printf("enter a single filename argument");
		return 0;
	} 
	if (file_isreg(argv)==1 && endsWith(argv, ".node")) {
		//proceed with triangulation

		//https://stackoverflow.com/questions/18421310/reading-a-file-line-by-line-and-splitting-the-string-into-tokens-in-c
		FILE* fp;
    	char  line[255];
    	fp = fopen(argv , "r");

		char * firstline = strtok(fgets(line, sizeof(line), fp), " ");
		int num_vertices = firstline[0];
		int dim = firstline[1];
		int num_bmarkers = firstline[2];

		float vertices [num_vertices][dim];

		int i = 0;

    	while (fgets(line, sizeof(line), fp) != NULL)
    	{
        	vertices[i] = line;
        	printf(line);
        	i++;
    	}
	}
   return 0;
}